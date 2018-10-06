from series.errors import SeriesException


class ArchiverError(SeriesException):
    pass


class InvalidDBError(SeriesException):

    def __init__(self, specifics):
        text = 'Invalid database: {}'
        super().__init__(text.format(specifics))
