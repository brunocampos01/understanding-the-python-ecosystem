from tek_utils.sharehoster.torrent import _clients, _cachers

downloadable = {}  # type: dict
caching = {}  # type: dict


class SpecCacher(object):

    def __init__(self, torrent=None, file_id=None, largest_file=True):
        self.torrent = torrent
        self._file_id = file_id
        self._largest_file = largest_file
        self._create_info = {}
        self._info = {}
        self.downloaded = downloadable.get(self.torrent, True)

    @property
    def caching(self):
        return caching.get(self.torrent, False)

    def request(self):
        pass

    @property
    def download_url(self):
        return 'http://host/{}/filename'.format(self.torrent[7:])

    @property
    def status(self):
        return ('IN_QUEUE' if self.caching else 'DOWNLOADED' if self.downloaded
                else 'NONE')

    @property
    def status_message(self):
        return ('up: 5 down: 2' if self.caching else 'downloaded' if
                self.downloaded else 'nope')


class SpecClient(object):

    @property
    def account_info(self):
        return True

    @property
    def transfers(self):
        return []

_clients['spec'] = SpecClient
_cachers['spec'] = SpecCacher
