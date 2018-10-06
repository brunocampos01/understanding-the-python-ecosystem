#!/usr/bin/env python

import os
import fnmatch
from os import path

from golgi import process, cli, Config

mp3gain = '/usr/bin/mp3gain'
vorbisgain = '/usr/bin/vorbisgain'
metaflac = '/usr/bin/metaflac'

# mp3gain maybe uses 83 dB, vorbisgain 89 dB as a reference
mp3gainflags = ['-p', '-c', '-f', '-a']
vorbisgainflags = ['-a', '-f', '-s']
metaflacflags = ['--add-replay-gain']


@cli
def gain_collection(collection_path=None):
    if collection_path is None:
        collection_path = path.expanduser(Config['music'].collection_dir)
    gain(collection_path)


def gain(rootdir):
    """ Search for subdirs containing music files, gaining each as an
    album.

    """
    for root, dirs, files in os.walk(rootdir):
        oggs = fnmatch.filter(files, '*.ogg')
        mp3s = fnmatch.filter(files, '*.mp3')
        flacs = fnmatch.filter(files, '*.flac')
        if oggs:
            gain_cmd, flags, files = vorbisgain, vorbisgainflags, oggs
        elif mp3s:
            gain_cmd, flags, files = mp3gain, mp3gainflags, mp3s
        elif flacs:
            gain_cmd, flags, files = metaflac, metaflacflags, flacs
        else:
            continue
        paths = [path.join(root, f) for f in files]
        process(['nice', '-n18', gain_cmd] + flags + paths, True, False)
