import re
from os.path import expandvars
from pathlib import Path
from typing import Iterable

from golgi.config.errors import ConfigValueError, ConfigTypeError
from golgi.logging import Logging

from amino import List, _, Boolean, Lists


def boolify(value):
    """ Return a string's boolean value if it is a string and "true" or
    "false"(case insensitive), else just return the object.
    """
    try:
        return value.lower() in ['true', 'yes', '1']
    except:
        return bool(value)


class ConfigOption(Logging):

    def __init__(self, positional=None, short=None, **params):
        self.positional = positional
        self.short = short
        self.set_argparse_params(**params)

    def set_argparse_params(self, help=''):
        self._help = help
        self.help = help

    @property
    def argparse_params(self):
        p = dict()
        for name in ['help']:
            value = getattr(self, '_' + name, None)
            if value:
                p[name] = value
        return p

    def set_from_co(self, other):
        self.set_argparse_params(**other.argparse_params)
        if other.positional is not None:
            self.positional = other.positional
        if other.short is not None:
            self.short = other.short

    @property
    def effective_value(self):
        return self.value


class TypedConfigOption(ConfigOption):
    """ This is intended to automagically create objects from a string
    read from a config file, if desired. If a TypedConfigOption is put
    into a ConfigDict, setting a value is passed to the set() method,
    which then creates an object from the parameter from the config.
    """

    def __init__(self, value_type, defaultvalue, factory=None, **params):
        """ Construct a TypedConfigOption.
            @param value_type: The type used to create new instances of
            the config value.
            @param defaultvalue: The initial value to which this object
            is set.
            @type defaultvalue: value_type
        """
        self.value_type = value_type
        self._factory = factory
        self.set(defaultvalue)
        ConfigOption.__init__(self, **params)

    def set(self, args):
        """ Assign args as the config object's value.
        If args is not of the value_type of the config object, it is
        passed to value_type.__init__. args may be a tuple of
        parameters.
        """
        try:
            if isinstance(args, tuple):
                if len(args) != 1:
                    self.log.debug('TypedConfigOption: len > 1')
                    self.value = self.value_type(*args)
                    return
                else:
                    args = args[0]
            if isinstance(args, self.value_type):
                self.value = args
            elif self._factory is not None:
                self.value = self._factory(args)
            else:
                self.value = self.value_type(args)
        except ValueError:
            raise ConfigValueError(self.__class__, args)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def set_from_co(self, other):
        if other.value is not None:
            self.value = other.value
        ConfigOption.set_from_co(self, other)


class BoolConfigOption(TypedConfigOption):
    """ Specialization of TypedConfigOption for booleans, as they must
    be parsed from strings differently.
    """

    def __init__(self, defaultvalue=False, no=None, no_switch=None, **params):
        TypedConfigOption.__init__(self, Boolean, defaultvalue, **params)
        self.no = no
        self.no_switch = no_switch

    def set_from_co(self, other):
        if other.no is not None:
            self.no = other.no
            self.no_switch = other.no_switch
        TypedConfigOption.set_from_co(self, other)

    def set(self, arg):
        super(BoolConfigOption, self).set(boolify(arg))


class ListConfigOption(TypedConfigOption):

    def __init__(self, defaultvalue=None, splitchar=',', element_type=None,
                 **params):
        if defaultvalue is None:
            defaultvalue = []
        self._splitchar = splitchar
        self._element_type = element_type
        super().__init__(List, defaultvalue, factory=List.wrap, **params)

    def set(self, value):
        if isinstance(value, str):
            value = value.split(self._splitchar)
        elif not isinstance(value, Iterable):
            raise ConfigTypeError(list, value)
        super().set(value)
        if self._element_type is not None:
            self.value = self.value / self._element_type

    @property
    def effective_value(self):
        if self._element_type is not None:
            return [getattr(e, 'effective_value', e) for e in self.value]
        else:
            return TypedConfigOption.effective_value.fget(self)

    def __str__(self):
        return self._splitchar.join(self.value / str)


class PathListConfigOption(ListConfigOption):

    def __init__(self, *a, **kw):
        t = PathConfigOption
        super().__init__(*a, element_type=t, **kw)

    def set(self, value):
        super().set(value)
        glob = lambda a: Lists.wrap(a.parent.glob(a.name))
        self.value = List.wrap(self.value) / _.value // glob

    @property
    def effective_value(self):
        return self.value


class UnicodeConfigOption(TypedConfigOption):

    def __init__(self, default, **params):
        TypedConfigOption.__init__(self, str, default, **params)


class PathConfigOption(TypedConfigOption):

    def __init__(self, path=None, **params):
        super().__init__(Path, path or Path.cwd(), **params)

    def set(self, path):
        self.value = Path(expandvars(str(path))).expanduser().absolute()


class NumericalConfigOption(TypedConfigOption):

    def __init__(self, defaultvalue=-1, value_type=int, **params):
        super(NumericalConfigOption, self).__init__(value_type, defaultvalue,
                                                    **params)


class IntConfigOption(NumericalConfigOption):

    def __init__(self, defaultvalue=-1, **params):
        super(IntConfigOption, self).__init__(defaultvalue=defaultvalue,
                                              value_type=int, **params)


class FloatConfigOption(NumericalConfigOption):

    def __init__(self, defaultvalue=-1., **params):
        super(FloatConfigOption, self).__init__(defaultvalue=defaultvalue,
                                                value_type=float, **params)


class FileSizeConfigOption(FloatConfigOption):
    _prefixes = ['', 'k', 'm', 'g', 't', 'p']
    _prefix_string = ''.join(_prefixes)
    _regex = re.compile('(\d+(?:\.\d+)?)\s*([{}])b?$'.format(_prefix_string),
                        re.I)

    def __init__(self, defaultvalue=-1, **params):
        super(FileSizeConfigOption, self).__init__(defaultvalue, **params)

    def set(self, value):
        if isinstance(value, str):
            m = self._regex.match(value)
            if not m:
                raise CValueError(FileSizeConfigOption, value)
            value, prefix = m.groups()
            try:
                pass
            except IndexError:
                raise CValueError(FileSizeConfigOption, value)
            exponent = 3 * self._prefixes.index(prefix.lower())
            value = float(value) * (10 ** exponent)
        super(FileSizeConfigOption, self).set(value)


class DictConfigOption(TypedConfigOption):

    def __init__(self, defaultvalue=None, key_type=str,
                 dictvalue_type=str, **params):
        defaultvalue = defaultvalue or dict()
        self.key_type = key_type
        self.dictvalue_type = dictvalue_type
        super(DictConfigOption, self).__init__(value_type=dict,
                                               defaultvalue=defaultvalue)

    def set(self, value):
        sanitize = lambda s: s.replace('\\', '')
        if isinstance(value, str):
            items = (re.split(r'(?<!\\):', item, maxsplit=1) for item in
                     re.split(r'(?<!\\),', value))
            value = dict(((self.key_type(sanitize(k)),
                           self.dictvalue_type(sanitize(v)))
                          for k, v in items))
        super(DictConfigOption, self).set(value)

__all__ = ['BoolConfigOption', 'ListConfigOption', 'UnicodeConfigOption',
           'PathConfigOption', 'PathListConfigOption', 'FileSizeConfigOption',
           'IntConfigOption', 'FloatConfigOption', 'DictConfigOption']
