import os
import re

from golgi.config import configurable
from tek.util.decorator import lazy_property

from tek_utils.sharehoster.common import LinkCheckingDownloader


@configurable(zevera=['user', 'password'])
class ZeveraDownloader(LinkCheckingDownloader):
    _zevera_url = ('https://zevera.com/getFiles.aspx?'
                   'login={user}&pass={password}&ourl={url}')

    def _setup_params(self):
        def trim(filename):
            return re.sub('\.html?$', '', filename)

        def split(url):
            return url.rsplit('/')[-2:]
        fileid, filename = split(self.url)
        self.file_path = os.path.join(self._download_dir, trim(filename))

    @lazy_property
    def effective_url(self):
        return self._zevera_url.format(user=self._user,
                                       password=self._password, url=self.url)

__all__ = ['ZeveraDownloader']
