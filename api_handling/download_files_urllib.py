import hashlib
import os
from urllib.request import urlretrieve


def download(url: str, file: str):
    """
    Download file from <url>

    :param url: URL to file
    :param file: Local file path
    """
    if not os.path.isfile(file):
        print('Downloading ' + file + '...')
        urlretrieve(url, file)
        print('Download Finished')


def check_files(file_name: str, checksum: str):
    # Make sure the files aren't corrupted
    assert hashlib.md5(open(file_name, 'rb').read()) \
               .hexdigest() == checksum, \
                    f'{file_name} file is corrupted.  Remove the file and ' \
                    f'try again.'


def main():
    # Download the training and test dataset.
    download(url='https://s3.amazonaws.com/udacity-sdc/notMNIST_train.zip',
             file='notMNIST_train.zip')
    download(url='https://s3.amazonaws.com/udacity-sdc/notMNIST_test.zip',
             file='notMNIST_test.zip')

    check_files(file_name='notMNIST_train.zip',
                checksum='c8673b3f28f489e9cdf3a3d74e2ac8fa')
    check_files(file_name='notMNIST_test.zip',
                checksum='5d3c7e653e63471c88df796156a9dfa9')
    # Wait until you see that all files have been downloaded.
    print('All files downloaded.')


if __name__ == '__main__':
    main()
