import traceback
import sys


def func():
    try:
        raise SomeError("Something went wrong...")
    except:
        print('traceback\n')
        traceback.print_exc(file=sys.stderr)


def func():
    try:
        raise NotImplementedError("Something went wrong...")
    except Exception as err:
        raise ('hummmm ...') from err


if __name__ == "__main__":
    func()
