import threading
from functools import wraps

import requests
from requests.exceptions import RequestException

from flask import Flask, jsonify, request

from golgi import configurable

from series.logging import Logging


def json_response(func):
    @wraps(func)
    def wrapper(*a, **kw):
        response = func(*a, **kw)
        if isinstance(response, tuple):
            rest = response[1:]
            response = response[0]
        elif response is None:
            rest = ()
            response = {}
        else:
            rest = ()
        return (jsonify(dict(response=response)),) + rest
    return wrapper


def route_decorator():
    routes = {}

    def _route(path, **kwargs):
        def add_route(func):
            configs = routes.setdefault(func.__name__, [])
            configs.append((path, kwargs,))
            return func
        return add_route
    return routes, _route


@configurable(general=['debug'])
class RestApi(threading.Thread, Logging):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.app = Flask(__name__)
        if self._debug:
            self.app.config['TESTING'] = True

    def run(self):
        self.log.info('Starting REST API.')
        self.setup_routes()
        try:
            self.app.run(host=self._rest_api_host, port=self._rest_api_port)
        except OSError as e:
            self.log.error('''Couldn't start REST API: {}'''.format(e))

    def _shutdown(self):
        func = request.environ.get('werkzeug.server.shutdown')
        func()
        return 'server shut down.'

    def stop(self):
        self.app.add_url_rule('/shutdown', 'shutdown', self._shutdown,
                              methods=['PUT'])
        uri = 'http://localhost:{}/shutdown'.format(self._rest_api_port)
        try:
            requests.put(uri)
        except RequestException as e:
            self.log.debug('api shutdown request failed: {}'.format(e))

    def setup_routes(self):
        for name, configs in self.routes.items():
            for index, config in enumerate(configs):
                path, kwargs = config
                func = getattr(self, name)
                self.app.add_url_rule(path, name + str(index),
                                      json_response(func), **kwargs)

__all__ = ['RestApi', 'route_decorator']
