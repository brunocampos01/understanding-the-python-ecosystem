import sys

from golgi import cli

from series.client.cli import HTTPCLI
from series.get.client.rest_api import GetClient
from series.get import SeriesGetD


class SeriesGetC(HTTPCLI):

    @property
    def _client(self):
        return GetClient()


@cli()
def getd():
    SeriesGetD().run()


@cli(positional=(('cli_cmd', 1), ('cli_params', '*')))
def getc():
    if not SeriesGetC().run():
        sys.exit(1)

__all__ = ['getd', 'getc']
