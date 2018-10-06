import os

from golgi.config import configurable
from tek.tools import wait_for

from amino import Just, Empty

from series.library.playback_observer import PlaybackObserver
from series.logging import Logging


@configurable(player=['display', 'path', 'subtitles', 'args', 'resume_before',
                      'mplayer_extra_args', 'mpv_extra_args', 'player_type'])
class Player(Logging):

    def __init__(self, library) -> None:
        self._library = library
        if self._display:
            os.environ['DISPLAY'] = self._display
        self._Player = None
        self._mplayer = None
        self._target = None
        self._observer = None
        self._extra_args = []  # type: list
        self._sub_fps = Empty()
        self._setup_player_type()

    def _setup_player_type(self):
        errors = []
        if self._player_type == 'mplayer':
            try:
                from series.library.player.mplayer import MPlayer
                from mplayer import Player
            except ImportError as e:
                errors.append(e)
            else:
                self._Player = MPlayer
                Player.exec_path = self._path
                self._extra_args = self._mplayer_extra_args
        elif self._player_type == 'mpv':
            try:
                from series.library.player.mpv import MPV
            except ImportError as e:
                errors.append(e)
            else:
                self._Player = MPV
                self._extra_args = self._mpv_extra_args
        if self._Player is None:
            self.log.error(f'initializing player failed: {errors}')

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, epi):
        self.stop()
        self._target = epi

    def start(self):
        self._check_file()
        self._mplayer = self._Player(self._all_args)
        self._observer = PlaybackObserver(self._mplayer, self._library,
                                          self._target, self)
        self._mplayer.loadfile(str(self._file))
        self._observer.start()
        self._resume()

    def _resume(self):
        wait_for(lambda: self.running)
        pos = self._target.resume_position
        subdelay = self._target.subdelay
        length = self._wait_for_prop('length')
        if pos and length and pos < self._resume_before * length:
            self._set_pos(pos)
        if subdelay:
            self.sub_delay(subdelay)

    def restart(self) -> None:
        self.stop()
        self.start()

    def _check_file(self):
        if not (self._file and self._file.exists()):
            raise OSError('File not found: {}'.format(self._file))

    def toggle_pause(self):
        if self.running:
            self._mplayer.pause()

    def seek(self, value):
        if self.running:
            elapsed = self._wait_for_prop('time_pos')
            if elapsed is not None:
                new_value = elapsed + value
                self._set_pos(new_value)

    def seek_to_ratio(self, value):
        if self.running:
            new_value = value * self.length
            self._set_pos(new_value)

    def _set_pos(self, new_value):
        new_value = max(0, new_value)
        new_value = min(self.length, new_value) if self.length else new_value
        self._mplayer.time_pos = new_value
        self.message('pos: {}'.format(new_value))

    def sub_delay(self, value):
        if self.running:
            self._mplayer.sub_delay += value
            self.message('sub: {}'.format(self._mplayer.sub_delay))

    def sub_fps(self, value) -> None:
        if self.running:
            self._sub_fps = Just(value)
            self.restart()

    def change_volume(self, value):
        if self.running:
            current = self._mplayer.current_volume
            new_value = current + value
            self._mplayer.volume(min(100, max(0, new_value)))
            self.message('vol: {}'.format(new_value))

    def stop(self):
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
        if self._mplayer is not None:
            self._mplayer.stop()
            self._mplayer = None

    def toggle_info(self):
        if self.running:
            current = self._mplayer.osd_level()
            self._mplayer.osd(0 if current > 1 else 3)

    def message(self, msg, duration=500):
        self._mplayer.show_text(msg, duration)

    @property
    def elapsed(self):
        return self._player_prop('time_pos')

    @property
    def length(self):
        return self._player_prop('length')

    @property
    def remaining(self):
        return self.length - self.remaining

    @property
    def _file(self):
        return self._library.video_path(self.target)

    @property
    def _sub_file(self):
        return self._library.subtitle_path(self._target)

    @property
    def running(self):
        return self._mplayer is not None and self._mplayer.running

    @property
    def _all_args(self):
        args = self._args.copy()
        args.update(self._subtitle_args)
        args.update(self._subfps_args)
        args.update(self._extra_args)
        return args

    @property
    def _subtitle_args(self):
        return (dict(sub_files=str(self._sub_file))
                if self._subtitles and self._target
                else [])

    @property
    def _subfps_args(self):
        value = self._target.subfps_fallback
        return dict(subfps=value) if value else []

    def _player_prop(self, name, default=0):
        return getattr(self._mplayer, name, default)

    def _wait_for_prop(self, name):
        value = None
        def poll():
            nonlocal value
            value = self._player_prop(name, None)
            return value
        wait_for(poll, 0.5, 0.1)
        return value

    def same_episode(self, observer):
        return observer is self._observer

__all__ = ['Player']
