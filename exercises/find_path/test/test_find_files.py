import os
import tempfile
import unittest

from first_exercise.app.find_files import find_files


class TestFindFiles(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and some files for testing.
        self.tempdir = tempfile.TemporaryDirectory()
        self.dirpath = self.tempdir.name
        self.filepaths = [
            os.path.join(self.dirpath, "file1.txt"),
            os.path.join(self.dirpath, "file2.log"),
            os.path.join(self.dirpath, "subdir1", "file3.log"),
            os.path.join(self.dirpath, "subdir1", "file4.txt"),
            os.path.join(self.dirpath, "subdir2", "file5.log"),
        ]
        os.makedirs(os.path.join(self.dirpath, "subdir1"))
        os.makedirs(os.path.join(self.dirpath, "subdir2"))
        for filepath in self.filepaths:
            with open(filepath, "w") as f:
                f.write("test")

    def tearDown(self):
        # Clean up the temporary directory and files.
        self.tempdir.cleanup()

    def test_positive(self):
        # Test that the function returns the correct file paths for a directory with matching files.
        result = list(find_files("*.log", self.dirpath)).sort()
        expected = [os.path.join(self.dirpath, "file2.log"),
                    os.path.join(self.dirpath, "subdir1", "file3.log"),
                    os.path.join(self.dirpath, "subdir2", "file5.log")].sort()
        self.assertEqual(result, expected)

    def test_without_matching(self):
        # Test that the function returns an empty list for a directory without matching files.
        result = list(find_files("*.pdf", self.dirpath))
        expected = []
        self.assertEqual(result, expected)
    
    def test_empty_suffix(self):
        # Test with empty suffix
        result = list(find_files('', './'))
        expected = []
        self.assertEqual(result, expected)

    def test_not_found_path(self):
        # Test with an invalid path.
        with self.assertRaises(FileNotFoundError):
            list(find_files(".txt", "/invalid/path"))

    def test_invalid_path(self):
        # Test with invalid arguments
        with self.assertRaises(OSError):
            list(find_files('.txt', 123))


if __name__ == "__main__":
    unittest.main()
