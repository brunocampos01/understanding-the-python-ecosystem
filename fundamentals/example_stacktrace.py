import traceback
import sys


class SomeError(Exception):
    pass


def func_traceback():
    try:
        raise SomeError("Something went wrong...")
    except Exception:
        print('traceback\n')
        traceback.print_exc(file=sys.stderr)


def func_chained():
    try:
        raise NotImplementedError("Something went wrong...")
    except Exception as err:
        raise RuntimeError('hummmm ...') from err


if __name__ == "__main__":
    func_traceback()

    try:
        func_chained()
    except RuntimeError as e:
        print(f"Caught chained exception: {e}")
