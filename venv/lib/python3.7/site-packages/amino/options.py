import os

import amino


class EnvOption:

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def exists(self) -> bool:
        return self.name in os.environ

    def __bool__(self) -> bool:
        return self.exists

    @property
    def value(self) -> 'amino.Maybe[str]':
        return amino.env[self.name]

    def __str__(self) -> str:
        value = self.value.map(lambda a: f'={a}') | ' is unset'
        return f'{self.name}{value}'


development = EnvOption('AMINO_DEVELOPMENT')
integration_test = EnvOption('AMINO_INTEGRATION')
anon_debug = EnvOption('AMINO_ANON_DEBUG')
io_debug = EnvOption('AMINO_IO_DEBUG')
env_xdg_data_dir = EnvOption('XDG_DATA_DIR')

__all__ = ('development', 'integration_test', 'anon_debug', 'io_debug', 'env_xdg_data_dir')
