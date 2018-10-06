from os import environ

dodebug = 'PYTHONDEBUG' in environ

__all__ = ['dodebug']
