import requests

from golgi import configurable
from tek.tools import find
from tek import logger

from tek_utils.sharehoster.errors import ShareHosterError


def is_dir(fdict):
    return fdict and fdict.get('content_type') == 'application/x-directory'


class RestClient(object):
    headers = {
        'accept': 'application/json',
    }

    def request(self, req_type, url, body={}, redirect=True, params={}):
        requester = getattr(requests, req_type)
        try:
            request = requester(url, data=body, headers=self.headers,
                                allow_redirects=redirect, params=params)
        except requests.RequestException as e:
            msg = 'Request failed! ({})'.format(e)
            raise ShareHosterError(msg) from e
        else:
            request.connection.close()
            return request

    def response(self, req_type, url, **kw):
        request = self.request(req_type, url, **kw)
        return self._handle_response(request)

    def _handle_response(self, response):
        try:
            _json = response.json()
        except ValueError:
            return {}
        else:
            return _json


@configurable(putio=['token'])
class PutIoClient(object):
    _api_url_tmpl = 'https://api.put.io/v2/{path}?oauth_token={token}'
    _rest = RestClient()

    def _api(self, method, path, **kw):
        return self._rest.response(method, self._api_url(path), **kw)

    def _api_url(self, path):
        return self._api_url_tmpl.format(path=path, token=self._token)

    def get(self, path, **kw):
        return self._api('get', path, **kw)

    def post(self, path, **kw):
        return self._api('post', path, **kw)

    def put(self, path, **kw):
        return self._api('put', path, **kw)

    def delete(self, path, **kw):
        return self._api('delete', path, **kw)

    def raw(self, method, path, **kw):
        return self._rest.request(method, self._api_url(path), redirect=False,
                                  **kw)

    @property
    def transfers(self):
        return self.get('transfers/list').get('transfers', [])

    def request(self, torrent):
        return self.post('transfers/add', body=self._request_params(torrent))

    def _request_params(self, torrent):
        return dict(
            url=torrent,
            parent_id=0,
            extract=False,
            callback_url=None,
        )

    def transfer_for_torrent(self, torrent):
        return find(lambda t: t.get('source') == torrent, self.transfers, {})

    def cancel_transfers(self, ids):
        return self.post('transfers/cancel', body=dict(transfer_ids=ids))

    def clean_transfers(self):
        return self.post('transfers/clean')

    def download_url(self, _id):
        request = self.raw('get', 'files/{}/download'.format(_id))
        return request.headers.get('location', '')

    def zip_url(self, _id):
        request = self.raw('get', 'files/zip', body=dict(file_ids=[_id]))
        return request.headers.get('location', '')

    def file(self, _id):
        return self.get('files/{}'.format(_id)).get('file')

    def files(self, _id=None):
        params = {} if _id is None else dict(parent_id=_id)
        return self.get('files/list', params=params).get('files')

    @property
    def account_info(self):
        return self.get('account/info').get('info')

    def delete_file(self, _id):
        return self.post('files/delete', body=dict(file_ids=[_id]))


class PutIoFile(object):
    _client = None

    def __init__(self, torrent=None, file_id=None, largest_file=True):
        self.torrent = torrent
        self._file_id = file_id
        self._largest_file = largest_file
        self._create_info = {}
        self._info = {}

    def request(self):
        self.update()
        if not self.downloaded:
            response = self.client.request(self.torrent)
            if response.get('status') == 'ERROR':
                msg = response.get('error_message')
                logger.error('Error requesting torrent: {}'.format(msg))
            else:
                self._create_info = response.get('transfer', {})

    @property
    def client(self):
        if self._client is None:
            self._client = PutIoClient()
        return self._client

    def update(self):
        if self.id == -1:
            self._lookup_transfer()
        response = self.client.get('transfers/{}'.format(self.id))
        self._info = response.get('transfer', {})

    def _lookup_transfer(self):
        self._create_info = self.client.transfer_for_torrent(self.torrent)

    @property
    def id(self):
        return self._create_info.get('id', -1)

    @property
    def file_id(self):
        return self._file_id or self.info.get('file_id')

    @property
    def downloaded(self):
        return (self.file_id is not None or
                str(self.info.get('percent_done')) == '100')

    @property
    def status(self):
        return self.info.get('status', 'unknown')

    @property
    def status_message(self):
        return self.info.get('status_message', 'no status message')

    @property
    def caching(self):
        return self.status in ['IN_QUEUE', 'DOWNLOADING']

    @property
    def info(self):
        self.update()
        return self._info

    def cancel(self):
        return self.client.cancel_transfers([self.id])

    @property
    def download_url(self):
        if self.downloaded:
            return self.client.download_url(self.content_id)

    @property
    def content_id(self):
        if self.is_dir and self._largest_file:
            return self.largest_file_id
        else:
            return self.file_id

    @property
    def largest_file_id(self):
        def filesize(fdict):
            return 0 if is_dir(fdict) else fdict.get('size', 0)
        files = self.all_files
        if files:
            target = max(files, key=filesize)
            return target.get('id', self.file_id)
        else:
            return self.file_id

    @property
    def all_files(self):
        if self.is_dir:
            return list(self.files_recursive(self.file_id))
        else:
            return [self.file]

    def files_recursive(self, file_id):
        for _file in self.files(file_id):
            if is_dir(_file):
                yield from self.files_recursive(_file.get('id', -1))
            else:
                yield _file

    def files(self, file_id=None):
        file_id = file_id or self.file_id
        return self.client.files(file_id)

    @property
    def valid(self):
        if self._file_id:
            return True
        else:
            self.update()
            return self.id != -1

    def directories(self, file_id=None):
        file_id = file_id or self.file_id
        return [f for f in self.files(file_id) if is_dir(f)]

    @property
    def file(self):
        return self.client.file(self.file_id)

    @property
    def is_dir(self):
        return is_dir(self.file)

    def delete(self):
        if self.downloaded:
            self.client.delete_file(self.file_id)
        else:
            logger.warn('Cannot delete uncached file "{}"'.format(self))

    @property
    def name(self):
        return self.info.get('name', 'unknown')

__all__ = ['PutIoClient']
