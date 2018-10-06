import sys
PY3 = sys.version_info[0] == 3

try:
    next = next
except NameError: # pragma: no cover
    # for Python 2.5
    def next(gen):
        return gen.next()

