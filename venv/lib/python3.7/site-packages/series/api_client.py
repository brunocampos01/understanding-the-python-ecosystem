import abc
import requests
import functools
from typing import Callable, Any

from flask import json

from amino import IO, Left, Right, List, __, _, L, Empty, Just, Boolean

from series.logging import Logging

from series.client.errors import SeriesClientException


def is_int(value):
    return (isinstance(value, int) or isinstance(value, str) and
            value.isnumeric())


class ApiClient(Logging):

    def __init__(self, url, port, info_output=True):
        self.url = url
        self.port = port
        self._info_output = info_output

    def _url(self, path):
        return '{}:{}/{}'.format(self.url, self.port, path)

    def _request(self, req_type, path, body):
        headers = {'content-type': 'application/json'}
        requester = getattr(requests, req_type)
        url = self._url(path)
        self.log.debug('api request: {}'.format(url))
        try:
            response = requester(url, data=json.dumps(body), headers=headers)
        except requests.RequestException as e:
            msg = 'Request failed! ({})'.format(e)
            raise SeriesClientException(msg) from e
        else:
            if response.status_code >= 400:
                self.log.error(
                    'API response status {}'.format(response.status_code))
            try:
                _json = response.json()
            except ValueError as e:
                msg = 'Error in API request (no JSON in response)!'
                raise SeriesClientException(msg) from e
            else:
                data = _json.get('response', {})
                if isinstance(data, dict) and 'error' in data:
                    self.log.error(data['error'])
                return data

    def get(self, path, body={}):
        return self._request('get', path, body)

    def post(self, path, body={}):
        return self._request('post', path, body)

    def put(self, path, body={}):
        return self._request('put', path, body)

    def delete(self, path, body={}):
        return self._request('delete', path, body)


class Command(metaclass=abc.ABCMeta):

    def __init__(self, name, args, client, param_desc, desc) -> None:
        self.name = name
        self.args = List.wrap(args)
        self.client = client
        self.param_desc = param_desc
        self.desc = desc


class RecordCommand(Command):

    def __init__(self, name, args, client, param_desc, desc, params) -> None:
        super().__init__(name, args, client, param_desc, desc)
        self.params = params

    @abc.abstractproperty
    def _id_spec(self) -> IO[Left]:
        ...

    @abc.abstractproperty
    def _data_spec(self) -> IO[Right]:
        ...

    @abc.abstractproperty
    def _data_path(self) -> IO[str]:
        ...

    @abc.abstractproperty
    def _type(self) -> str:
        ...

    @abc.abstractproperty
    def rest(self):
        ...

    def _lookup(self, data):
        def check(resp):
            return (
                IO.failed('no release found')
                if resp == -1 else
                IO.pure((resp, self.rest))
            )
        return IO.delay(self.client.get, '{}_id'.format(self._type), body=data) // check

    @property
    def is_id_spec(self) -> Boolean:
        return self.args.head.exists(is_int)

    @property
    def spec(self):
        return (self._id_spec
                if self.is_id_spec else
                self._data_spec)

    @property
    def data(self):
        return (
            self.spec //
            __.lmap(lambda a: IO.pure((a, self.args.tail | List())))
            .left_or_map(self._lookup)
        )

    def run(self, f: Callable[[int, List], Any]) -> IO:
        return self.data.flat_map2(f)

    def _req(self, meth, path=Empty(), data=None):
        sub = path / '/{}'.format | ''
        cb = (lambda a: Just(dict())) if data is None else data
        def io(i, body):
            return IO.delay(meth(self.client), '{}/{}{}'.format(self._type, i, sub), body=body)
        def assemble(i, a):
            return cb(a).io('invalid arguments') // L(io)(i, _)
        def check_error(response):
            if isinstance(response, dict) and 'error' in response:
                return IO.failed(response['error'])
            else:
                return IO.pure(response)
        return self.run(assemble) // check_error

    def get(self, data: Callable=None, path=Empty()):
        return self._req(_.get, path=path, data=data)

    def put(self, data: Callable=None, path=Empty()):
        return self._req(_.put, path=path, data=data)

    def post(self, data: Callable=None, path=Empty()):
        return self._req(_.post, path=path, data=data)

    @property
    def delete(self):
        return self._req(_.delete)

    def create(self, data: Callable=None, path=Empty()):
        cb = (lambda a: Just(dict())) if data is None else data
        sub = path / '/{}'.format | ''
        def assemble(path):
            return (cb(self.rest).io('invalid arguments') /
                    L(self.client.post)('{}{}'.format(path, sub), _))
        return self._data_path // assemble


def command_base(Cmd, param_desc, desc, **extra):
    def decor(func):
        func._doc = (param_desc, desc)
        @functools.wraps(func)
        def wrap(self, *args):
            cmd = Cmd(func.__name__, args, self.client, param_desc, desc,
                      **extra)
            return func(self, cmd).attempt
        return wrap
    return decor


def command(param_desc, desc):
    return command_base(Command, param_desc, desc)


class ApiClientMeta(abc.ABCMeta):

    def __new__(cls, name, bases, namespace) -> None:
        inst = super().__new__(cls, name, bases, namespace)  # type: ignore
        doc = ((name, fun._doc) for name, fun in namespace.items()
               if hasattr(fun, '_doc'))
        inst.doc = dict(doc)
        return inst


class ClientBase(Logging):

    @abc.abstractproperty
    def client(self):
        ...

    @command('', 'Display this help text')
    def help(self, cmd):
        if self.doc:
            maxlen = len(max(self.doc.keys(), key=len))
            pad = lambda s: s.ljust(maxlen)
            def output():
                yield 'Available commands:'
                data = List.wrap(self.doc.items()).sort_by(_[0])
                for name, (param_desc, desc) in data:
                    yield ''
                    yield '{}    {}'.format(pad(name), param_desc)
                    yield '  {}'.format(desc)
            return IO.delay(output) / '\n'.join
        else:
            return IO.failed('no doc for client')

__all__ = ['ApiClient']
