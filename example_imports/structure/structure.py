# Standard library imports
import pathlib
import sys

# ----------------------------------------------------------------------------
# Local imports
# ----------------------------------------------------------------------------

# # option: 1
# import files

# option: 2
# Implicit Relative Imports.
# These were removed from the language by PEP 328
# The issue with this approach is that your
# import path can get very messy and hard to understand.
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import files

# option: 3
# from . import files

# A more common way to open data files
# is to locate them based on your module’s __file__ attribute:
import pathlib

DATA_DIR = f'{pathlib.Path(__file__).parent.parent}/data'
with open(f'{DATA_DIR}/test.xml') as fid:
    fid.read()


def main():
    # Read path from command line
    try:
        breakpoint()  # type n in PDB
        root = pathlib.Path(sys.argv[1]).resolve()
    except IndexError:
        print("Need one argument: the root of the original file tree")
        raise SystemExit()

    # Re-create the file structure
    new_root = files.unique_path(pathlib.Path.cwd(), "{:03d}")
    for path in root.rglob("*"):
        if path.is_file() and new_root not in path.parents:
            rel_path = path.relative_to(root)
            files.add_empty_file(new_root / rel_path)


if __name__ == "__main__":
    main()
