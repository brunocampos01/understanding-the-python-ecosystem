import abc
import time
from typing import Union, Any, Callable
from datetime import datetime

import spec

from amino.test.spec import SpecBase, IntegrationSpecBase, default_timeout
from amino.test.sure import SureSpec


def later(ass: Callable[..., bool], *a: Any, timeout: Union[float, None]=None, intval: float=0.1, **kw: Any) -> bool:
    timeout = default_timeout if timeout is None else timeout
    start = datetime.now()
    ok = False
    while not ok and (datetime.now() - start).total_seconds() < timeout:
        try:
            ass(*a, **kw)
            ok = True
        except AssertionError:
            time.sleep(intval)
    return ass(*a, **kw)


class SpecMeta(spec.InnerClassParser, abc.ABCMeta):
    pass


class Spec(SureSpec, SpecBase, spec.Spec, metaclass=SpecMeta):

    def setup(self) -> None:
        SureSpec.setup(self)
        SpecBase.setup(self)

    def _wait_for(self, pred: Callable[[], bool], timeout: float=default_timeout, intval: float=0.1) -> None:
        start = datetime.now()
        while (not pred() and (datetime.now() - start).total_seconds() < timeout):
            time.sleep(intval)
        pred().should.be.ok


class IntegrationSpec(IntegrationSpecBase, Spec):

    def setup(self) -> None:
        IntegrationSpecBase.setup(self)
        Spec.setup(self)

__all__ = ('Spec', 'IntegrationSpec')
