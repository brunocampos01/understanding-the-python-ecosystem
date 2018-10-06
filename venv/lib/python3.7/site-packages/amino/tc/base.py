import importlib
import abc
from typing import Dict, Tuple, Any, Callable, Union, Optional, GenericMeta, TypeVar, Generic
from functools import partial, wraps

import amino
from amino.util.string import snake_case
from amino.lazy import lazy

from amino.logging import amino_root_logger, Logging

A = TypeVar('A')
TC = TypeVar('TC', bound='TypeClass')


class TypeClassMeta(GenericMeta):

    def __new__(
            cls: type,
            name: str,
            bases: tuple,
            namespace: dict,
            tpe: type=None,
            pred: Callable=None,
            sub: type=None,
            **kw: dict
    ) -> type:
        inst = super().__new__(cls, name, bases, namespace, **kw)  # type: ignore
        if name != 'TypeClass':
            if tpe is not None:
                Instances.add_auto(tpe, inst())
            elif pred is not None:
                Instances.add_pred(pred, inst())
            elif sub is not None:
                Instances.add_pred(lambda t: issubclass(t, sub), inst())
        return inst

    def fatal(self, tpe: type) -> 'TypeClass':
        return Instances.lookup_fatal(self, tpe)

    lookup = fatal

    def fatal_for(self, a: Any) -> 'amino.maybe.Maybe[TypeClass]':
        return self.fatal(type(a))

    def m(self, tpe: type) -> 'amino.maybe.Maybe[TypeClass]':
        return amino.maybe.Maybe.check(Instances.lookup(self, tpe))

    def m_for(self, a: Any) -> 'amino.maybe.Maybe[TypeClass]':
        return self.m(type(a))

    def e(self, tpe: type) -> 'amino.maybe.Maybe[TypeClass]':
        return (
            self.m(tpe)
            .to_either(f'no `{self.__name__}` instance for {tpe}')
        )

    def e_for(self, a: A) -> 'amino.either.Either[str, TC]':
        return self.e(type(a))

    def exists_instance(self, tpe: type) -> bool:
        return self.m(tpe).present

    exists = exists_instance


class TypeClass(Generic[A], Logging, metaclass=TypeClassMeta):
    pass


class TypeClasses:

    @property
    def instances(self) -> Dict[type, TypeClass]:
        pass


class ImplicitInstancesNotFound(Exception):

    def __init__(self, mod: str, cls: str, name: str) -> None:
        msg = 'invalid implicit class path {}.{} for {}'.format(mod, cls, name)
        super().__init__(msg)


operators = (
    '__floordiv__',
    '__truediv__',
    '__mod__',
    '__or__',
    '__and__',
)


class ImplicitInstancesMeta(abc.ABCMeta):

    def __new__(cls: type, name: str, bases: tuple, namespace: dict, tpe: type=None, **kw: dict) -> type:
        inst = super().__new__(cls, name, bases, namespace,  # type: ignore
                               **kw)
        if name != 'ImplicitInstances' and tpe is not None:
            Instances.add_instances(tpe, inst())
        return inst


class ImplicitInstances(metaclass=ImplicitInstancesMeta):

    @lazy
    def instances(self) -> Dict[type, TypeClass]:
        return (
            TC.instances ** self._instances **  # type: ignore
            self._override_instances
        )

    @abc.abstractproperty
    def _instances(self) -> Dict[type, TypeClass]:
        ...

    @property
    def _override_instances(self) -> Dict[type, TypeClass]:
        from amino.map import Map
        return Map()


def lookup_implicit_instances(name: str, m: str, c: str) -> ImplicitInstances:
    err = ImplicitInstancesNotFound(m, c, name)
    try:
        mod = importlib.import_module(m)
    except ImportError:
        raise err
    else:
        if hasattr(mod, c):
            instances = getattr(mod, c)()
            return instances
        else:
            raise err


class InstancesMetadata:

    def __init__(self, name: str, mod: str, cls: str) -> None:
        self.name = name
        self.mod = mod
        self.cls = cls
        self._instances = None  # type: Optional[ImplicitInstances]

    def __str__(self) -> str:
        return '{}({}, {}, {})'.format(self.__class__.__name__, self.name,
                                       self.mod, self.cls)

    @property
    def instances(self) -> Dict[type, TypeClass]:
        if self._instances is None:
            self._instances = lookup_implicit_instances(self.name, self.mod, self.cls)
        return self._instances.instances


def _infer_implicits(name: str) -> Tuple[str, str]:
    snake = snake_case(name)
    return 'amino.instances.{}'.format(snake), '{}Instances'.format(name)


class ImplicitsMeta(GenericMeta):

    @staticmethod
    def _mk_operator(name: str) -> Callable:
        def dispatch(self: Any, other: Any) -> Any:
            return self._operator(name, other)
        return dispatch

    def _attach_operators(inst) -> None:
        for op in operators:
            setattr(inst, op, ImplicitsMeta._mk_operator(op))

    def __new__(cls: type, name: str, bases: tuple, namespace: dict, imp_mod: str=None, imp_cls: str=None,
                implicits: bool=False, auto: bool=False, **kw: Any) -> type:
        inst = super().__new__(cls, name, bases, namespace, **kw)  # type: ignore
        inst.auto = auto or getattr(inst, 'auto', False)
        if not implicits:
            return inst
        else:
            inst.instances_meta = None
            inst.name = name
            ImplicitsMeta._attach_operators(inst)
            if not inst.auto:
                if imp_mod is None or imp_cls is None:
                    imp_mod, imp_cls = _infer_implicits(name)
                meta = InstancesMetadata(name, imp_mod, imp_cls)
                inst.imp_mod = imp_mod
                inst.imp_cls = imp_cls
                inst.instances_meta = meta
                Instances.add(meta)
            return inst

    __copy__ = None


def tc_prop(f: Callable) -> Callable:
    f._tc_prop = True  # type: ignore
    return f


class Implicits(metaclass=ImplicitsMeta):
    permanent = True

    def _lookup_implicit_attr(self, name: str) -> Optional[Callable]:
        meta = type(self).instances_meta  # type: ignore
        if meta is not None:
            return next((getattr(inst, name) for inst in meta.instances.v if hasattr(inst, name)), None)
        elif self.auto:
            return Instances.lookup_auto_attr(type(self), name)

    def _bound_implicit_attr(self, name: str) -> Union[None, Callable, partial]:
        f = self._lookup_implicit_attr(name)
        if f is not None:
            if hasattr(f, '_tc_prop'):
                return f(self)
            else:
                return partial(f, self)
        return None

    def _set_implicit_attr(self, name: str) -> Any:
        f = self._lookup_implicit_attr(name)
        if f is not None:
            @wraps(f)
            def wrap(self: Any, *a: Any, **kw: Any) -> Any:
                return f(self, *a, **kw)  # type: ignore
            g = property(wrap) if hasattr(f, '_tc_prop') else wrap
            setattr(type(self), name, g)
            return getattr(self, name)

    def __getattr__(self, name: str) -> Callable:
        imp = self._set_implicit_attr(name) if Implicits.permanent else self._bound_implicit_attr(name)
        if imp is None:
            err = '\'{}\' object has no attribute \'{}\''.format(self.__class__.__name__, name)
            raise AttributeError(err)
        else:
            return imp

    def _operator(self, name: str, other: Any) -> Any:
        op = (self._set_implicit_attr(name) if Implicits.permanent else
              self._bound_implicit_attr(name))
        if op is None:
            err = '\'{}\' has no implicit operator \'{}\''.format(self, name)
            raise TypeError(err)
        else:
            return op(other)

    @property
    def dbg(self) -> Any:
        amino_root_logger.test(self)
        return self

    @property
    def dbgr(self) -> Any:
        v = self.log.verbose  # type: ignore
        v(repr(self))
        return self


class GlobalTypeClasses(TypeClasses):

    @property
    def instances(self) -> Dict[type, TypeClass]:
        from amino.map import Map
        from amino.tc.tap import Tap
        from amino.tc.show import Show
        return Map({Show: Show(), Tap: Tap()})


class F(Generic[A], Implicits):
    pass


TC = GlobalTypeClasses()


class ImplicitNotFound(Exception):

    def __init__(self, tc: type, a: type) -> None:
        msg = 'no type class found for {}[{}]'.format(tc, a)
        super().__init__(msg)


class AutoImplicitInstances(ImplicitInstances):

    def __init__(self, tpe: type, instance: TypeClass) -> None:
        self.tpe = tpe
        self.instance = instance

    @lazy
    def _instances(self) -> Dict[type, TypeClass]:
        from amino import Map
        return Map({self.tpe: self.instance})


class NoTypeClass(Exception):

    def __init__(self, inst: Any) -> None:
        super().__init__('invalid type class: {}'.format(inst))


class PredTypeClass:

    def __init__(self, pred: Callable[[type], bool], tc: TypeClass) -> None:
        self.pred = pred
        self.tc = tc


class AllInstances:

    def __init__(self) -> None:
        self.instances = dict()  # type: Dict[str, InstancesMetadata]
        self.auto_instances = dict()  # type: Dict[type, ImplicitInstances]
        self.pred_instances = (dict())  # type: Dict[type, amino.list.List[PredTypeClass]]

    def add(self, data: InstancesMetadata) -> None:
        self.instances[data.name] = data

    def add_instances(self, tpe: type, instances: ImplicitInstances) -> None:
        if tpe in self.auto_instances:
            self.auto_instances[tpe].instances.update(instances._instances)
        else:
            self.auto_instances[tpe] = instances

    def _tc_type(self, inst: TypeClass) -> type:
        mro = inst.__class__.__mro__
        if len(mro) < 2 or TypeClass not in mro:
            raise NoTypeClass(inst)
        return mro[1]

    def add_auto(self, tpe: type, inst: TypeClass) -> None:
        tc_type = self._tc_type(inst)
        self.add_instances(tpe, AutoImplicitInstances(tc_type, inst))

    def add_pred(self, pred: Callable[[type], bool], inst: TypeClass) -> None:
        import amino.list
        tc_type = self._tc_type(inst)
        data = PredTypeClass(pred, inst)
        if tc_type in self.pred_instances:
            self.pred_instances[tc_type].append(data)
        else:
            self.pred_instances[tc_type] = amino.list.List(data)

    def lookup_fatal(self, TC: type, G: type) -> TypeClass:
        tc = self.lookup(TC, G)
        if tc is None:
            raise ImplicitNotFound(TC, G)
        return tc

    def lookup(self, TC: type, G: type) -> Optional[TypeClass]:
        ''' Find an instance of the type class `TC` for type `G`.
        Iterates `G`'s parent classes, looking up instances for each,
        checking whether the instance is a subclass of the target type
        class `TC`.
        '''
        match = lambda a: self._lookup_type(TC, a)
        def attach_type(tc: TypeClass) -> TypeClass:
            setattr(tc, 'tpe', G)
            return tc
        return next((attach_type(a) for a in map(match, G.__mro__) if a is not None), None)

    def lookup_auto_attr(self, tpe: type, name: str) -> Optional[Callable]:
        def check(t: type) -> 'amino.maybe.Maybe[Callable]':
            if t in self.auto_instances:
                ins = self.auto_instances[t]
                return next((getattr(inst, name) for inst in ins.instances.v if hasattr(inst, name)), None)
            else:
                return None
        return next((a for a in map(check, tpe.__mro__) if a is not None), None)

    def _lookup_type(self, TC: type, G: type) -> Optional[TypeClass]:
        auto = self._lookup_auto(TC, G)
        if auto is not None:
            return auto
        reg = self._lookup_regular(TC, G)
        if reg is not None:
            return reg
        return self._lookup_pred(TC, G)

    def _lookup_auto(self, TC: type, G: type) -> Optional[TypeClass]:
        if G in self.auto_instances:
            return next((b for a, b in self.auto_instances[G].instances.items() if isinstance(b, TC)),  # type: ignore
                        None)
        else:
            return None

    def _lookup_regular(self, TC: type, G: type) -> Optional[TypeClass]:
        if G.__name__ in self.instances:
            return next((b for a, b in self.instances[G.__name__].instances.items() if isinstance(b, TC)), None)
        else:
            return None

    def _lookup_pred(self, TC: type, G: type) -> Optional[TypeClass]:
        if TC in self.pred_instances:
            return next((a.tc for a in self.pred_instances[TC] if a.pred(G)), None)
        else:
            return None

Instances = AllInstances()  # type: AllInstances

__all__ = ('TypeClasses', 'TC', 'tc_prop', 'TypeClass')
