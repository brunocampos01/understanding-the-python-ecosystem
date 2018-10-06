from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup


class TvrageError(Exception):
    """ Base class for custom exceptions"""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TvrageRequestError(TvrageError):
    """ Wrapper for HTTP 400 """
    pass


class TvrageNotFoundError(TvrageError):
    """ Wrapper for HTTP 404"""
    pass


class TvrageInternalServerError(TvrageError):
    """ Wrapper for HTTP 500"""
    pass


def _fetch(url):
    try:
        result = urlopen(url)
    except URLError as e:
        if 400 == e.code:
            raise TvrageRequestError(str(e))
        elif 404 == e.code:
            raise TvrageNotFoundError(str(e))
        elif 500 == e.code:
            raise TvrageInternalServerError(str(e))
        else:
            raise TvrageError(str(e))
    except Exception as e:
        raise TvrageError(str(e))
    else:
        return result


def parse_synopsis(page, cleanup=None):
    soup = BeautifulSoup(page)
    try:
        result = soup.find('div', attrs={'class': 'show_synopsis'}).text
        # cleaning up a litle bit
        if cleanup:
            result, _ = result.split(cleanup)
        return result
    except AttributeError as e:
        print(('parse_synopyis - BeautifulSoup.find(): %s' % e))
