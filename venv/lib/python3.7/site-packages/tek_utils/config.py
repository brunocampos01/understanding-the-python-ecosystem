from sys import stdin

metadata = {
    'parents': ['golgi'],
}


def reset_config():
    interactive = stdin.isatty()
    return {'global': {'interactive': interactive}}
