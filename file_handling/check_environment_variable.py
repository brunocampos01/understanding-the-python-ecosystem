import os

LANGUAGE = os.getenv('LANGUAGE')
SHELL = os.getenv('SHELL')


def check_env(var):
    """
    Function to check if env exists
    """
    try:
        print('Environment Varible: ', var)
        return os.environ[var]
    except KeyError("Not found environment variable: %s" % var):
        raise


if '__name__' == '__main__':
    check_env(LANGUAGE)
    check_env(SHELL)
