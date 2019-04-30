import logging
import configparser
import mysql.connector
from pathlib import Path


PATH_PROJECT = str(Path(__file__).parent.parent.parent)
PATH_CONFIG = "/conf/prod/luigi.cfg"

config = configparser.ConfigParser()
config.read(PATH_PROJECT + PATH_CONFIG)

MYSQL_USER_COCKPIT = config['RDSMySQL']['']
MYSQL_PASSWORD_COCKPIT = config['RDSMySQL']['']
MYSQL_USER = config['RDSMySQL']['']
MYSQL_PASSWORD = config['RDSMySQL']['']
HOST_MYSQL = config['RDSMySQL']['']
MYSQL_DB_NAME = config['RDSMySQL']['']
PATH_SCRIPT_SQL = config['RDSMySQL']['']

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


def read_script_sql(path):
    """
    :param path: file script sql
    :return: object with querys of script sql
    """
    try:
        return [query.strip() for query in open(path, 'r').read().strip().split(';')]
    except IOError:
        logging.exception("Failed of read in file %s:", path)


def manager_cnx(host, user, password):
    """
    :return: object of connection
    """
    logging.info('Mysql trying to connect in %s', host)
    try:
        cnx = mysql.connector.connect(host=host,
                                      user=user,
                                      passwd=password,
                                      connection_timeout=30,
                                      get_warnings=True)
        return cnx
    except mysql.connector.Error:
        logging.exception("Connection failed: ")


def create_user(database, host, creater, pw_creater, user, password):
    """
    :param database: database's name
    :param host: DNS
    :param creater: user's name exists
    :param pw_creater: user's password exists
    :param user: name of new user
    :param password: key of new user
    :return: None
    """
    logging.info("Creating user %s", user)

    query_create = "CREATE USER'{}'@'%' IDENTIFIED BY '{}';".format(user, password)
    query_grant = "GRANT ALL PRIVILEGES ON {}.* TO '{}'@'%';".format(database, user)
    query_load_permissions = "FLUSH PRIVILEGES;"
    query_list = [query_create, query_grant, query_load_permissions]

    cnx = manager_cnx(host=host, user=creater, password=pw_creater)
    cursor = cnx.cursor(buffered=True)

    for query in query_list:
        try:
            cursor.execute(query)
        except mysql.connector.Error:
            logging.error("Failed creating user:"
                          "\ndatabase: %s, host: %s, creater: %s, pw_creater: %s, user: %s, password: %s"
                          "\nquery: %s"
                          % (database, host, creater, pw_creater, user, password, query))
            raise

    close_conn(connection=cnx, cursor=cursor)


def create_databases(host, user, password, db_name):
    """
    :param host: DNS, get config file
    :param user: get config file
    :param password: get config file
    :param db_name: get config file
    :return: None
    """
    logging.info("Creating database %s", db_name)

    cnx = manager_cnx(host, user, password)
    cursor = cnx.cursor(buffered=True)

    try:
        cursor.execute("CREATE DATABASE {};".format(db_name))
    except mysql.connector.Error:
        logging.error("Failed creating database:\nhost: %s, user: %s, password: %s, db_name: %s"
                      % (host, user, password, db_name))
        raise
    finally:
        close_conn(connection=cnx, cursor=cursor)


def create_tables(host, user, password, path_script):
    """
    :param path_script: get config file
    :param host: get config file
    :param user: get config file
    :param password: get config file
    :return: None
    """
    logging.info("Creating tables ...")

    cnx = manager_cnx(host, user, password)
    cursor = cnx.cursor(buffered=True)
    querys_script = read_script_sql(path_script)

    for query in querys_script:
        try:
            cursor.execute(query)
        except mysql.connector.Error:
            logging.error("Failed creating tables, query: [%s]"
                          "\nhost: %s, user: %s, password: %s, path_script: %s"
                          % (query, host, user, password, path_script))
            raise
    close_conn(connection=cnx, cursor=cursor)


def close_conn(connection, cursor):
    connection.close()
    cursor.close()


# run
if __name__ == "__main__":
    """
    Running this file to create USER, DATABASE and TABLES
    """
    create_user(database=MYSQL_DB_NAME,
                host=HOST_MYSQL,
                creater=MYSQL_USER_COCKPIT,
                pw_creater=MYSQL_PASSWORD_COCKPIT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD)

    create_databases(user=MYSQL_USER,
                     password=MYSQL_PASSWORD,
                     host=HOST_MYSQL,
                     db_name=MYSQL_DB_NAME)

    create_tables(user=MYSQL_USER,
                  password=MYSQL_PASSWORD,
                  host=HOST_MYSQL,
                  path_script=PATH_PROJECT+PATH_SCRIPT_SQL)
