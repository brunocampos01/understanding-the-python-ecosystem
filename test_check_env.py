from __future__ import print_function

import os
from datetime import datetime
import unittest
from pathlib import Path
from platflows.commons import metrics, global_parameters


PATH_CONF = str(Path(__file__).parent.parent.parent)


class MetricsTest(unittest.TestCase):

    # metrics
    task_id = "Agrega_ALL_APIKEYS_2019_01_02_True_adf4567d99"
    task_name = "agrega"
    env = "dev"
    date_to_run = 2019-04-22
    start_time = datetime.now()

    def test_config_file(self):
        config_file_dev = "/conf/dev/luigi.cfg"
        config_file_prod = "/conf/prod/luigi.cfg"

        assert os.path.exists(PATH_CONF + config_file_prod)
        assert os.path.exists(PATH_CONF + config_file_dev)

    def test_calculate_time(self):
        func_calculate_time = metrics.calculate_time(self.start_time)
        self.assertTrue(type(func_calculate_time) is list)

    def test_payload(self):
        func_payload = metrics.generate_payload(self.task_id,
                                                self.task_name,
                                                self.env,
                                                self.date_to_run,
                                                self.start_time)
        self.assertTrue(type(func_payload) is dict)


if __name__ == "__main__":
    unittest.main(argv='--verbose')
