import amino.logging
from amino.logging import amino_logger
from amino.lazy import lazy

log = series_root_logger = amino_logger('series')


def series_logger(name: str):
    return series_root_logger.getChild(name)


class Logging(amino.logging.Logging):

    @lazy
    def _log(self) -> amino.logging.Logger:  # type: ignore
        return series_logger(self.__class__.__name__)

__all__ = ('series_logger', 'Logging')
