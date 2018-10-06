import abc
from datetime import datetime, timedelta

from series.condition import AttrCondition
from series.handler import Handler
from series.get.model.release import ReleaseMonitor
from series.get.model.link import Link, Torrent
from series.get.model.show import Show

from sqlalchemy.sql.expression import and_

import amino
from amino import Empty, Maybe, _, __


class ReleaseAttr(AttrCondition[ReleaseMonitor]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('release', attr, target=target)


R = ReleaseAttr


class LinkAttr(AttrCondition[Link]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('link', attr, target)


Li = LinkAttr


class ShowAttr(AttrCondition[Show]):

    def __init__(self, attr: str, target=True) -> None:
        super().__init__('show', attr, target)


S = ShowAttr


class BaseHandler(Handler):

    def __init__(self, data, interval, description, **kw):
        self._data = data
        super().__init__(interval, description, **kw)

    @property
    def _candidates(self):
        return self._data.all

    @property
    def _lock(self):
        return self._data.lock

    def _update(self, item, **data):
        self._update_id(item.id, **data)

    def _update_id(self, id, **data):
        self._data.update_by_id(id, **data)


class ReleaseHandler(BaseHandler):

    @property
    def _releases(self):
        return self._data

    @property
    def _no_cached_torrents_q(self):
        return (
            self._releases.monitors
            .filter_by(downloaded=False, downloading=False)
            .filter(~ReleaseMonitor.torrents.any(
                and_(Torrent.cached, ~Torrent.dead)))
        )

    @property
    def _no_cached_torrents(self):
        return self._no_cached_torrents_q.all()


class ShowHandler(BaseHandler):

    @property
    def _shows(self):
        return self._data


class AsyncAdapter:

    def __init__(self, proc, monitor) -> None:
        self.proc = proc
        self.monitor = monitor
        self.created = datetime.now()

    def kill(self):
        pass

    def start(self):
        return self.proc.start()


class ProcessAdapter(AsyncAdapter):

    def kill(self):
        return self.proc.terminate()


class AsyncHandler(ReleaseHandler):

    def __init__(self, timeout, *a, **kw) -> None:
        super().__init__(*a, **kw)
        self._async = Empty()
        self._timeout = timedelta(minutes=timeout)

    def _handle(self, monitor):
        if self._async.empty:
            self._async = (
                self._create_async(monitor) /
                amino.L(self._adapter)(_, monitor) %
                __.start()
            )

    def _cleanup(self):
        def timeout(a):
            if datetime.now() - a.created > self._timeout:
                self._clean_timeout(a)
                a.kill()
                return True
        if (self._async.exists(self._clean_done) or
                self._async.exists(timeout)):
            self._async = Empty()

    @abc.abstractproperty
    def _adapter(self) -> type:
        ...

    @abc.abstractmethod
    def _clean_done(self, proc) -> bool:
        ...

    @abc.abstractmethod
    def _clean_timeout(self, proc) -> None:
        ...


class ThreadHandler(AsyncHandler):

    @property
    def _adapter(self):
        return AsyncAdapter


class ProcessHandler(AsyncHandler):

    @property
    def _adapter(self):
        return ProcessAdapter

    @abc.abstractmethod
    def _create_async(self, monitor) -> Maybe[AsyncAdapter]:
        ...


__all__ = ('ReleaseHandler', 'ShowHandler', 'ProcessHandler', 'ThreadHandler')
