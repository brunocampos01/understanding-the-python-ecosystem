import sys

from golgi import cli

from series.client.cli import HTTPCLI
from series.library.client.rest_api import LibClient
from series.library import SeriesLibraryD


class SeriesLibraryC(HTTPCLI):

    @property
    def _client(self):
        return LibClient()


@cli(positional=(('cli_cmd', 1), ('cli_params', '*')))
def libc():
    if not SeriesLibraryC().run():
        sys.exit(1)


@cli()
def libd():
    SeriesLibraryD().run()

__all__ = ['libc', 'libd']
