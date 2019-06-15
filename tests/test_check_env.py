from __future__ import print_function

import os
import unittest
from pathlib import Path

PATH_CONF = str(Path(__file__).parent.parent.parent)


class MetricsTest(unittest.TestCase):

    @staticmethod
    def test_config_file():
        config_file_dev = "/conf/dev/luigi.cfg"
        config_file_prod = "/conf/prod/luigi.cfg"

        if not os.path.exists(PATH_CONF + config_file_prod):
            raise AssertionError()

        if not os.path.exists(PATH_CONF + config_file_dev):
            raise AssertionError()


if __name__ == "__main__":
    unittest.main()
