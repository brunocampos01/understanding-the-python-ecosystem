from abc import ABCMeta, abstractmethod, abstractproperty

from series.logging import Logging


class PlayerInterface(Logging, metaclass=ABCMeta):

    def __init__(self, player):
        self._player = player

    @abstractmethod
    def stop(self):
        ...

    @abstractmethod
    def pause(self):
        ...

    @abstractmethod
    def osd(self, level):
        ...

    @abstractmethod
    def osd_level(self):
        ...

    @abstractproperty
    def current_volume(self):
        ...

    @abstractmethod
    def volume(self, value):
        ...

    def __getattr__(self, name):
        return getattr(self._player, name)

    def __setattr__(self, name, value):
        if name == '_player':
            super().__setattr__(name, value)
        else:
            setattr(self._player, name, value)

    @property
    def running(self):
        return self.time_pos is not None

    @abstractmethod
    def message(self, msg, duration):
        ...

    def show_progress(self):
        pass

__all__ = ['PlayerInterface']
