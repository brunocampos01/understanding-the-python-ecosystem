
import pkgutil

def submodules(pkg_name):
    tip = pkg_name.rsplit('.')[-1]
    pkg = __import__(pkg_name, fromlist=tip)
    for loader, name, is_pkg in pkgutil.iter_modules(pkg.__path__):
        if not is_pkg:
            yield __import__('{0}.{1}'.format(pkg_name, name), fromlist=name) 
