import os
from itertools import filterfalse, chain

from golgi import logger, cli, Config

from tek import logger

from tek_utils.extract import extract_files
from tek_utils.gain import gain
from mootag.handler import handle
from mootag.store import Album
from mootag.util.path import music_dirs


@cli(positional=('album', '+'))
def process_album():
    tempdir = Config['process_album'].music_tempdir
    args = Config['process_album'].album
    albums = chain(filter(os.path.isdir, args),
                   extract_files(filterfalse(os.path.isdir, args), tempdir))

    def _dirs():
        for album in map(music_dirs, albums):
            for dir in album:
                os.chmod(dir, 0o755)
                for file in os.listdir(dir):
                    file = os.path.join(dir, file)
                    if os.path.isfile(file):
                        os.chmod(file, 0o644)
                yield dir

    def handled_albums():
        for dir in _dirs():
            try:
                handle(dir)
                yield dir
            except Exception as e:
                logger.error('Error handling album %s:' % dir)
                logger.error(e)

    def stored_dirs():
        for path in handled_albums():
            try:
                yield Album(path).store()
            except Exception as e:
                logger.error(e)
    for dir in stored_dirs():
        gain(dir)
