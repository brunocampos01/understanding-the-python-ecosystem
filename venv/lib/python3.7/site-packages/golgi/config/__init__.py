import re
import os
import configparser
import importlib
import copy

from amino.util.string import camelcaseify
from amino.lazy import lazy

from golgi.config.errors import (NoSuchSectionError, NoSuchOptionError,
                                 ConfigClientNotYetConnectedError,
                                 ConfigLoadError)
from golgi.logging import Logging, golgi_logger
from golgi.config.options import (ListConfigOption, UnicodeConfigOption,
                                  PathConfigOption, PathListConfigOption,
                                  FileSizeConfigOption, IntConfigOption,
                                  FloatConfigOption, DictConfigOption,
                                  ConfigOption, TypedConfigOption,
                                  BoolConfigOption)
from golgi.config.errors import ConfigError


class ConfigDict(dict):
    ''' Dictionary that respects TypedConfigOptions when getting or
    setting.
    '''

    def getitem(self, key):
        ''' special method that is used in Configuration objects.
        Return the content of the TypedConfigOption wrapper, if it is
        present.
        '''
        value = self[key]
        if isinstance(value, TypedConfigOption):
            value = value.effective_value
        return value

    def __setitem__(self, key, value):
        ''' TypedConfigOption instances get special treatment:
            If one would be overwritten, call its set() method instead.
            If the new value also is a TypedConfigOption, pass its value
            to set().
            If the key is new, try to create a TypedConfigOption.
        '''
        if key not in self:
            if not (isinstance(value, str) or
                    isinstance(value, TypedConfigOption) or
                    value is None):
                try:
                    name = value.__class__.__name__
                    typ = eval(camelcaseify(name) + 'ConfigOption')
                except NameError:
                    value = TypedConfigOption(type(value), value)
                else:
                    value = typ(value)
            dict.__setitem__(self, key, value)
        else:
            if isinstance(self[key], TypedConfigOption):
                if isinstance(value, TypedConfigOption):
                    self[key].set_from_co(value)
                else:
                    self[key].set(value)
            else:
                dict.__setitem__(self, key, value)

    def update(self, newdict):
        ''' Convenience overload. '''
        for key, value in dict(newdict).items():
            self[key] = value


class Configuration(object):
    ''' Container for several dictionaries representing configuration
    options from various sources:
    - The defaults, to be set from a Configurations.register_config call
    - The file config, read from all files given in a call to
      Configurations.register_files
    - The command line options, passed by a CLIConfig object through
      Configurations.set_cli_config
    - Values set by Configurations.override, mainly for testing purposes
    It can be used from ConfigClient subclasses or instances to
    obtain the value to a config key, where the precedence is
    overridden->cli->files->defaults.
    Different section names can be used for groups of options from the
    register_config call, which correspond to the section names from the
    files.
    '''

    def __init__(self, defaults):
        ''' Initialize the dicts used to store the config and the list
        of section names that are added for defaults.
        '''
        self.config_defaults = ConfigDict()
        self.config_from_file = dict()
        self.config_from_cli = ConfigDict()
        self.overridden = ConfigDict()
        self.config = ConfigDict()
        self.set_defaults(defaults)

    def __getitem__(self, key):
        ''' Emulate read-only container behaviour. '''
        if key not in self.config:
            raise NoSuchOptionError(key)
        return self.config.getitem(key)

    def __str__(self):
        return str(self.config)

    def __repr__(self):
        return repr(self.config)

    def has_key(self, key):
        ''' Emulate read-only container behaviour. '''
        return key in self.config

    @property
    def info(self):
        ''' Return the contents of all sources. '''
        s = 'Defaults: %s\nCLI: %s\nFiles: %s' % (str(self.config_defaults),
                                                  str(self.config_from_cli),
                                                  str(self.config_from_file))
        return s

    def __rebuild_config(self):
        ''' Collect the config options from the defaults, the file
        config sections that have been default-added and the cli
        config in that order and store them in self.config.
        The defaults and file config sections are iterated in the
        order of the additions of the defaults.
        To be called after new values are added.
        '''
        self.config = ConfigDict()
        self.config.update(self.config_defaults)
        self.config.update(self.config_from_file)
        self.config.update(self.config_from_cli)
        self.config.update(self.overridden)

    def config_update(f):
        def wrap(self, *a, **kw):
            f(self, *a, **kw)
            self.__rebuild_config()
        return wrap

    @config_update
    def set_defaults(self, new_defaults):
        ''' Add a new unique section with default values to the list of
        default options.
        '''
        self.config_defaults.update(new_defaults)

    @config_update
    def set_cli_config(self, values):
        ''' Set the config values read from command line invocation.
            @param values: Obtained from an instance of OptionParser.
            Its __dict__ contains all of the possible command line
            options. If an option hasn't been supplied, it is None, and
            thus not considered here.
            @type values: optparse.Values
        '''
        self.config_from_cli.update([key, value] for key, value in
                                    values.__dict__.items()
                                    if value is not None and
                                    key in self.config_defaults)

    @config_update
    def set_file_config(self, file_config):
        ''' Add the values obtained from the files as a ConfigDict
        object and rebuild the main config.
        '''
        self.config_from_file = ConfigDict()
        self.config_from_file.update(file_config)

    @config_update
    def override(self, **values):
        self.overridden.update(values)

    def config_from_section(self, section, key):
        ''' Obtain the value that key has in the specific section,
        in the order file->default.
        '''
        if not self.has_section(section):
            raise NoSuchSectionError(section)
        elif (section in self.config_from_file and key in
              self.config_from_file[section]):
            return self.config_from_file[section][key]
        elif key not in self.config_defaults[section]:
            raise NoSuchOptionError(key)
        else:
            return self.config_defaults[section][key]

    def has_section(self, name):
        ''' Return True if a section with name has been added. '''
        return name in self.sections


class ConfigClient(Logging):
    ''' Standard read-only proxy for a Configuration. '''
    def __init__(self, name):
        ''' Connect to the Configuration called name. '''
        self.connected = False
        self._config = None
        self.__register(name)

    def __register(self, name):
        ''' Add self to the list of instances waiting for the
        Configuration in the Configurations proxy.
        '''
        self.name = name
        Configurations.register_client(self)

    def config(self, key):
        ''' Obtain a config option's value. '''
        if self._config is None:
            raise ConfigClientNotYetConnectedError(self.name, key)
        return self._config[key]

    def __call__(self, key):
        return self.config(key)

    def print_all(self):
        self.log.info(self._config.info)

    def connect(self, config):
        ''' Reference the Configuration instance as the config to be
        used by the client. Called from Configurations once the
        Configuration is ready.
        Mark as connected, so that the config isn't switched.
        '''
        if self._config is None:
            self._config = config


class ConfigurationFactory(Logging):
    ''' Construct Configuration objects out of a section of the given
    config files.
    '''

    def __init__(self, allow_files=True):
        self.files = []
        self.config_parser = configparser.ConfigParser()
        self._allow_files = allow_files

    def add_files(self, files):
        self.files += files
        self.read_config()

    def read_config(self):
        self.config_parser.read(self.files)

    def create(self, section, defaults):
        config = Configuration(defaults)
        if self._allow_files:
            try:
                file_config = dict(self.config_parser.items(section))
                config.set_file_config(file_config)
            except configparser.NoSectionError as e:
                self.log.debug('configparser: ' + str(e))
            except configparser.Error as e:
                self.log.error('configparser: ' + str(e))
        return config


class ConfigProxy(object):

    def __init__(self, config):
        self._config = config

    def __str__(self):
        return str(self._config)

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        return self._config[key]


class ConfigMeta(type):

    def __str__(self):
        return str(self._configs)

    def __getitem__(self, section):
        if section not in self._configs:
            raise NoSuchSectionError(section)
        return ConfigProxy(self._configs[section])


class Configurations(metaclass=ConfigMeta):
    ''' Program-wide register of Configuration instances.
    Connects the clients to the according Configuration, as soon as it
    has registered.
    '''
    # A dict of configuration factories by an alias name
    _factories = {}
    # A dict of Configuration instances by their section name
    _configs = {}
    _cli_config = None
    # A mapping of config keys to -x cli short option characters
    _cli_short_options = {}
    _cli_params = {}
    # A dict of lists of client instances grouped by the name of the
    # target Configuration's name
    _pending_clients = {}
    # classes that have attributes set from configurable decorator
    _configurables = set()
    # read config from file system
    allow_files = True
    allow_override = True
    default_metadata = dict(parents=[], std_files=True, files=[])
    metadata = {}
    log = golgi_logger('configurations')

    @classmethod
    def create_alias(cls, alias):
        if alias not in cls._factories:
            cls._factories[alias] = ConfigurationFactory(cls.allow_files)

    @classmethod
    def register_files(cls, alias, *files):
        cls.create_alias(alias)
        files = [os.path.abspath(os.path.expanduser(f)) for f in files]
        cls._factories[alias].add_files(files)

    @classmethod
    def register_config(cls, file_alias, section, **defaults):
        ''' Add a Configuration instance to the configs dict that
        contains the specified section of the files denoted by the
        specified alias and connect waiting client instances.
        If register_files wasn't called with this alias before, it is
        created now.
        '''
        cls.create_alias(file_alias)
        if section not in cls._configs:
            config = cls._factories[file_alias].create(section, defaults)
            if cls._cli_config:
                config.set_cli_config(cls._cli_config)
            cls._configs[section] = config
            cls.notify_clients(section)
        else:
            cls._configs[section].set_defaults(defaults)

    @classmethod
    def set_cli_config(cls, values):
        cls._cli_config = values
        for config in list(cls._configs.values()):
            config.set_cli_config(values)
        cls.notify_all_clients()

    @classmethod
    def register_client(cls, client):
        ''' Connect a client instance to the according Configuration
        instance, buffering the request if neccessary.
        '''
        try:
            client.connect(cls._configs[client.name])
        except KeyError:
            if client.name not in cls._pending_clients:
                cls._pending_clients[client.name] = []
            cls._pending_clients[client.name].append(client)

    @classmethod
    def notify_all_clients(cls):
        for name in list(cls._pending_clients.keys()):
            cls.notify_clients(name)

    @classmethod
    def notify_clients(self, name):
        ''' Connects clients to Configuration 'name' that have been
        registered before their target and clear the client dict item.
        '''
        if name in self._configs:
            if name in self._pending_clients:
                for client in self._pending_clients[name]:
                    client.connect(self._configs[name])
                del self._pending_clients[name]
        else:
            msg = ('Configurations.notify clients called for Configuration' +
                   '\'{}\' which hasn\'t been added yet')
            self.log.debug(msg.format(name))

    @classmethod
    def override_defaults(self, section, **defaults):
        if self.allow_override:
            if section in self._configs:
                self._configs[section].set_defaults(defaults)
            else:
                m = 'Tried to override defaults in nonexistent section \'{}\''
                self.log.debug(m.format(section))

    @classmethod
    def override(self, section, **values):
        if self.allow_override:
            if section in self._configs:
                self._configs[section].override(**values)
            else:
                msg = 'Tried to override values in nonexistent section \'{}\''
                self.log.debug(msg.format(section))

    @classmethod
    def parse_cli(self, positional=()):
        ''' Add positional parameters, then define options and switches
        based on the config. Parse command line parameters and set
        optional positionals to None that haven't been specified at cli.
        Write parsed options to config.
        '''
        from argparse import ArgumentParser
        parser = ArgumentParser()
        seen = []

        def positional_not_as_tuple():
            ''' backwards compatibility for parameter positional.
            Previously, only one positional argument was possible.
            '''
            return (isinstance(positional, (tuple, list)) and positional and
                    not isinstance(positional[0], (tuple, list)))
        if positional_not_as_tuple():
            positional = (positional,)
        for pos_arg in positional:
            parser.add_argument(pos_arg[0], nargs=pos_arg[1])

        def is_not_positional(name, value):
            ''' Check if either the config defines this value as
            positional or the caller requested the parameter of that
            name as positional
            '''
            return (not
                    (isinstance(value, ConfigOption) and value.positional) and
                    (positional is None or not
                     any(p[0] == name for p in positional)
                     ))

        def add_option(name, value):
            arg = ['']
            params = {}

            def add():
                parser.add_argument(*arg, **params)
            switchname = name.replace('_', '-')
            arg = ['--%s' % switchname]
            params = {'default': None}
            if name in self._cli_short_options:
                arg.append('-%s' % self._cli_short_options[name])
            if name in self._cli_params:
                params.update(self._cli_params[name])
            if isinstance(value, ConfigOption):
                params.update(value.argparse_params)
                if value.short:
                    arg.append('-%s' % value.short)
            if isinstance(value, BoolConfigOption):
                params['action'] = 'store_true'
                if value.no:
                    add()
                    params = {'default': None}
                    arg = ['--no-%s' % switchname]
                    if value.no_switch is not None:
                        arg.append(value.no_switch)
                    params['action'] = 'store_false'
                    params['dest'] = name
            add()
        for config in self._configs.values():
            for name, value in config.config.items():
                if name in seen:
                    continue
                seen.append(name)
                if is_not_positional(name, value):
                    add_option(name, value)
        args = parser.parse_args()
        for pos_arg in positional:
            if pos_arg is not None and not getattr(args, pos_arg[0]):
                setattr(args, pos_arg[0], None)
        self.set_cli_config(args)

    @classmethod
    def set_cli_short_options(self, **options):
        self._cli_short_options.update(options)

    @classmethod
    def set_cli_params(self, name, *short, **params):
        if short:
            self.set_cli_short_options(dict([[name, short[0]]]))
        self._cli_params[name] = params

    @classmethod
    def clear(self):
        self._configs = {}
        self._cli_config = None
        self._pending_clients = {}
        self._factories = {}
        for cls in self._configurables:
            if hasattr(cls, '__conf_init__'):
                cls.__init__ = cls.__conf_init__

    @classmethod
    def clear_configs(self):
        self.clear()

    @classmethod
    def clear_metadata(self):
        self.metadata = {}

    @classmethod
    def add_configurable(self, cls):
        self._configurables.add(cls)

    @classmethod
    def write_config(self, filename):
        def write_section(f, section, config):
            f.write('[{0:s}]\n'.format(section))
            for key, value in config.config.items():
                if not (isinstance(value, ConfigOption) and value.positional):
                    if isinstance(value, ConfigOption) and value.help:
                        f.write('\n# {0:s}\n'.format(value.help))
                    if value is None:
                        value = ''
                    f.write('# {0:s} = {1:s}\n'.format(key, str(value)))
            f.write('\n')
        with filename.open('w') as f:
            if 'global' in self._configs:
                write_section(f, 'global', self._configs['global'])
            for section, config in self._configs.items():
                if not section == 'global':
                    write_section(f, section, config)

    @classmethod
    def load_config(self, name):
        if name not in self.metadata:
            self._load_config(name)

    @classmethod
    def _load_config(self, name):
        try:
            module = importlib.import_module('{}.config'.format(name))
        except ImportError as e:
            text = 'Could not import config {}!'
            raise ConfigLoadError(text.format(name)) from e
        metadata = copy.deepcopy(self.default_metadata)
        metadata.update(getattr(module, 'metadata', {}))
        func = getattr(module, 'reset_config', None)
        if func is None:
            text = 'Missing reset_config function for {}!'
            raise ConfigLoadError(text.format(name))
        self.metadata[name] = metadata
        self.metadata[name]['func'] = func
        self.metadata[name]['name'] = name
        metadata.setdefault('alias', name.split('.')[0])
        self.load_dependencies(name)

    @classmethod
    def load_dependencies(self, name):
        for dep in self.metadata[name]['parents']:
            self.load_config(dep)

    @classmethod
    def setup(self, *names, files=True):
        self.clear_metadata()
        for name in names:
            self.load_config(name)
        self.reset(files)

    @classmethod
    def reset(self, files=True, alias=None):
        self.clear_configs()
        for metadata in self.order_dependencies(alias):
            self.auto_setup_alias(metadata, files)
            config = metadata['func']()
            if config:
                self.auto_setup_configs(metadata, config)

    @classmethod
    def auto_setup_alias(self, metadata, add_files):
        alias = metadata['alias']
        files = []
        if add_files:
            files.extend(metadata['files'])
            if metadata['std_files']:
                files.extend(standard_config_files(alias))
        self.register_files(alias, *files)

    @classmethod
    def auto_setup_configs(self, metadata, config):
        for section, defaults in config.items():
            self.register_config(metadata['alias'], section, **defaults)

    @classmethod
    def order_dependencies(self, alias=None):
        pending = [name for name, m in self.metadata.items()
                   if alias is None or m['alias'] in alias]

        def resolved(key):
            parents = self.metadata[key]['parents']
            return not parents or not any(p in pending for p in parents)
        while pending:
            none_found = True
            for name in pending:
                if resolved(name):
                    yield self.metadata[name]
                    pending.remove(name)
                    pending = [n for n in pending if n != name]
                    none_found = False
            if none_found:
                text = 'Circular dependencies for keys: {}!'
                raise ConfigLoadError(text.format(pending))

Config = Configurations

conf_attr_re = re.compile(r'_((?P<section>.+)__)?(?P<key>.+)')


def _add_conf_property(cls, section, key):
    ''' Binds two lazy properties to cls: _key and _section__key.
    Upon first access, those properties assign the config value for the
    corresponding key to __dict__[key].
    '''
    getter = lambda self: Config[section][key]  # type: ignore
    simple_name = '_{}'.format(key)
    complex_name = '_{}__{}'.format(section, key)
    for name in [simple_name, complex_name]:
        setattr(cls, name, lazy(getter, name=name))


def configurable(**sections):
    ''' Set lazy properties for all values in each item in 'sections'.
    It is imperative that the property adding routine is encapsulated in
    the function _add_conf_property, because the closure 'getter' won't
    bind to the current value of loop variables 'key' and 'section',
    resulting in all properties defined in one decoration having the
    same effective value.
    '''
    def dec(cls):
        Configurations.add_configurable(cls)
        for section, keys in sections.items():
            for key in keys:
                _add_conf_property(cls, section, key)
        return cls
    return dec


def config_home():
    return os.environ.get('XDG_CONFIG_HOME',
                          os.path.expanduser(os.path.join('~', '.config')))


def standard_config_files(alias):
    etc_dir = os.path.join('/etc', alias)
    fname = '{}.conf'.format(alias)
    return (os.path.join('/etc', fname), os.path.join(etc_dir, fname),
            os.path.join(config_home(), fname),)


def reset_config():
    Configurations.register_files('golgi', *standard_config_files('golgi'))
    Configurations.register_config('golgi', 'general', debug=False,
                                   verbose=False,
                                   stdout=BoolConfigOption(True, no=True))


__all__ = ('ConfigClient', 'Configurations', 'configurable',
           'lazy_configurable', 'ListConfigOption',
           'UnicodeConfigOption', 'PathConfigOption', 'PathListConfigOption',
           'FileSizeConfigOption', 'IntConfigOption', 'FloatConfigOption',
           'DictConfigOption', 'ConfigError', 'reset_config')
