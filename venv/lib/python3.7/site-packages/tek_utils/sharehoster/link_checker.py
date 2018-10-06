import requests

from golgi.config import configurable
from tek.tools import resolve_redirect
from tek import logger

from tek_utils.sharehoster.models.link_status import LinkStatus
from tek_utils.sharehoster.errors import InvalidURLError


@configurable(sharehoster=['link_checker_url'])
class LinkChecker(object):

    def __init__(self, minimum_size=None):
        pass

    def query(self, url):
        data = dict(response_format='json', link=url)
        response = {}
        try:
            request = requests.post(self._link_checker_url, data=data,
                                    timeout=5)
        except requests.RequestException as e:
            logger.error('Error querying url checker for {}: {}'.format(url,
                                                                        e))
        else:
            if isinstance(request.json(), dict):
                response = request.json()
            request.connection.close()
        return LinkStatus(response)

    def check(self, url):
        valid = True
        status = LinkStatus(dict(status='failed',
                                 result='unable to query link checker'))
        if self._link_checker_url:
            try:
                status = self.query(url)
                if not status.success:
                    url = resolve_redirect(url)
                    status = self.query(url)
            except ValueError as e:
                logger.error('Error checking url {}: {}'.format(url, e))
                valid = True
            except requests.RequestException:
                raise InvalidURLError('couldn\'t connect')
            else:
                valid = status.success and not status.error
        return valid, status

__all__ = ['LinkChecker']
