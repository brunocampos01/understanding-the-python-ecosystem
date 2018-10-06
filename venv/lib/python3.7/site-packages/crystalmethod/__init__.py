"""
A multimethod implementation.
Loosely based on Guido's initial 'Five-minute Multimethods in Python':
http://www.artima.com/weblogs/viewpost.jsp?thread=101605
This implementation is more advanced and supports instance methods as
well as a condition based dispatch.
"""

from itertools import starmap


class multimethod(object):
    """Decorator for multiple dispatch of functions and methods.

    This decorator provides a mechanism for multiple dispatch, whereby
    the function to be invoked can depend on the type of more than one
    argument. For instance::

        >>> @multimethod(int, int)
        ... def foo(a, b):
        ...    return "int, int"

        >>> @multimethod(float, float)
        ... def foo(a, b):
        ...    return "float, float"

        >>> foo(1, 2)
        'int, int'

        >>> foo(1.1, 2.3)
        'float, float'

    This multiple dispatch can be combined with the built-in dispatch:

        >>> class A(object):
        ...     @multimethod(int)
        ...     def foo(self, a):
        ...          return 'A, int'
        ...     @multimethod(float)
        ...     def foo(self, a):
        ...          return 'A, float'

        >>> x = A()
        >>> x.foo(3)
        'A, int'

        >>> x.foo(1.3)
        'A, float'

    Additional preconditions can be specified in the multimethod
    definition. For instance a poor man's implementation of the
    absolute value could be::

        >>> from numbers import Number
        >>> @multimethod(Number, condition="x >= 0")
        ... def absolute_value(x):
        ...     return x

        >>> @multimethod(Number, condition="x < 0")
        ... def absolute_value(x):
        ...     return -x

        >>> absolute_value(3)
        3

        >>> absolute_value(-0.25)
        0.25

    For more general uses, one should use the decorators provided by
    ``peak.rules``.
    """

    def __init__(self, *types, **kwargs):
        self.types = types
        self.condition = kwargs.pop('condition', None)
        if kwargs:
            msg = "multimethod() got an unexpected keyword argument {0!r}"
            raise TypeError(msg.format(list(kwargs.keys())[0]))

    class _Dispatcher(object):

        def __init__(self):
            self.typemap = []
            self.ismethod = False

        def __get__(self, obj, type=None):
            if obj is None:
                return self
            from functools import partial
            self.ismethod = True
            return partial(self, obj)

        def __call__(self, *args, **kw):
            matchable = args[1:] if self.ismethod else args
            for types, condition, function, argspec in self.typemap:
                if (len(matchable) == len(types) and
                        all(starmap(isinstance, zip(matchable, types)))):
                    if condition is None:
                        return function(*args, **kw)
                    else:
                        l = dict(zip(argspec.args, args))
                        if eval(condition, globals(), l):
                            return function(*args, **kw)
            raise ValueError("multimethod: no matching method found")

    def __call__(self, function):
        import inspect
        frame = inspect.currentframe()
        try:
            dispatcher = frame.f_back.f_locals.get(function.__name__,
                                                   self._Dispatcher())
        finally:
            del frame
        dispatcher.typemap.append((self.types, self.condition, function,
                                   inspect.getargspec(function)))
        return dispatcher
