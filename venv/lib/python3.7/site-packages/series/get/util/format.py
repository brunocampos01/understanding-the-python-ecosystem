from typing import Callable

from amino import _, Map, List, L
from amino.util.string import camelcaseify

from golgi.io.terminal import terminal as term, ColorString


def explain_item(e):
    for comp in e:
        name = str(ColorString(comp['name'], term.blue))
        cond = comp['cond']
        yield '{}: {}'.format(name, cond)


def explain_lines(data, title: Callable):
    for r in data:
        item = r['item']
        yield str(ColorString(title(item), term.bold))
        yield from explain_item(r['expl'])
        yield ''


def explain_release_lines(data):
    def title(monitor):
        data = Map(monitor['release']).values_at('series', 'season', 'episode')
        return '{} {}x{}'.format(*data)
    return List.wrap(explain_lines(data, title))


def format_explain_release(data):
    return explain_release_lines(data).join_lines


def explain_show_lines(data):
    return List.wrap(explain_lines(data, _['name']))


def format_explain_show(data):
    return explain_show_lines(data).join_lines


def format_status_lines(output):
        ind = '  {}'.format
        id = lambda r: ColorString('#{}'.format(r['id']), term.red)
        series = lambda r: ColorString(
            camelcaseify(r['series'], sep=' ', splitter='[ _]'), term.yellow)
        head = lambda t: ColorString('{}:'.format(t), term.green)
        def enum(r):
            return '{}x{}'.format(
                ColorString(r['season'], term.blue),
                ColorString(r['episode'], term.blue),
            )
        desc = lambda r: '{} {} {}'.format(id(r), series(r), enum(r))
        date = lambda r, d: ColorString(r.get(d, 'no date'), term.bold)
        with_date = lambda r, d: ind('{} – {}'.format(date(r, d), desc(r)))
        ad = lambda r: with_date(r, 'airdate')
        dd = lambda r: with_date(r, 'download_date')
        any_date = lambda r: r.get('download_date', r.get('airdate', ''))
        def entry(rs, h, fmt):
            s = List.wrap(rs).sort_by(any_date)
            return (s / fmt).cons(head(h)) if rs else List()
        def section(key, fmt, head):
            return output.get(key) / L(entry)(_, fmt, head) | List()
        return List(
            ('done', 'Downloaded episodes', dd),
            ('caching', 'Caching releases', ad),
            ('search', 'Searching for torrents', ad),
            ('next', 'Upcoming episodes', ad),
            ('downloading', 'Currently downloading', ad),
            ('failed', 'Failed downloads', ad),
            ('current_search', 'Current torrent search', ad),
        ).flat_map3(section)


def format_status(output):
    return format_status_lines(output).join_lines

__all__ = ('explain_item', 'explain_lines', 'explain_release_lines',
           'format_explain_release', 'explain_show_lines',
           'format_explain_show')
