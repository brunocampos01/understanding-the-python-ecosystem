import functools


def generated_list(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        return list(func(*a, **kw))
    return wrapper


def generated_sum(init=0):
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            return sum(func(*a, **kw), init)
        return wrapper
    return decorate


class _LazyPropDecorator(object):

    def __init__(self, method, name=None):
        self.create = method
        self.name = name or method.__name__
        functools.update_wrapper(self, method)


class lazy_property(_LazyPropDecorator):

    def __get__(self, instance, owner):
        if instance is None:
            return self
        elif self.name in instance.__dict__:
            return instance.__dict__[self.name]
        else:
            value = self.create(instance)
            instance.__dict__[self.name] = value
            return value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set__(self, instance, value):
        msg = 'Tried to set lazy property {}.{}'.format(
            type(instance).__name__, self.name)
        raise AttributeError(msg)


class lazy_class_property(_LazyPropDecorator):

    def __get__(self, instance, owner):
        value = self.create(owner)
        setattr(owner, self.name, value)
        return value

__all__ = ['generated_list', 'generated_sum', 'lazy_property',
           'lazy_class_property']
