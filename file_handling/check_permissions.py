import os


def check_permissions(file_path):
    """
    Args:
        :param path: path with the file, e.g. $HOME/.bashrc
    Return:
        path validated (exists and permissions)
    """
    try:
        if os.access(file_path, os.W_OK):
            pass
        else:
            os.chmod(file_path, 0o666)
    except OSError as err:
        print('IOError: ', file_path, err)
        raise
    else:
        return file_path
