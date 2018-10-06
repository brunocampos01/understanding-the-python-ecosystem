import re
from datetime import datetime
import calendar

from tek.errors import ParseError


def domain(url):
    """ Extract the domain name out of url.
    """
    if isinstance(url, str):
        domain_match = re.match(r'https?://(?:www\.)?([^/]+)\.[^/]+', url)
        return domain_match.group(1) if domain_match else ''
    else:
        raise ParseError('Invalid input for domain(): {}'.format(url))


def unix_to_datetime(stamp):
    return datetime.utcfromtimestamp(stamp)


def datetime_to_unix(_date):
    return calendar.timegm(_date.utctimetuple())


def now_unix():
    return datetime_to_unix(datetime.now())

__all__ = ('domain', 'unix_to_datetime', 'datetime_to_unix')
