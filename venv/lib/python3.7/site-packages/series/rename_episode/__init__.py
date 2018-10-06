import shutil, os
from os import path

from series.logging import series_logger
from tek.user_input import YesNo
from tek.tools import listdir_abs, ymap

from series import episode_metadata
from series.errors import SeriesException

log = series_logger('rename')

class EpisodeEnumerationError(SeriesException):
    def __init__(self, filename):
        text = "Couldn't find enumeration: %s" % filename
        TException.__init__(self, text)

def make_identifier(se):
    return 'x'.join(str(s).zfill(2) for s in se)

def rename(filename, series_name=None, season_name=None):
    ext = filename.rsplit('.', 1)[-1]
    _series_name, _season_name, _number = episode_metadata(filename)
    name = series_name or _series_name
    season = season_name or _season_name
    identifier = make_identifier((season, _number))
    return '%s_%s.%s' % (name, identifier, ext.lower())

def move_path(filepath, series_name=None, force=False):
    filename = path.basename(filepath)
    new_name = rename(filename, series_name)
    if not new_name:
        return None
        log.warning('%s cannot be renamed' % filename)
    else:
        return new_name

def move(filepath, series_name=None, force=False):
    if not path.exists(filepath):
        raise IOError('File not found: ' + filepath)
    dir = path.dirname(filepath)
    new_name = move_path(filepath, series_name, force)
    new_path = os.path.join(dir, new_name)
    exists = path.exists(new_path)
    prompt = '%s "%s"?' % (('Overwrite' if exists else 'Move to'), new_name)
    if exists and not force:
        log.info('File exists: ' + new_name)
    elif YesNo(prompt).read():
        shutil.move(filepath, new_path)

def move_description(job, exists, maxlen):
    s = job[0].ljust(maxlen) + '  =>  ' + job[1]
    if exists:
        s += ' (exists)'
    return s

def fix_all(dir='.', series_name=None):
    jobs = []
    files_abs = list(filter(path.isfile, listdir_abs(dir)))
    subs = path.join(dir, 'sub')
    if path.isdir(subs):
        files_abs.extend(list(filter(path.isfile, listdir_abs(subs))))
    files = list(map(os.path.basename, files_abs))
    dests = ymap(move_path, files, series_name)
    jobs = list(zip(files, dests, files_abs))
    jobs = [s_d_ig for s_d_ig in jobs if s_d_ig[1] is not None and s_d_ig[0] != s_d_ig[1]]
    if jobs:
        maxlen = max(len(j[0]) for j in jobs)
        exists = lambda f: os.path.isfile(os.path.join(dir, f))
        strings = [move_description(job, exists(job[1]), maxlen) for job in
                   jobs]
        log.info(strings)
        if YesNo(['Execute?']).read():
            for source, dest, source_abs in jobs:
                base = os.path.dirname(source_abs)
                shutil.move(source_abs, os.path.join(base, dest))

__all__ = ('find_episode_enumeration', 'make_series_name',
           'make_identifier', 'rename', 'move', 'fix_all',
           'EpisodeEnumerationError')
