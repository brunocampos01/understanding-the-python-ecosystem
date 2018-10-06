import abc
import time
from threading import Thread
from datetime import datetime, timedelta

import sqlalchemy

from series.logging import Logging

import amino
from amino import List, Map, __

from series.errors import SeriesDException
from series.condition import HandlerCondition, StrictCondition


class Job:

    def __init__(self, item) -> None:
        self.item = item


class Handler(Thread, Logging, metaclass=abc.ABCMeta):

    def __init__(self, interval, description, cooldown=0,
                 inactive_interval=60):
        self._interval = 1 if amino.development else interval
        self._description = description
        self._inactive_interval = 1 if amino.development else inactive_interval
        super().__init__(name=self._description)
        self._running = True
        self._initial_wait = 5
        self._failures = 0
        self._cooldown = 0 if amino.development else cooldown
        self._last_check = {}

    def run(self):
        self.log.info('Starting {}.'.format(self._description))
        try:
            self._sanity_check()
        except SeriesDException as e:
            self.log.error('Shutting down {} with reason: {}'.format(
                self._description, e))
        else:
            self._main_loop()

    def _main_loop(self):
        next_check = datetime.now() + timedelta(seconds=self._initial_wait)
        while self._running:
            if datetime.now() > next_check:
                next_check = (self._next_check if self._check_error_wrapper()
                              else self._next_check_inactive)
            time.sleep(1)

    def stop(self):
        self._running = False

    def _check_error_wrapper(self):
        ''' *handled* is indicative of whether a candidate was found and
        processed.
        Returns *True* if there are remaining jobs in the database.
        '''
        handled = False
        try:
            handled = self._check()
        except sqlalchemy.exc.InvalidRequestError as e:
            self.log.debug(e)
        except Exception as e:
            self._failure(e)
        else:
            if handled:
                self._success()
            return handled
        return True

    def _check(self):
        with self._lock:
            ret = self._current.effect(self._process).is_just
            self._cleanup()
            return ret

    def _process(self, job):
        item = job.item
        if hasattr(item, 'id'):
            self._last_check[str(item.id)] = time.time()
        self._handle_job(job)

    def _cleanup(self):
        pass

    @property
    def _next_check(self):
        return datetime.now() + timedelta(seconds=self._interval)

    @property
    def _next_check_inactive(self):
        return datetime.now() + timedelta(seconds=self._inactive_interval)

    def _handle_job(self, job):
        return self._handle(job.item)

    def _handle(self, task):
        pass

    @property
    def _current(self):
        return self._choose(self._qualified)

    def _choose(self, qualified):
        return qualified.head

    def _cool(self, job):
        item = job.item
        return (not hasattr(item, 'id') or
                self._time_since_last(item) > self._cooldown)

    def _time_since_last(self, item):
        return time.time() - self._last_check.get(str(item.id), 0)

    def activate_id(self, id):
        if str(id) in self._last_check:
            del self._last_check[str(id)]

    @abc.abstractproperty
    def _candidates(self):
        ...

    def _qualify(self, candidate):
        return self._conditions.ev(candidate)

    def _qualify_job(self, job):
        return (self._job_conditions.get(type(job)) / __.ev(job.item) |
                (lambda: self._qualify(job.item)))

    @property
    def _qualified(self):
        def job(item):
            return item if isinstance(item, Job) else Job(item)
        return (
            List.wrap(self._candidates)
            .map(job)
            .filter(self._cool)
            .filter(self._qualify_job)
        )

    def explain(self, item):
        desc = __.describe(item, target=True)
        cond = (
            desc(self._conditions)
            if self._job_conditions.empty else
            (self._job_conditions.v / desc).join_lines
        )
        return dict(name=self._description, cond=cond)

    @property
    def _conditions(self) -> HandlerCondition:
        return StrictCondition(False)

    @property
    def _job_conditions(self):
        return Map()

    def _commit(self):
        pass

    def _sanity_check(self):
        pass

    def _failure(self, exc):
        self._failures += 1
        import traceback
        self.log.error('Error in {}:'.format(self._description))
        self.log.error(exc)
        traceback.print_exc()
        if amino.development or self._failures >= 20:
            msg = '20 failures in a row in {}, shutting down.'
            self.log.error(msg.format(self._description))
            self.stop()

    def _success(self):
        self._failures = 0

    @property
    def _lock(self):
        raise NotImplementedError('Handler._lock')

__all__ = ['Handler']
