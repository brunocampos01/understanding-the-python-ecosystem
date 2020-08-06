import os


here = os.path.abspath(os.path.dirname(__file__))

# good pratices to file configuration: use file .cfg, ini or json
path_config = "/conf/prod/luigi.cfg"

path_project = os.path.dirname(__file__)
path_outside = os.path.join(here + '/..')

# Use JOIN to concatenate paths
path_path_file = os.path.join(PATH_PROJECT + PATH_SCRIPT_SQL)
