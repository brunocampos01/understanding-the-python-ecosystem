from tek_utils.sharehoster.torrent import torrent_cacher

from golgi.config import configurable

from amino.lazy import lazy


@configurable(torrent=['cacher'])
class TorrentProxy(object):

    def __init__(self, record):
        self.record = record
        self.link = record.url

    @lazy
    def cacher(self):
        return torrent_cacher(self.link)

    @property
    def domain(self):
        self._cacher

    @property
    def cachable(self):
        return not (self.caching or self.cached)

    @property
    def caching(self):
        return self.valid and self.cacher.caching

    @property
    def cached(self):
        return self.valid and self.cacher.downloaded

    def request(self):
        if self.valid:
            self.cacher.request()

    @property
    def valid(self):
        return self.cacher is not None

    @property
    def download_url(self):
        if self.valid:
            return self.cacher.download_url

__all__ = ['TorrentProxy']
