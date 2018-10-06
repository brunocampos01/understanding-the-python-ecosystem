import sys
import pkgutil

from golgi.config import Config
from golgi.logging import log


def config_names(_dir):
    modules = pkgutil.walk_packages([str(_dir)], onerror=lambda x: True)
    for _l, name, ispkg in modules:
        if not ispkg and '.' in name:
            pkg, module = name.rsplit('.', 1)
            if module == 'config':
                yield pkg


def write_pkg_config(_dir, outfile, alias):
    sys.path[:0] = [str(_dir)]
    Config.allow_files = False
    Config.allow_override = False
    Config.clear_metadata()
    for name in config_names(_dir):
        try:
            Config.load_config(name)
        except Exception as e:
            log.debug(e)
    Config.reset(files=False, alias=[alias])
    Config.write_config(outfile)
