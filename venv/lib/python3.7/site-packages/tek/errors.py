class Error(Exception):

    def __init__(self, msg=''):
        super(Error, self).__init__(str(msg))


class TException(Error):
    pass


MooException = TException


class NoOverloadError(NotImplementedError):

    def __init__(self, function, obj):
        error_msg = '%s cannot handle parameters of type %s!' \
                    % (function, type(obj))
        super(NoOverloadError, self).__init__(error_msg)


class InternalError(TException):
    pass


class InvalidInput(TException):
    def __init__(self, string):
        super(InvalidInput, self).__init__('Invalid input: %s' % string)


class NotEnoughDiskSpace(TException):
    def __init__(self, dir, wanted, avail):
        from tek.tools import sizeof_fmt
        text = 'Not enough space in directory "{}" ({} needed, {} available)'
        text = text.format(dir, sizeof_fmt(wanted), sizeof_fmt(avail))
        super(NotEnoughDiskSpace, self).__init__(text)


class ParseError(TException):
    pass
