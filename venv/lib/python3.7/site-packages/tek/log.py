import logging
import os
import sys

from tek.util.debug import dodebug

logger = logging.getLogger('tek')
logger.setLevel(logging.INFO)
stdouthandler = logging.StreamHandler(sys.stdout)
stdouthandler.setLevel(logging.INFO)
logger.addHandler(stdouthandler)
if dodebug:
    logger.setLevel(logging.DEBUG)
    stdouthandler.setLevel(logging.DEBUG)
if 'TEK_PYTHON_FILE_LOGGING' in os.environ:
    try:
        handler = logging.FileHandler(os.path.expanduser('~/.python/log'))
        logger.addHandler(handler)
        if dodebug:
            handler.setLevel(logging.DEBUG)
    except IOError:
        pass

if dodebug and 'TEK_PYTHON_DEBUG_LOGGING' in os.environ:
    debug_logger = logger.getChild('debug')
    debug_logger.setLevel(logging.DEBUG)
    try:
        handler = logging.FileHandler(os.path.expanduser('~/.python/debug'))
        debug_logger.addHandler(handler)
        handler.setLevel(logging.DEBUG)
    except IOError:
        pass
    debug = debug_logger.debug
else:
    debug = lambda *a, **kw: True
