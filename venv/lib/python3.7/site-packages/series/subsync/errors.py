from tek.errors import TException

class NoSuchSeriesMapping(TException):
    def __init__(self, name):
        text = 'No url mapping for series {}'.format(name)
        super().__init__(text)

class NoSubsForEpisode(TException):
    def __init__(self, series, season, episode):
        text = 'No subs for episode {} of series "{}" season {}'
        text = text.format(episode, series, season)
        super().__init__(text)
