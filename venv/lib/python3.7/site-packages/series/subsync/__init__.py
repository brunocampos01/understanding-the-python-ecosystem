import re
import os
from io import StringIO
from urllib.parse import urljoin
from operator import attrgetter

from lxml import etree

import requests

from golgi import Config, cli
from golgi.config import configurable, ConfigError

from tek.user_input import CheckboxList
from tek.tools import parallel_map

from amino import Path

from series import SubtitleMetadata, latest_season_dir
from series import dir_info, episode_number, get_release

from series.subsync.errors import NoSubsForEpisode
from series.logging import Logging, log


@configurable(subsync=['series_url_map'])
class SubtitleQueryData(SubtitleMetadata):

    def __init__(self, search_name, canonical_name, season, episode,
                 release=None, extension='srt'):
        self.canonical_name = canonical_name
        super().__init__(search_name, season, episode, release=release,
                         extension=extension)

    @property
    def local_path(self):
        path = Path(self.canonical_name) / 's{}'.format(self.season)
        if self.extension == 'srt':
            path = path / 'sub'
        return path / self.filename

    @property
    def file_series_name(self):
        return self.canonical_name

    @property
    def query_data(self):
        return [self._series_name] + self[1:]

    @property
    def _series_name(self):
        return self._series_url_map.get(self[0], self[0])


@configurable(subsync=['base_url', 'cookies'])
class SubtitleHTTPHandler(object):

    def get(self, url):
        if self._base_url is None:
            raise ConfigError('subsync: config option "base_url" must be set!')
        url = urljoin(self._base_url, url)
        return requests.get(url, cookies=self._cookies).text


@configurable(series=['series_dir'], subsync=['base_url', 'cookies'])
class Subtitle(Logging):

    def __init__(self, info, release, url, hearing_impaired):
        self.metadata = info
        self.release = release
        self._url = url
        self._content = None
        self.hearing_impaired = hearing_impaired
        self._http = SubtitleHTTPHandler()

    @property
    def local_path(self):
        return self.metadata.local_path

    @property
    def content(self):
        if self._content is None:
            try:
                self._content = self._http.get(self._url)
            except requests.RequestException as e:
                self.log.error('Subtitle: {}'.format(e))
        return self._content

    def write(self):
        self.write_to(self.local_path)

    def write_to(self, local_path):
        path = self._series_dir / local_path
        base = path.parent
        if not base.is_dir():
            base.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            if self.content:
                f.write(self.content)
            else:
                self.log.error('Could not download the subtitle.')


class HTMLParser(object):
    xpath_deaf = "descendant::img[@title='Hearing Impaired']"
    xpath_download = "descendant::a[@class='buttonDownload']"
    release_re = re.compile(r'Version ([^,]+),')
    parser = etree.HTMLParser()

    def __init__(self, info):
        self._info = info
        self._http = SubtitleHTTPHandler()

    def subtitles(self):
        url = 'serie/{}/{}/{}/1'.format(*self._info.query_data)
        html = str(self._http.get(url))
        return self._parse(html)

    def _parse(self, html):
        tree = etree.parse(StringIO(html), self.parser)
        if tree.getroot() is None:
            raise NoSubsForEpisode(*self._info)
        epi_divs = tree.xpath("//div[@id='container95m']")
        return [_f for _f in map(self.subtitle_from_div, epi_divs) if _f]

    def subtitle_from_div(self, div):

        def release():
            for line in div.itertext():
                match = self.release_re.search(line)
                if match:
                    return match.group(1).lower()

        def subtitle():
            download = div.xpath(self.xpath_download)[-1]
            return download.attrib['href']
        try:
            hearing_impaired = bool(div.xpath(self.xpath_deaf))
            return Subtitle(self._info, release(), subtitle(),
                            hearing_impaired)
        except IndexError:
            pass


def get_episode(search_name, season, number, release=None,
                canonical_name=None):
    from tek.tools import find
    canon = canonical_name or search_name
    info = SubtitleQueryData(search_name, canon, season, number, release)
    parser = HTMLParser(info)
    subs = parser.subtitles()
    if not subs:
        raise NoSubsForEpisode(search_name, season, number)
    same_release = lambda sub: sub.release == release
    if release is not None:
        matching = list(filter(same_release, subs))
        if matching:
            subs = matching
    not_deaf = lambda sub: not sub.hearing_impaired
    return find(not_deaf, subs) or subs[0]


def write_subs(subs):
    input = CheckboxList(list(map(attrgetter('local_path'), subs)),
                         [True] * len(subs),
                         text_pre=['Downloading these subtitles:'],
                         text_post=['Write to series dir?'])
    write = input.read()

    def process(args):
        sub, doit = args
        if doit:
            sub.write()

    return parallel_map(process, zip(subs, write))


def subsync_episode(metadata, write=True):
    try:
        sub = get_episode(*metadata.all)
        if write:
            sub.write()
        return sub
    except NoSubsForEpisode:
        pass


def target_episodes(vid_epis, sub_epis):
    conf = Config['subsync']
    targets = conf.episodes
    if not targets:
        if conf.only_latest:
            vid_max = max(vid_epis) if vid_epis else 0
            sub_max = max(sub_epis) if sub_epis else 0
            targets = range(sub_max + 1, vid_max + 1)
        else:
            targets = set(vid_epis) - set(sub_epis)
    return sorted(targets)


def subsync_dir(_dir, write=True):
    subs = []
    series_name, season = dir_info(_dir)
    if season is None:
        log.error('Not a season dir!')
    else:
        subs_dir = os.path.join(_dir, 'sub')
        if not os.path.isdir(subs_dir):
            os.makedirs(subs_dir)
        present_vids = os.listdir(_dir)
        present_subs = os.listdir(subs_dir)
        vid_epis = [_f for _f in map(episode_number, present_vids) if _f]
        sub_epis = [_f for _f in map(episode_number, present_subs) if _f]
        targets = target_episodes(vid_epis, sub_epis)

        def process(number):
            try:
                release = get_release(series_name, season, number)
                return get_episode(series_name, season, number, release)
            except NoSubsForEpisode:
                log.warning('No subs found for episode {}!'.format(number))

        subs = [sub for sub in parallel_map(process, targets) if sub is not
                None]
        if subs and write:
            write_subs(subs)
    return subs


@cli(positional=(('cli_dir', 1), ('episodes', '*')))
def subsync_dir_cli():
    _dir = Config['subsync'].cli_dir[0]
    return subsync_dir(_dir)


@cli(positional=(('episodes', '*'),))
def subsync_cwd():
    return subsync_dir(os.getcwd())


@cli()
def subsync_auto():
    monitor = Config['series'].monitor

    def sync():
        for _dir in map(latest_season_dir, monitor):
            yield subsync_dir(_dir, write=False)

    subs = sum(sync(), [])
    if subs:
        write_subs(subs)
