from series.handler import Handler

class BaseHandler(Handler):

    def __init__(self, data, interval, description, **kw):
        self._data = data
        super().__init__(interval, description, **kw)

    @property
    def _lock(self):
        return self._data.lock

__all__ = ['BaseHandler']
