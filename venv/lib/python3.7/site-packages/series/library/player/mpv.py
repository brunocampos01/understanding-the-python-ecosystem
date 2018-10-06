from typing import Callable

from mpv import MPV as Player

from series.library.player.interface import PlayerInterface
from series.logging import Logging


class MPV(PlayerInterface, Logging):

    def __init__(self, args: tuple) -> None:
        self._player = Player(input_default_bindings=True, input_vo_keyboard=True, **args)
        def callback(name: str, handler: Callable) -> None:
            def wrap(*a: tuple, **kw: dict) -> None:
                handler(*a, **kw)
            self._player.event_callback(name)(wrap)
        callback('shutdown', self.event_shutdown)

    def stop(self):
        self._player.quit()
        self._player = None

    def pause(self):
        self._player.pause = not self._player.pause

    def osd(self, level):
        self._player.osd_level = level

    def osd_level(self):
        return self._player.osd_level

    @property
    def current_volume(self):
        return self._player.volume

    def volume(self, value):
        self._player.volume = value

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except TypeError:
            pass

    def event_shutdown(self, data, *a, **kw):
        pass

    @property
    def length(self):
        return self.duration

    def message(self, msg, duration):
        self._player.show_message(msg, duration)

    def show_progress(self):
        self._player.show_progress()

__all__ = ['MPV']
