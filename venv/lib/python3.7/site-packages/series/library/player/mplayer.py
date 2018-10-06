from mplayer import Player

from series.library.player.interface import PlayerInterface


class MPlayer(PlayerInterface):

    def __init__(self, args):
        def dict2args(a):
            return ["-{}={}".format(k, v) for k, v in a.items()]
        base_args = ('-slave', '-idle', '-really-quiet', '-msglevel',
                     'global=4', '-noconfig', 'all')
        super().__init__(Player(args=dict2args(args) + base_args))

    def stop(self):
        self._player.stop()

    def pause(self):
        self._player.pause()

    def osd(self, level):
        self._player.osd(level)

    def osd_level(self):
        return self._player.osdlevel

    @property
    def current_volume(self):
        return self._player.volume

    def volume(self, value):
        self._player.volume = value

    def message(self, msg, duration):
        pass

__all__ = ['MPlayer']
