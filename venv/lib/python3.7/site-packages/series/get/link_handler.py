from multiprocessing import Process, Array, Value
from datetime import datetime

from golgi.config import configurable
from amino import Maybe
from amino.lazy_list import lazy_list

from series.get.handler import ReleaseHandler
from series.get.model.link import LinkChecker
from series.logging import Logging
from series.handler import Job


@configurable(get=['link_check_proc_timeout'])
class LinkCheckTask(Process, Logging):

    def __init__(self, link):
        self._link_check_proc_timeout
        self.link = link
        self.done = Value('i', 0)
        self.status = Value('i', 0)
        self.dead = Value('i', 0)
        self.reason = Array('c', 1024)
        self.size = Value('i', 0)
        self.multipart = Value('i', 0)
        self.link.last_check = datetime.now()
        super().__init__(name='seriesd link checker')
        self.get = True

    def run(self):
        self.log.debug('Checking link {}…'.format(self.link.url))
        self._check_link()
        self.done.value = 1

    @property
    def timeout(self):
        delta = (datetime.now() - self.link.last_check).total_seconds()
        return delta > self._link_check_proc_timeout

    def _check_link(self):
        checker = LinkChecker(self.link)
        status, dead, reason, size, multipart = checker.result
        self.status.value = status
        self.dead.value = dead
        self.reason.value = reason.encode('utf8')[:1024]
        self.size.value = size
        self.multipart.value = multipart

    @property
    def result(self):
        return [self.status.value, self.dead.value, self.reason.value.decode(),
                self.size.value, self.multipart.value]


@configurable(get=['link_check_procs'])
class LinkHandler(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        self._running_tasks = []
        super().__init__(releases, 1, 'link handler', **kw)

    def _handle(self, links):
        for link in links:
            if len(self._running_tasks) < self._link_check_procs:
                self._launch_task(link)
        self._cleanup()

    @property
    def _current(self):
        return Maybe(Job(self._candidates))

    def _launch_task(self, link):
        link.checking = True
        task = LinkCheckTask(link)
        self._running_tasks.append(task)
        task.start()

    def _cleanup(self):
        self._clean_done()
        self._clean_timeouts()

    def _clean_done(self):
        done = [task for task in self._running_tasks if task.done.value]
        for task in done:
            task.link.checking = False
            self._running_tasks.remove(task)
            task.link.set_status(*task.result)
        if done:
            self._commit()

    def _clean_timeouts(self):
        timeout = [task for task in self._running_tasks if task.timeout]
        for task in timeout:
            task.terminate()
            task.link.checking = False
            task.link.check_failed()
            self._running_tasks.remove(task)
        if timeout:
            self._commit()

    def wait(self):
        while self._running_tasks:
            self._cleanup()
        self._cleanup()

    def terminate(self):
        for task in self._running_tasks:
            task.terminate()

    def stop(self):
        super().stop()
        self.terminate()

    @property
    def _candidates(self):
        return self._critical or self._normal or self._recheck

    @property
    def _critical(self):
        return self._pick_links(self._critical_releases)

    @property
    def _normal(self):
        return self._pick_links(self._normal_releases)

    @property
    def _recheck(self):
        return self._pick_links(self._normal_releases, recheck=True)

    @lazy_list
    def _pick_links(self, releases, recheck=False):
        attr = ('re' if recheck else '') + 'checkable_links'
        for release in releases:
            links = getattr(release, attr)
            if links:
                yield links[0]

    @property
    def _critical_releases(self):
        return [r for r in self._normal_releases if not r.valid_links]

    @property
    def _normal_releases(self):
        return self._releases.download_candidates

__all__ = ['LinkHandler']
