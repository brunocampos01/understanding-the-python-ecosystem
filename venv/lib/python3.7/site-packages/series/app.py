import threading
import time
import importlib

from golgi.run import SignalManager

from amino import List, Map
from amino.util.string import camelcaseify
from series.logging import Logging


class App(threading.Thread, Logging):
    _components = []  # type: List[Handler]

    def __init__(self, c_module, run, omit, c_args=(), interval=0.2,
                 name='series'):
        super().__init__(name=name)
        self._c_module = c_module
        self._c_args = c_args
        self._interval = interval
        self.name = name
        self._running = False
        self.components = List()
        self.component_map = Map()
        self._init_components(run, omit)

    def run(self):
        self.register_sigint_handler()
        self.pre()
        self.main_loop()

    def pre(self):
        self.start_components()
        self.prepare()

    def prepare(self):
        pass

    def start_components(self):
        for component in self.components:
            component.start()

    def main_loop(self):
        self._running = True
        self.log.info('{} running.'.format(self.name))
        while self._running:
            time.sleep(self._interval)

    def _init_components(self, run, omit):
        components = self._components
        if run:
            components = [c for c in components if c in run]
        if omit:
            components = [c for c in components if c not in omit]
        for component in components:
            self._setup_component(component)

    def _setup_component(self, component):
        def error(exc):
            msg = 'Invalid component name: {} ({})'.format(component, exc)
            self.log.error(msg)
        mod_name = 'series.{}.{}'.format(self._c_module, component)
        try:
            module = importlib.import_module(mod_name)
        except ImportError as e:
            error(e)
        else:
            try:
                Component = getattr(module, camelcaseify(component))
            except AttributeError as e:
                error(e)
            else:
                instance = Component(*self._c_args)
                setattr(self, component, instance)
                self.components.append(instance)
                self.component_map[component] = instance

    def register_sigint_handler(self):
        SignalManager.instance.sigint(self.interrupt)

    def interrupt(self, signum=10, frame=None):
        self._stop_components()
        self._join_threads()
        self._cleanup()
        self._running = False
        self.log.info('{} shut down due to SIGINT.'.format(self.name))

    def _stop_components(self):
        for component in self.components:
            component.stop()

    def _join_threads(self):
        for component in self.components:
            if component.is_alive():
                component.join()

    def _cleanup(self):
        pass

    def component(self, name):
        return self.component_map.get(name)

__all__ = ['App']
