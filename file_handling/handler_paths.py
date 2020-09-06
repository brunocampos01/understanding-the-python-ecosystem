import os


here = os.path.abspath(os.path.dirname(__file__))

# good pratices to file configuration: use file .cfg, ini or json
path_config = "/conf/prod/luigi.cfg"

path_project = os.path.dirname(__file__)
path_outside = os.path.join(here + '/..')
name_file = os.path.basename(__file__)
name_filw_without_ext = dag_id = os.path.splitext(here)[0]

# Use JOIN to concatenate paths
path_path_file = os.path.join(PATH_PROJECT + PATH_SCRIPT_SQL)
