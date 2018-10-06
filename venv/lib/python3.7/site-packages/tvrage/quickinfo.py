from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import quote
from .util import _fetch
from .exceptions import ShowNotFound

BASE_URL = 'http://services.tvrage.com/tools/quickinfo.php'


def fetch(show, exact=False, ep=None):
    query_string = '?show=' + quote(show)
    if exact:
        query_string = query_string + '&exact=1'
    if ep:
        query_string = query_string + '&ep=' + quote(ep)
    resp = _fetch(BASE_URL + query_string).read()
    show_info = {}
    if 'No Show Results Were Found For' in resp:
        raise ShowNotFound(show)
    else:
        data = resp.replace('<pre>', '').splitlines()
        for line in data:
            k, v = line.split('@')
            # TODO: use datetimeobj for dates
            show_info[k] = (v.split(' | ') if ' | ' in v else
                            (v.split('^') if '^' in v else v))
    return show_info
