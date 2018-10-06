import amino.logging
from amino.logging import amino_logger
from amino.lazy import lazy

log = golgi_root_logger = amino_logger('golgi')


def golgi_logger(name: str):
    return golgi_root_logger.getChild(name)


class Logging(amino.logging.Logging):

    @lazy
    def _log(self) -> amino.logging.Logger:  # type: ignore
        return golgi_logger(self.__class__.__name__)

__all__ = ('golgi_logger', 'Logging')
