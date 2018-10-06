import os
import subprocess
import shutil
import re
import sys
from os import path
from itertools import filterfalse
from glob import glob

from tek import process_output, logger
from tek.tools import find, list_diff
from golgi.config import Config, ConfigClient, configurable
from golgi import cli
from tek.errors import MooException
from tek.user_input import SpecifiedChoice


class Extractor(object):
    suffixes = ['.part1', '.html']

    def __init__(self, program, extensions, common_switches=[],
                 extract_switches=[], destswitch=[],
                 list_switches=[], archive_switches=[]):
        self.program = program
        self.common_switches = common_switches
        self.extract_switches = extract_switches
        self.destswitch = destswitch
        self.list_switches = list_switches
        self.archive_switches = archive_switches
        self.extensions = extensions
        self.exitval = -1
        self.pipe = False
        self.output = []

    def process(self, archive, destdir, verbose=True):
        cmdline = [self.program] + self._extract_switches(archive, destdir)
        self._exec(cmdline, verbose)
        dirname = archive.path
        for suffix in self.suffixes:
            dirname = dirname.rsplit(suffix)[0]
        for ex in self.extensions:
            dirname = dirname.rsplit('.' + ex)[0]
        return path.basename(dirname)

    def list(self, archive, destdir, verbose=True):
        cmdline = [self.program] + self._list_switches(archive)
        self._exec(cmdline, verbose)

    def _exec(self, cmdline, verbose):
        if verbose:
            logger.info('executing {}'.format(' '.join(cmdline)))
        if self.pipe:
            stdout = stderr = subprocess.PIPE
        else:
            stdout, stderr = sys.stdout, sys.stderr
        proc = subprocess.Popen(cmdline, stdout=stdout, stderr=stderr)
        self.exitval = proc.wait()
        if self.pipe:
            self.output = proc.stdout.readlines()

    def _extract_switches(self, archive, destdir):
        return (self.common_switches + self.extract_switches +
                self._archive_switches(archive) + self._suffix_params(archive,
                                                                      destdir))

    def _list_switches(self, archive):
        return (self.common_switches + self.list_switches +
                self._archive_switches(archive))

    def _archive_switches(self, archive):
        return self.archive_switches + [archive.path]

    def _suffix_params(self, archive, destdir):
        return self.destswitch + [destdir]

    def set_password(self, *a, **kw):
        pass


@configurable(extract=['tar_switches'])
class TarExtractor(Extractor):

    def __init__(self, cryptoswitch=[], cryptoext=[]):
        Extractor.__init__(self, program='tar', extensions=['tar']+cryptoext,
                           extract_switches=['-x'],
                           common_switches=self._tar_switches+cryptoswitch,
                           destswitch=['-C'],
                           list_switches=['-t'],
                           archive_switches=['-f'])


class TarGzExtractor(TarExtractor):

    def __init__(self):
        TarExtractor.__init__(self, cryptoswitch=['-z'], cryptoext=['gz',
                                                                    'tgz'])


class TarBz2Extractor(TarExtractor):

    def __init__(self):
        TarExtractor.__init__(self, cryptoswitch=['-j'], cryptoext=['bz2',
                                                                    'tbz2'])


class TarXzExtractor(TarExtractor):

    def __init__(self):
        TarExtractor.__init__(self, cryptoswitch=['--xz'], cryptoext=['xz'])


@configurable(extract=['rar_switches'])
class RarExtractor(Extractor):

    def __init__(self):
        Extractor.__init__(self, program='unrar', extensions=['rar'],
                           extract_switches=['x'],
                           common_switches=self._rar_switches,
                           list_switches=['v'])

    def set_password(self, password):
        self.common_switches += ['-p-', '-p' + password]


class ZipExtractor(Extractor):

    def __init__(self):
        Extractor.__init__(self, program='unzip', extensions=['zip'],
                           destswitch=['-d'], list_switches=['-l'])


class SevenZExtractor(Extractor):

    def __init__(self):
        Extractor.__init__(self, program='7z', extensions=['7z'],
                           extract_switches=['x'], list_switches=['l'])

    def _suffix_params(self, archive, destdir):
        return ['-o' + destdir]


class PathError(MooException):
    pass


class MimeTypeError(MooException):

    def __init__(self, archive_type, extension):
        msg = "Unknown archive type \'{}\' with extension '{}'!"
        MooException.__init__(self, msg.format(archive_type, extension))


class Archive(object):
    """ simple struct for file path and archive type """

    def __init__(self, filepath, extractor):
        self.path = path.abspath(filepath)
        self.extractor = extractor
        self.missing_parts = None
        self.check_path()

    def __hash__(self):
        return hash(self.path)

    def check_path(self):
        if not path.exists(self.path):
            raise PathError('Source file "{}" not found!'.format(self.path))
        if path.isdir(self.path):
            msg = "Expected a filename, got a directory. ({})"
            raise PathError(msg.format(self.path))

    def __eq__(self, other):
        return isinstance(other, Archive) and self.path == other.path

    def extract(self, dest_dir=None, verbose=False):
        if dest_dir is None:
            dest_dir = os.getcwd()
        return self.extractor.process(self, dest_dir, verbose)

    def list(self, dest_dir, verbose=True):
        return self.extractor.list(self, dest_dir, verbose)

    def delete(self):
        os.remove(self.path)

    @property
    def size(self):
        return os.path.getsize(self.path)

    @property
    def complete(self):
        return True


class RarArchive(Archive):
    pass


class MultipartRarArchive(RarArchive):

    def __init__(self, archive, parts, extractor):
        rex = re.compile('.*\.part(\d+).rar')

        def enum(name):
            match = rex.match(name)
            return int(match.group(1)) if match else 1
        self._parts = parts
        self._enums = list(map(enum, parts))
        super(MultipartRarArchive, self).__init__(archive, extractor)
        max_enum = max(self._enums)
        self.missing_parts = list_diff(list(range(1, max_enum+1)), self._enums)

    @property
    def size(self):
        return sum(map(os.path.getsize, self._parts))

    def delete(self):
        for p in self._parts:
            try:
                os.remove(p)
            except IOError as e:
                logger.error(e)

    @property
    def complete(self):
        return not self.missing_parts


class ArchiveFactory(object):
    extractors = {
        'tar': TarExtractor,
        'gzip': TarGzExtractor,
        'bzip2': TarBz2Extractor,
        'rar': RarExtractor,
        'zip': ZipExtractor,
        'xz': TarXzExtractor,
        '7z': SevenZExtractor,
        '7z-compressed': SevenZExtractor,
    }

    def __init__(self, use_mime=True, use_extension=True, pipe=False):
        self._use_mime = use_mime
        self._use_extension = use_extension
        self._pipe = pipe

    def _archive_type(self, path):
        """ file returns a string formatted like application/x-gzip or
        application/zip choose second part and remove eventual leading
        'x-'
        """
        try:
            output = process_output(['file', '--mime-type', '-b', path])[0]
            mtype = output.split('/')[-1]
            if mtype.startswith('x-'):
                mtype = mtype[2:]
            return mtype
        except MooException as e:
            logger.error('Error while determining mime type: {}'.format(e))

    def _check_multipart(self, path):
        base = os.path.basename(path)
        dir = os.path.dirname(path)
        match = re.match('(.*)\.(part\d+)', base)
        is_multi = bool(match)
        if is_multi:
            name, part = list(map(match.group, (1, 2)))
            glub = os.path.join(dir, '{}.part*.rar'.format(name))
            parts = sorted(glob(glub))
            archive = parts[0]
        else:
            archive = path
            parts = None
        return is_multi, archive, parts

    def archive(self, path):
        extension = path.rsplit('.')[-1]
        _type = self._archive_type(path)
        if self._use_mime:
            self._use_mime = _type in self.extractors
            Extractor = self.extractors.get(_type, None)
        if not self._use_mime and self._use_extension:
            Extractor = find(lambda e: extension in e().extensions,
                             list(self.extractors.values()))
        if not Extractor:
            raise MimeTypeError(_type, extension)
        extractor = Extractor()
        if isinstance(extractor, RarExtractor):
            is_multi, archive, parts = self._check_multipart(path)
            if is_multi:
                archive = MultipartRarArchive(archive, parts, extractor)
            else:
                archive = RarArchive(path, extractor)
        else:
            archive = Archive(path, extractor)
        extractor.pipe = self._pipe
        return archive


class ArchiveActionNotSupported(MooException):
    msg = 'Unsupported action for {}: {}'

    def __init__(self, action, _type=None):
        if _type is None:
            target = 'ExtractJob'
        msg = self.msg.format(target, action)
        super(ArchiveActionNotSupported, self).__init__(msg)


class ExtractJob(object):
    actions = ['extract', 'list']

    def __init__(self, archive_path, action='extract', dest_dir=os.getcwd(),
                 use_temp_dir=True, use_mime=True, use_extension=True,
                 verbose=True, password=None, pipe=False):
        if action not in self.actions:
            raise ArchiveActionNotSupported(action)
        else:
            self.action = action
            self._action = getattr(self, action)
        self.verbose = verbose
        self._password = password
        self.archive = ArchiveFactory(use_mime=use_mime,
                                      use_extension=use_extension,
                                      pipe=pipe).archive(archive_path)
        self.extractor = self.archive.extractor
        self.dest_dir = path.abspath(dest_dir)
        self.use_temp_dir = use_temp_dir
        self._prepare()

    def __hash__(self):
        return hash(self.archive)

    def __eq__(self, other):
        return isinstance(other, ExtractJob) and self.archive == other.archive

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.archive.path)

    def _prepare(self):
        if self.action in ['extract']:
            self.check_dest_dir()
            if self.use_temp_dir:
                self.determine_temp_dir_name()
                self.exdir = self.temp_dir
            else:
                self.exdir = self.dest_dir

    def check_dest_dir(self):
        if path.isfile(self.dest_dir):
            raise PathError("Destination is a regular file!")
        if not path.isdir(self.dest_dir):
            os.makedirs(self.dest_dir)

    def determine_temp_dir_name(self):
        temp_dir = path.join(self.dest_dir, 'extract_temp')
        check_dir = temp_dir
        i = 0
        while path.lexists(check_dir):
            check_dir = temp_dir + str(i)
            i += 1
        self.temp_dir = check_dir

    def create_temp_dir(self):
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)

    def process(self):
        self._action()

    def extract(self):
        """ extract the archive.
        @returns: the target location
        """
        self._process_password_param()
        if self.use_temp_dir:
            self.create_temp_dir()
        self.dir_name = self.archive.extract(self.exdir, self.verbose)
        self.move_dest = self.exdir
        if self.use_temp_dir:
            self.determine_move_dirs()
            try:
                self.check_destination_dir()
                self.move_to_dest_dir()
            except PathError as e:
                logger.error('Error while extracting: {}'.format(e))
            self.cleanup()
        return self.move_dest

    def list(self):
        self.archive.list(self.verbose)

    def _process_password_param(self):
        conf = ConfigClient('extract')
        passwords = conf('passwords')
        if self._password is None:
            global_pass = global_password()
            if global_pass is not None:
                self._password = global_pass
            elif conf('ask_password') and passwords:
                text = ['Choose a password for {}:'.format(self.archive.path)]
                self._password = SpecifiedChoice(passwords,
                                                 text_pre=text).read()
        if self._password is not None:
            self.extractor.set_password(self._password)

    def determine_move_dirs(self):
        self.move_source = self.temp_dir
        content = os.listdir(self.move_source)
        single_file = False
        files_in_root = True
        while len(content) == 1 and not single_file:
            files_in_root = False
            root_dir = content[0]
            self.move_source = path.join(self.move_source, root_dir)
            if not path.isdir(self.move_source):
                single_file = True
            else:
                content = os.listdir(self.move_source)
        if files_in_root:
            self.move_dest = path.join(self.dest_dir, self.dir_name)
        else:
            self.move_dest = path.join(self.dest_dir, root_dir)

    def check_destination_dir(self):
        if path.exists(self.move_dest):
            msg = 'Destination path \'{}\' already exists!'
            raise PathError(msg.format(self.move_dest))

    def move_to_dest_dir(self):
        try:
            shutil.move(self.move_source, self.move_dest)
            if self.verbose:
                logger.info('extracted archive to {}.'.format(self.move_dest))
        except Exception as e:
            logger.error(e)
            msg = 'Moving the extracted data to \'{}\' failed.'
            raise PathError(msg.format(self.move_dest.decode('utf-8')))

    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.debug('Error while cleaning up: {}'.format(e))

    @property
    def exitval(self):
        return self.extractor.exitval

_global_pw = None


def global_password():
    global _global_pw
    if _global_pw is None:
        passwords = Config['extract'].passwords
        password = Config['extract'].password
        if password is not None:
            _global_pw = password
        elif Config['extract'].global_password and passwords:
            text = ['Choose a password:']
            _global_pw = SpecifiedChoice(passwords, text_pre=text).read()
    return _global_pw


def extract_files(files, destdir):
    password = global_password()
    tempdir = Config['extract'].temp
    action = 'list' if Config['extract'].list else 'extract'
    for _path in files:
        try:
            job = ExtractJob(_path, dest_dir=destdir, use_temp_dir=tempdir,
                             password=password, action=action)
            yield job.process()
        except (PathError, MimeTypeError) as e:
            logger.error('Error while extracting files: {}'.format(e))


@cli(positional=('archive', '+'))
def extract():
    args = Config['extract'].archive
    files = filterfalse(os.path.isdir, args)
    try:
        destdir = next(filter(os.path.isdir, args))
    except StopIteration:
        destdir = os.getcwd()
    return list(extract_files(files, destdir))
