import random
import string


class Random(object):
    _char_pool = string.ascii_uppercase + string.digits

    @staticmethod
    def string(n=10):
        return ''.join(random.choice(Random._char_pool) for _ in range(n))

__all__ = ('Random',)
