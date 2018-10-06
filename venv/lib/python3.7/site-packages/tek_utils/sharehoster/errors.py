from tek.errors import TException


class ShareHosterError(TException, ConnectionError):
    pass


class InvalidURLError(ShareHosterError):
    _text = 'Invalid sharehoster URL: {url}'

    def __init__(self, url, details=None):
        text = self._text.format(url=url)
        if details is not None:
            text = '{} ({})'.format(text, details)
        super(InvalidURLError, self).__init__(text)


class RapidshareError(ShareHosterError):
    pass


class IllegalFile(RapidshareError):

    def __init__(self, fname):
        text = 'DMCA takedown: {}'.format(fname)
        super(IllegalFile, self).__init__(text)


class NoMoreResults(TException):
    def __init__(self):
        super(NoMoreResults, self).__init__('No more results.')


class NetloadError(ShareHosterError):
    pass


class InvalidHosterError(InvalidURLError):

    def __init__(self, hoster):
        reason = 'Invalid hoster: {}'.format(hoster)
        super(InvalidHosterError, self).__init__(reason)


class TorrentError(ShareHosterError):
    pass

__all__ = ['InvalidURLError', 'RapidshareError', 'IllegalFile',
           'NoMoreResults', 'NetloadError', 'InvalidHosterError']
