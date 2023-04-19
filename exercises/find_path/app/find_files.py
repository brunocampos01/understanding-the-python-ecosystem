import argparse
import fnmatch
import os
from typing import List


def find_files(suffix: str, path: str) -> List[str]:
    """
    Find all files with a given suffix in a path and its subdirectories.
    Args:
        suffix: The suffix of the files to find.
        path: The path to search for files.
    Returns:
        A list of paths to files with the given suffix.
    """
    for entry in os.scandir(path):
        if entry.is_file() and fnmatch.fnmatch(entry.name, suffix):
            yield entry.path
        elif entry.is_dir():
            yield from find_files(suffix, entry.path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find all files with a given suffix in a path and its subdirectories.")
    parser.add_argument("suffix", type=str, help="The suffix of the files to find. Example: *.pdf")
    parser.add_argument("path", type=str, help="The path to search for files.")
    args = parser.parse_args()

    files = find_files(args.suffix, args.path)
    for file in files:
        print(file)
