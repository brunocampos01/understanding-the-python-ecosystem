"""
Best Practices: except clause
When inside an except clause, you might want to, for example, log that a specific type of error happened, and then re-raise. The best way to do this while preserving the stack trace is to use a bare raise statement. For example:
"""
from pip.utils import logging


logger = logging.getLogger(__name__)


def do_something_in_app_that_breaks_easily():
    pass


try:
    do_something_in_app_that_breaks_easily()
except AppError as error:
    logger.error(error)
    raise                 # just this!
    # raise AppError      # Don't do this, you'll lose the stack trace!
