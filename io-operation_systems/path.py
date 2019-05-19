import os
import configparser


PATH_PROJECT = os.path.dirname(__file__)
PATH_CONFIG = "/conf/prod/luigi.cfg"

config = configparser.ConfigParser()
config.read(PATH_PROJECT + PATH_CONFIG)

MYSQL_USER = config['RDSMySQL']['MYSQL_USER']
MYSQL_PASSWORD = config['RDSMySQL']['MYSQL_PASSWORD']
HOST_MYSQL = config['RDSMySQL']['HOST_MYSQL']
MYSQL_DB_NAME = config['RDSMySQL']['MYSQL_DB_NAME']
PATH_SCRIPT_SQL = config['RDSMySQL']['PATH_SCRIPT_SQL']

PATH_SCRIPT_JOIN = os.path.join(PATH_PROJECT + PATH_SCRIPT_SQL)

# Use JOIN to concatenate paths
