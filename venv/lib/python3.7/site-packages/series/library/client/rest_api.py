from golgi.config import configurable
from series.logging import Logging

from amino import IO

from series.api_client import ClientBase, ApiClientMeta, command, ApiClient


@configurable(library_client=['rest_api_port', 'rest_api_url'])
class LibClient(ClientBase, metaclass=ApiClientMeta):

    @property
    def client(self):
        return ApiClient(self._rest_api_url, self._rest_api_port)

    @command('series season episode', 'Create an episode with the supplied metadata')
    def create_episode(self, cmd):
        series, season, episode = cmd.args
        data = dict(episode=episode)
        path = 'series/{}/seasons/{}/episodes'.format(series, season)
        return IO.delay(self.client.post, path, body=data)

    @command('series season episode subfps', 'Set the episode\'s subfps')
    def subfps(self, cmd):
        series, season, episode, subfps = cmd.args
        data = dict(subfps=subfps)
        path = 'series/{}/seasons/{}/episodes/{}'.format(series, season,
                                                         episode)
        return IO.delay(self.client.put, path, body=data)

__all__ = ('LibClient',)
