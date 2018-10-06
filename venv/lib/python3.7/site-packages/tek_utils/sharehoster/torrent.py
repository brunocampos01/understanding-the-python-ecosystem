import time
import itertools
import collections
from urllib.parse import urlencode, urlparse, parse_qs

import requests

import tek
from tek.util.decorator import lazy_property
from tek.tools import sizeof_fmt, maxlen
from tek.user_input import CheckboxList, SpecifiedChoice
from tek import logger

from golgi import Config
from golgi.config import configurable, ConfigError
from golgi.io.terminal import terminal

from amino import Map, __, List, Right, Left, Maybe, _, Either
from amino.regex import Regex

from tek_utils.sharehoster.putio import PutIoFile, PutIoClient, is_dir
from tek_utils.sharehoster import Downloader


def parse_int(i):
    return Right(i) if isinstance(i, int) else (
        Right(int(i)) if isinstance(i, str) and i.isdigit() else
        Left('could not parse int {}'.format(i))
    )

_cachers = {
    'putio': PutIoFile,
}

_clients = {
    'putio': PutIoClient,
}

yify_url = 'https://yts.ag/api/v2/list_movies.json'


def is_torrent(url):
    ''' Indicate whether url points to a torrent file or is a magnet
    link.
    '''
    return (isinstance(url, str) and (url.endswith('torrent') or
                                      url.startswith('magnet')))


def torrent_cacher(*a, **kw):
    Cacher = _cachers.get(Config['torrent'].cacher)
    if Cacher:
        return Cacher(*a, **kw)


def torrent_cacher_client(*a, **kw):
    Client = _clients.get(Config['torrent'].cacher)
    if Client:
        return Client(*a, **kw)


def truncate(items, *columns):
    ''' truncate the main strings for a SpecifiedChoice-like output
    according to the available terminal size.
    'columns' is a list of additional column widths, assumed to be
    separated by a three character wide field.
    The line enumeration is assumed to be 4 characters plus the width of
    the number wide.
    A single padding character is placed at the very right.
    '''
    term_width = terminal.cols
    if term_width is None:
        term_width = 80
    rest = sum(columns) + 3 * len(columns) + 4 + len(str(len(items))) + 1
    length = term_width - rest
    return [i[:length] for i in items]


class Magnet:
    _urn_re = Regex('urn:(.*:.*)')

    def __init__(self, name: Maybe[str], params: Map) -> None:
        self.name = name
        self.params = params

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.name |
                               self.params)

    @property
    def urn(self):
        return (
            self.params.get('xt') //
            _.head //
            Magnet._urn_re.match //
            __.l.lift(0)
        )


def parse_magnet(magnet) -> Either[str, Magnet]:
    pr = urlparse(magnet)
    if pr.scheme == 'magnet':
        q = Map(parse_qs(pr.query)).valmap(List.wrap)
        name = q.get('dn') // _.head
        return Right(Magnet(name, q))
    else:
        return Left('not a magnet')


class FilePickerList(CheckboxList):

    def process(self):
        super(FilePickerList, self).process()
        if self._input in 'dfr':
            self._force_terminate = True


class Input(object):

    def __init__(self, current, files):
        self.dir = current
        self.files = files
        self._init_strings()
        self._init_params()

    def _init_strings(self):
        titles = self._titles
        _format = '{u: <{ua}} | {s: >{sa}}'
        size_strings = self._size_strings
        max_size = maxlen(*size_strings)
        titles = truncate(titles, max_size)
        max_name = maxlen(*titles)
        self.lines = [_format.format(u=u, s=s, ua=max_name, sa=max_size)
                      for u, s in zip(titles, size_strings)]
        self.total_size = sum(self._sizes)
        self.text_pre = [self.dir['name'], ''] if self.dir else []

    @lazy_property
    def _menu(self):
        return self._type(self.lines, simple=self._simple, enter=self._enter,
                          text_pre=self.text_pre, text_post=self.text,
                          values=self.files, remove_text=True, newline=False,
                          overwrite=False)

    def read(self):
        choice = self._menu.read()
        return self._menu.value, choice

    @property
    def _titles(self):
        return [f['name'] for f in self.files]

    @property
    def _sizes(self):
        return [f['size'] for f in self.files]

    @property
    def _size_strings(self):
        return [sizeof_fmt(s) for s in self._sizes]


class Browser(Input):

    def _init_params(self):
        self.text = ['Total: {}'.format(sizeof_fmt(self.total_size)),
                     'Download [a]ll ([z]ipped), select a directory or'
                     ' [p]arent, toggle [s]election mode or [f]lat display'
                     ' or [q]uit.']
        self._type = SpecifiedChoice
        self._simple = ['s', 'p', 'q', 'a', 'f', 'z']
        self._enter = 's'


class FilePicker(Input):

    def _init_params(self):
        self.text = ['Total: {}'.format(sizeof_fmt(self.total_size)),
                     'Toggle [a]ll or individual files, toggle [f]lat display,'
                     ' [r]emove or [d]ownload selected files.']
        self._type = FilePickerList
        self._simple = ['f', 'd', 'r']
        self._enter = 'q'


SearchResult = collections.namedtuple(
    'SearchResult', ['title', 'size', 'size_str', 'seeders', 'magnet_link']
)

trackers = List('udp://open.demonii.com:1337/announce',
                'udp://tracker.openbittorrent.com:80')


def yify_magnet(name, hsh):
    query = (List(('xt', 'urn:btih:{}'.format(hsh)), ('dn', name)) +
             (trackers / (lambda a: ('tr', a))))
    return 'magnet:?{}'.format(urlencode(query))


class SearchResultFactory(object):

    @classmethod
    def from_tpb(self, result):
        return SearchResult(result['title'], result['size'],
                            result['size_str'], result['seeders'],
                            result['magnet_link'])

    @classmethod
    def from_lime(self, result):
        return SearchResult(result['title'], result['size'],
                            result['size_str'], result['seeders'],
                            result['magnet_link'])

    @classmethod
    def from_kickass(self, result):
        seed = parse_int(result.seed) | 0
        return SearchResult(result.name, result.size, seed,
                            result.magnet_link)

    @classmethod
    def from_yify(self, result):
        data = Map(result)
        title_long = data.get('title_long') | 'no title'
        title = data.get('title') | 'no title'
        def parse(torr):
            td = Map(torr)
            name = '{} {}'.format(title_long, td.get('quality') | '')
            size = td.get('size_bytes') | 0
            size_str = sizeof_fmt(str(size))
            seeds = td.get('seeds') | 0
            hsh = td.get('hash') | 'no_hash'
            magnet_link = yify_magnet(title, hsh)
            return SearchResult(name, size, size_str, seeds, magnet_link)
        return data.get('torrents') / List.wrap / __.map(parse) | List()


class SearchResultChoice(Input):

    def __init__(self, query, search):
        self._query = query
        super(SearchResultChoice, self).__init__(None, search)

    def _init_params(self):
        self.text_pre = ['Results for \'{}\':'.format(self._query), '']
        self.text = ['Choose one or [q]uit']
        self._type = SpecifiedChoice
        self._simple = ['q']
        self._enter = 'q'

    def _init_strings(self):
        _format = '{u: <{ua}} | {d: >{da}} | {s: >{sa}}'
        titles = [f.title for f in self.files]
        size_strings = [f.size_str for f in self.files]
        seeders = [str(f.seeders) for f in self.files]
        max_size = maxlen(*size_strings)
        max_seeders = maxlen(*seeders)
        titles = truncate(titles, max_size, max_seeders)
        max_name = maxlen(*titles)
        self.lines = [_format.format(u=u, d=d, s=s, ua=max_name,
                                     da=max_seeders, sa=max_size)
                      for u, s, d in zip(titles, size_strings, seeders)]
        self.text_pre = [self.dir['name'], ''] if self.dir else []

    def read(self):
        choice = self._menu.read()
        return self._menu.raw_value, choice


@configurable(torrent=['limit', 'delete', 'pirate_bay_url', 'search_engine'])
class TorrentDownloader(object):

    def __init__(self, args=[]):
        engines = {
            'kickass': self._search_kickass,
            'piratebay': self._search_tpb,
            'piratebay_old': self._search_tpb_old,
            'yify': self._search_yify,
            'lime': self._search_lime,
        }
        self.args = args
        self._nested = True
        self._browse = True
        self._current = None
        self._cachers = []
        self._uris = []
        if self._search_engine not in engines:
            raise ConfigError(
                'No such search engine: {}'.format(self._search_engine)
            )
        self._search = engines[self._search_engine]

    def process(self):
        if not self._search_terms_given or self._search():
            self.cache()
            self.menu_loop()

    def _search_tpb_old(self):
        import tpb
        query = ' '.join(self.args)
        bay = tpb.TPB(self._pirate_bay_url)
        search = bay.search(query).order(tpb.ORDERS.SEEDERS.DES)
        results = [SearchResultFactory.from_tpb(res) for res in
                   itertools.islice(search, self._limit)]
        return self._handle_results(query, results)

    def _search_tpb(self):
        from tek_utils.sharehoster import piratebay
        query = ' '.join(self.args)
        search = piratebay.Search(query)
        results = search.run[:self._limit] / SearchResultFactory.from_tpb
        return self._handle_results(query, results)

    def _search_kickass(self):
        from tek_utils.sharehoster import kickass
        query = ' '.join(self.args)
        search = kickass.Search(query).order(kickass.ORDER.SEED,
                                             kickass.ORDER.DESC)
        results = [SearchResultFactory.from_kickass(res) for res in
                   itertools.islice(search, self._limit)]
        return self._handle_results(query, results)

    def _search_yify(self):
        query = ' '.join(self.args)
        response = requests.get(yify_url, params=dict(query_term=query,
                                                      limit=self._limit))
        data = Map(response.json())
        results = (
            (data.get('data') /
             Map //
             __.get('movies') /
             List.wrap /
             __.flat_map(SearchResultFactory.from_yify)) |
            List()
        )
        return self._handle_results(query, results)

    def _search_lime(self):
        from tek_utils.sharehoster import limetorrents
        query = ' '.join(self.args)
        search = limetorrents.search(query)
        results = search[:self._limit] / SearchResultFactory.from_lime
        return self._handle_results(query, results)

    def search_results(self) -> List[str]:
        return self._uris

    def _handle_results(self, query, results):
        if results:
            return self._choose_result(query, results)
        else:
            logger.warn('No results for "{}"'.format(query))

    def _choose_result(self, query, results):
        choice = SearchResultChoice(query, results)
        action, torrent = choice.read()
        if action != 'q':
            self._uris = [torrent.magnet_link]
            return True

    def cache(self):
        for uri in self._uris:
            cacher = self.cacher(uri)
            self._cachers.append(cacher)
            cacher.request()

    def cacher(self, uri):
        return torrent_cacher(uri, largest_file=False)

    @lazy_property
    def client(self):
        return torrent_cacher_client()

    def menu_loop(self):
        action = None
        self._set_initial_file()
        while not action == 'q':
            action, choice = self.display_menu()
            self.handle_input(action, choice)

    def _set_initial_file(self):
        if self._single_uri:
            cacher = self.cacher(self._uris[0])
            if cacher.downloaded:
                self._current = cacher.file

    def display_menu(self):
        if self._wait_for_files():
            Menu = Browser if self._nested and self._browse else FilePicker
            return Menu(self._current, self._files).read()
        else:
            return 'q', 'q'

    def handle_input(self, action, choice):
        if action == 'f':
            self._nested = not self._nested
        if action == 's':
            self._browse = not self._browse
        elif action == 'p':
            self._current = self._parent
        elif action == 'd':
            self._download(choice)
        elif action == 'r':
            self._delete_file(choice)
        elif action == 'a':
            self._download(self._current_files)
        elif action == 'z':
            self._download_zipped(self._current)
        elif isinstance(choice, dict):
            self._current = choice
        else:
            return choice

    @property
    def _current_id(self):
        if self._current:
            return self._current.get('id', 0)

    @property
    def _parent(self):
        if self._current:
            self.client.file(self._current.get('parent_id'))

    @property
    def _current_cacher(self):
        file_id = self._current_id
        if file_id:
            return torrent_cacher(file_id=file_id)

    @property
    def _files(self):
        return sorted(self._current_files if self._nested
                      else self._all_files, key=lambda f: f['name'])

    @property
    def _all_files(self):
        cacher = self._current_cacher
        return cacher.all_files if cacher else self._current_files

    @property
    def _current_files(self):
        if self._current and not is_dir(self._current):
            return [self._current]
        else:
            return self.client.files(self._current_id)

    def _download(self, states):
        for selected, _file in zip(states, self._files):
            if selected:
                self._download_tree(_file['id'])

    def _download_tree(self, file_id):
        proxy = PutIoFile(file_id=file_id)
        files = proxy.all_files
        links = [self.client.download_url(_file['id']) for _file in files]
        self._download_files(files, links)
        if self._delete:
            proxy.delete()

    def _download_zipped(self, _file):
        if _file:
            link = self.client.zip_url(_file['id'])
            self._download_file(link, _file.get('name'))

    def _download_files(self, files, links):
        for link, _file in zip(links, files):
            name = _file.get('name')
            self._download_file(link, name)

    def _download_file(self, link, name):
        downloader = Downloader(link)
        try:
            downloader.retrieve()
        except tek.errors.NotEnoughDiskSpace as e:
            logger.error(e)
        else:
            state = 'complete' if downloader.success else 'failed'
            logger.info('')
            logger.info('Download {}: {}'.format(state, name))

    def _delete_file(self, states):
        for selected, _file in zip(states, self._files):
            if selected:
                PutIoFile(file_id=_file['id']).delete()

    def _wait_for_files(self):
        if not self._files and self._uris:
            logger.info('Files not synced yet. Waiting for 5 seconds.')
            time.sleep(5)
        return bool(self._files)

    @property
    def _single_uri(self):
        return bool(self._uris) and len(self._uris) == 1

    @property
    def _uris_given(self):
        return bool(self.args) and is_torrent(self.args[0])

    @property
    def _search_terms_given(self):
        return bool(self.args) and not is_torrent(self.args[0])


__all__ = ('torrent_cacher', 'TorrentDownloader')
