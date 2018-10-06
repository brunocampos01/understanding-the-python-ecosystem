import os

from amino.map import Map
from amino import Either


class EnvVars:

    @property
    def vars(self):
        return Map(os.environ)

    def __contains__(self, name: str) -> bool:
        return name in self.vars

    def __getitem__(self, name: str) -> Either[str, str]:
        return self.vars.get(name).to_either(f'env var {name} is unset')

    def __setitem__(self, name: str, value: str) -> None:
        os.environ[name] = str(value)

env = EnvVars()

__all__ = ('EnvVars', 'env')
