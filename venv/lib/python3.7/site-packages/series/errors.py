from golgi.errors import Error


class MissingMetadata(Error):
    pass


class SeriesException(Error):
    pass


class InvalidDBError(SeriesException):
    def __init__(self, specifics):
        text = 'Invalid database: {}'
        super().__init__(text.format(specifics))


class SeriesDException(SeriesException):
    pass
