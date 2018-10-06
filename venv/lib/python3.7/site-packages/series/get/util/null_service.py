class NullService(object):

    def __init__(self, *a, **kw):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass

    def is_alive(self):
        return False

__all__ = []
