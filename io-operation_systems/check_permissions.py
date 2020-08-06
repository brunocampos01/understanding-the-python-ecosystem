import os


def check_permissions(file_path):
    """
    Args:
        :param path: path with the file, e.g. $HOME/.bashrc
    Return:
        path validated (exists and permissions)
    """
    try:
        if os.access(path, os.W_OK):
            pass
        else:
            os.chmod(path, 0o666)
    except OSError as err:
        print('IOError: ', path, err)
        raise
    else:
        return path
