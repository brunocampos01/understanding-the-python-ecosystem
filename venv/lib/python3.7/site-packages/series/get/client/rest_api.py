from datetime import datetime

from golgi.config import configurable

from tek.user_input import SpecifiedChoice, input_queue

from tek_utils.sharehoster.torrent import TorrentDownloader

from golgi.io.terminal import terminal as term, ColorString

from amino import Map, List, __, Empty, Just, Left, Right, IO, _, Try, Boolean, Lists
from amino.util.string import camelcaseify

from series.api_client import (ApiClientMeta, ApiClient, RecordCommand,
                               ClientBase, command_base, command)
from series.get import format_explain_release, format_explain_show
from series.get.util.format import format_status_lines
from series.etvdb import ETVDBFacade
from series.get.model.release import Release
from series.util import datetime_to_unix


def is_error(response):
    return isinstance(response, dict) and 'error' in response


purge_msg = 'Deleted {} monitors, {} orphan links and {} orphan releases'


class ReleaseCommand(RecordCommand):

    @property
    def _arg_error(self):
        return 'args must be an id or (show season episode)'

    @property
    def _data_arg_error(self):
        return 'args must be (show season episode)'

    @property
    def _id_spec(self):
        return self.args.head.map(Left).io(self._arg_error)

    @property
    def _data_spec(self):
        return (
            self.args.lift_all(0, 1, 2)
            .map3(lambda n, s, e: dict(show=n, season=s, episode=e))
            .io(self._arg_error)
            .map(Right)
        )

    @property
    def _data_path(self):
        tpl = 'release/{show}/{season}/{episode}'
        form = lambda a: IO.pure(tpl.format(**a))
        return self._data_spec // __.cata(IO.failed(self._arg_error), form)

    @property
    def _type(self):
        return 'release'

    @property
    def rest(self):
        return self.args.tail if self.is_id_spec else Just(self.args.drop(3))


class ShowCommand(RecordCommand):

    @property
    def _arg_error(self):
        return 'args must be an id or show name'

    @property
    def _id_spec(self):
        return self.args.head.map(Left).io(self._arg_error)

    @property
    def _data_spec(self):
        return (
            self.args.head
            .map(lambda a: dict(name=a))
            .map(Right)
            .io(self._arg_error)
        )

    @property
    def _data_path(self):
        tpl = 'show/{name}'
        form = lambda a: IO.pure(tpl.format(**a))
        return self._data_spec // __.cata(IO.failed(self._arg_error), form)

    @property
    def _type(self):
        return 'show'

    @property
    def rest(self):
        return self.args.tail | List()


def release_cmd(desc, params=List()):
    pd = '(id || show season episode) {}'.format(params.join_tokens)
    return command_base(ReleaseCommand, pd, desc, params=params)


def show_cmd(desc, params=List()):
    pd = '(id || name) {}'.format(params.join_tokens)
    return command_base(ShowCommand, pd, desc, params=params)


@configurable(get_client=['rest_api_port', 'rest_api_url', 'query_etvdb'])
class GetClient(ClientBase, metaclass=ApiClientMeta):

    @property
    def client(self):
        return ApiClient(self._rest_api_url, self._rest_api_port)

    def _resolve_show(self, name):
        e = ETVDBFacade()
        def run(names, ids):
            return (
                Empty()
                if ids.empty else
                ids.head
                if ids.length == 1 else
                self._ask_show(names, ids)
            )
        return e.shows(name).flat_map2(run)

    def _ask_show(self, names, ids):
        choice = SpecifiedChoice(names, text_pre=['Select a show'])
        choice.read()
        return ids.lift(choice.index)

    @release_cmd('Add the url to the specified release\'s links', List('url'))
    def add_link(self, cmd):
        data = lambda a: a // _.head / (lambda b: dict(url=b))
        return cmd.put(data=data, path=Just('link'))

    @command('[regex]', 'Display info for all releases matching the ' +
             ' regex (default all)')
    def list(self, cmd):
        regex = cmd.args.head | ''
        return IO.pure(list(self._format_list(self._list(regex))))

    def _list(self, regex):
        return self.client.get('release', body=dict(regex=regex))

    def _format_list(self, matches):
        series = lambda r: ColorString(
            camelcaseify(r['series'], sep=' ', splitter='[ _]'), term.yellow)
        def enum(r):
            return '{}x{}'.format(
                ColorString(r['season'], term.blue),
                ColorString(r['episode'], term.blue),
            )
        if matches:
            text = '{} {} {} {}{}'
            for m in matches:
                r = m['release']
                dl = ' done' if m['downloaded'] else ''
                yield text.format(
                    ColorString('#{}'.format(m['id']), term.green),
                    series(r),
                    enum(r),
                    ColorString(r['airdate'], term.bold),
                    ColorString(dl, term.red)
                )
        else:
            yield 'No matching release found.'

    @release_cmd('Create a release')
    def create_release(self, cmd):
        return cmd.create()

    @release_cmd('Delete the release matching the supplied metadata')
    def delete_release(self, cmd):
        return cmd.delete

    @show_cmd('Add releases for aired episodes of the specified season',
              List('season'))
    def add_season(self, cmd):
        return (
            cmd.rest.head.io('specify a season') //
            (lambda a: cmd.post(path=Just('season/{}'.format(a))))
        )

    @show_cmd('Add the specified show', List('name', 'etvdb_id'))
    def add_show(self, cmd):
        name = cmd.args.head | ''
        def resolve():
            return self._resolve_show(name) if self._query_etvdb else Empty()
        def data(args):
            return args.head.o(resolve) / (lambda a: Map(id=a))
        return cmd.create(data=data)

    @show_cmd('Delete the specified show')
    def delete_show(self, cmd):
        return cmd.delete

    @command('[regex]', 'List show names matching the regex')
    def list_shows(self, cmd):
        regex = cmd.args.head | ''
        def output(matches):
            if matches:
                for id, description in matches:
                    i = ColorString('#{}'.format(id), term.green)
                    d = ColorString(description, term.yellow)
                    yield '{}: {}'.format(i, d)
            else:
                yield 'No matching show found.'
        return (IO.delay(self.client.get, 'show', body=dict(regex=regex)) /
                output / List.wrap)

    def print_shows(self, shows):
        colors = {
            0: term.blue,
            1: term.green,
            2: term.yellow,
            3: term.red,
        }
        if shows:
            for name, nepi, rel, status in shows:
                yield '{} {}'.format(ColorString('>>', term.red),
                                     ColorString(name, term.bold))
                yield '{} {}'.format(ColorString(' |', term.green), nepi)
                if rel:
                    col = colors.get(status, term.black)
                    yield '{} {}'.format(ColorString(' |', term.green),
                                         ColorString(rel, col))
                yield ''
        else:
            yield 'No matching show found.'

    def _shows(self, path, cmd):
        regex = cmd.args.head | ''
        return (self.client.get(path, body=dict(regex=regex)) /
                self.print_shows /
                List.wrap)

    @command('[regex]', 'Extended info for shows matching regex')
    def shows(self, cmd):
        return self._shows('show/info', cmd)

    @command('[regex]', 'List upcoming releases for shows matching regex')
    def next(self, cmd):
        return self._shows('show/next', cmd)

    @command('[regex]', 'List current releases for shows matching regex')
    def ready(self, cmd):
        return self._shows('show/ready', cmd)

    @command('[regex]', 'List downloaded releases for shows matching regex')
    def done(self, cmd):
        return self._shows('show/done', cmd)

    @release_cmd('Reset a release and mark its torrent as dead, forcing' +
                 'download of a different torrent')
    def reset_torrent(self, cmd):
        return cmd.put(path=Just('reset_torrent'))

    def _format_show(self, data):
        def fmt_line(key, value):
            return '{}: {}'.format(ColorString(key, term.yellow), value)
        return List.wrap(data.items()).map2(fmt_line)

    @release_cmd('Print release info')
    def show_release(self, cmd):
        return cmd.get() / self._format_show

    @show_cmd('Print show info')
    def show_show(self, cmd):
        return cmd.get() / self._format_show

    @release_cmd('Update release data', List('[key=value ...]'))
    def update_release(self, cmd):
        def data(args):
            return Just(Map(args.map(__.split('='))))
        return cmd.put(data) / self._format_show

    @show_cmd('Update show data', List('[key=value ...]'))
    def update_show(self, cmd):
        def data(args):
            return Just(Map(List.wrap(args).map(__.split('='))))
        return cmd.put(data) / self._format_show

    @release_cmd('Reset cooldown time for release')
    def activate_release(self, cmd):
        return cmd.put(path=Just('activate'))

    @show_cmd('Reset cooldown time for show')
    def activate_show(self, cmd):
        return cmd.put(path=Just('activate'))

    @release_cmd('Explain why the csv-specified services treat the release' +
                 ' as they do', List('[service[,service]*]'))
    def explain(self, cmd):
        def data(args):
            return args.head.map(lambda a: dict(services=a)).o(Just(dict()))
        def output(resp):
            return resp if is_error(resp) else format_explain_release(resp)
        return cmd.get(data=data, path=Just('explain')) / output

    @show_cmd('Explain why the csv-specified services treat the show as' +
              ' they do', List('[services]'))
    def explain_show(self, cmd):
        def data(args):
            return args.head.map(lambda a: dict(services=a)).o(Just(dict()))
        def output(resp):
            return resp if is_error(resp) else format_explain_show(resp)
        return cmd.get(data=data, path=Just('explain')) / output

    @release_cmd('set a release\'s airdate', List('[YYYY-]MM-DD'))
    def set_airdate(self, cmd):
        def data(args):
            return args.head / (lambda d: dict(date=d))
        return cmd.put(data, path=Just('airdate'))

    @command('', 'status of recent releases')
    def status(self, cmd):
        return IO.pure(format_status_lines(self._status))

    @property
    def _status(self):
        return Map(self.client.get('release/status'))

    @command('[data]', 'delete downloaded releases older than arg')
    def purge(self, cmd):
        days = cmd.args.head | 30
        self.log.info('Deleting releases older than {} days'.format(days))
        data = Map(self.client.put('release/purge', dict(days=days)))
        return IO.pure(
            purge_msg.format(data['monitors'], data['links'], data['releases'])
        )

    @release_cmd('Start manual search for the release, optionally with search query. If `date` is given as query, the' +
                 ' airdate is used.', List('[query]'))
    def search(self, cmd) -> None:
        def search(monitor) -> None:
            r = monitor['release']
            date = Try(datetime.strptime, r['airdate'], '%Y-%m-%d') | None
            release = Release(name=r['series'], season=r['season'], episode=r['episode'], search_name=r['search_name'],
                              airdate=date)
            query = cmd.rest.filter_not(_.empty) / _.join_tokens | release.search_query_no_res
            query1 = release.search_query_date if query == 'date' else query
            self.log.info(f'Searching torrent for "{release}" with query "{query1}"...')
            dl = TorrentDownloader([query1])
            res = Boolean(dl._search()).m(dl.search_results) / Lists.wrap // _.head
            return (
                res /
                (lambda l: cmd.put(data=(lambda i: Just(dict(url=l))), path=Just('link'))) |
                IO.failed('no search results')
            )
        def output(resp):
            return resp
        return cmd.get() // search / output

__all__ = ('ApiClient',)
