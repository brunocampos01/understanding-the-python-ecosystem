import os
import re

from golgi.config import configurable

from tek_utils.sharehoster.common import LinkCheckingDownloader


@configurable(uploaded=['cookies'])
class UploadedDownloader(LinkCheckingDownloader):

    def _setup_params(self):

        def trim(filename):
            return re.sub('\.html?$', '', filename)

        def split(url):
            return url.rsplit('/')[-2:]

        fileid, filename = split(self.url)
        self.file_path = os.path.join(self._download_dir, trim(filename))

    @property
    def cookies(self):
        return self._cookies

__all__ = ['UploadedDownloader']
