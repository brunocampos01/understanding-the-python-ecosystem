class LinkStatus(object):

    def __init__(self, response):
        self._result = response.get('result', '')
        self._status = response.get('status', '')

    @property
    def status(self):
        return self._status.lower()

    @property
    def result(self):
        return self._result.lower()

    @property
    def success(self):
        return self.result == 'success'

    @property
    def dead(self):
        return self.status == 'dead'

    @property
    def error(self):
        return self.dead

    @property
    def unknown(self):
        return self.status == 'unknown'

    @property
    def working(self):
        return self.status == 'working'

    def __str__(self):
        return '{}: {} ({})'.format(self.__class__.__name__, self._result,
                                    self._status)


class UnknownStatus(LinkStatus):

    def __init__(self):
        super(UnknownStatus, self).__init__(dict(status='unknown'))

__all__ = ['LinkStatus']
