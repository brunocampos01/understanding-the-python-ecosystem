import os


def drop_file(path):
    """
    Drop each execution the file
    """
    try:
        if os.path.exists(path):
            os.remove(path)

    except IOError as err:
        print ('IOError: ', err)
        pass
