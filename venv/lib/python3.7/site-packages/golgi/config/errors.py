class ConfigError(Exception):
    pass


class NoSuchOptionError(ConfigError):

    def __init__(self, key):
        super(NoSuchOptionError, self).__init__('No such config option: %s' % key)


class DuplicateDefaultError(ConfigError):

    def __init__(self, key):
        super(DuplicateDefaultError, self).__init__('Default config option already set: %s' % key)


class MultipleSectionsWithKeyError(ConfigError):

    def __init__(self, key):
        super(MultipleSectionsWithKeyError, self).__init__('More than one section contain an option with the value %s' % key)


class DuplicateFileSectionError(ConfigError):

    def __init__(self, section):
        super(DuplicateFileSectionError, self).__init__(
                'Config file section \'%s\' already added!' % section)


class DuplicateDefaultSectionError(ConfigError):

    def __init__(self, section):
        super(DuplicateDefaultSectionError, self).__init__(
                'Config defaults section \'%s\' already added!' % section)


class NoSuchConfigError(ConfigError):

    def __init__(self, name):
        super(NoSuchConfigError, self).__init__('No Configurable registered under the name %s' % name)


class NoSuchSectionError(ConfigError):

    def __init__(self, section):
        super(NoSuchSectionError, self).__init__('No section named \'%s\' had been loaded!' % section)


class ConfigClientNotYetConnectedError(ConfigError):
    """ This error is thrown if a ConfigClient instance tries to get a
    config value before the corresponding Configurable hadn't yet been
    initialized and connected.
    
    """

    def __init__(self, name, key):
        error_string = 'Config Client \'%s\' wasn\'t connected when accessing config option \'%s\'!' % (name, key)
        super(ConfigClientNotYetConnectedError, self).__init__(error_string)


class ConfigValueError(ConfigError):

    def __init__(self, option, value):
        message = '''Invalid value '{}' for config option '{}'!'''
        super().__init__(message.format(value, option))


class ConfigTypeError(ConfigError):

    def __init__(self, typ, value):
        message = 'Invalid type \'{}\' for \'{}\' (expected \'{}\')!'
        super().__init__(message.format(type(value), value, typ))


class ConfigLoadError(ConfigError):
    pass
