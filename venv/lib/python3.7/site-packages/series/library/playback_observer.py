import time
import threading
from datetime import datetime

from tek.tools import wait_for

from series.library.model.episode import Episode


class PlaybackObserver(threading.Thread):

    def __init__(self, mplayer, library, video, player):
        super().__init__()
        self._mplayer = mplayer
        self._library = library
        self._video = video
        self._player = player
        self._start_time = None
        self._finish_time = None
        self._stopped = False
        self._last_pos = None

    def run(self):
        wait_for(lambda: self._player.running)
        self._start_time = datetime.now()
        while self._running:
            self._set_position()
            time.sleep(1)
        self._finish()

    def stop(self):
        self._stopped = True

    def _set_position(self):
        position = self._player.elapsed
        if position:
            self._last_pos = position

    def _finish(self):
        self._finish_time = datetime.now()
        if isinstance(self._video, Episode):
            self._library.add_watch_event(
                self._video.series,
                self._video.season,
                self._video.number,
                self._start_time,
                self._finish_time,
                self._last_pos
            )

    @property
    def _running(self):
        ''' Test whether the same video is still loaded in mplayer.
        Either it has been terminated manually, which means that stop()
        has been called, or the video is at its end, in which case the
        'running' attribute of the player and the current observer is
        used.
        '''
        return (not self._stopped and self._player.running and
                self._player.same_episode(self))

__all__ = ['PlaybackObserver']
