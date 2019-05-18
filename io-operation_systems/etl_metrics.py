# -*- coding: utf-8 -*-
import os
import argparse

import mysql.connector
import configparser

path_directory = os.path.dirname(os.path.abspath(__file__))
path_config = ''.join(path_directory + '/config_mysql.ini')

config = configparser.ConfigParser()
config.read(path_config)

MYSQL_USER = config['ConnectDB']['MYSQL_USER']
MYSQL_PASSWORD = config['ConnectDB']['MYSQL_PASSWORD']
MYSQL_HOST = config['ConnectDB']['MYSQL_HOST']
MYSQL_DB_NAME = config['ConnectDB']['MYSQL_DB_NAME']
CONNECTION_TIMEOUT = config['ConnectDB']['CONNECTION_TIMEOUT']
ATTEMPTS = config['ConnectDB']['ATTEMPTS']
DELAY = config['ConnectDB']['DELAY']


class MySQLHelper(object):

    def __init__(self, hostname: str, user: str, password: str,
                 connection_timeout: str, attemps: int, delay: int):
        self.__conn = self.try_conn(hostname=hostname, user=user,
                                    password=password,
                                    connection_timeout=connection_timeout,
                                    attempts=attemps, delay=delay)
        self.__cursor = self.__conn.cursor(buffered=True)

    def __del__(self):
        self.__conn.close()
        self.__cursor.close()

    def try_conn(self, hostname: str, user: str, password: str,
                 connection_timeout: str, attempts: int, delay: int):
        """
        Function to try connection in db.
        If exception, execute function ping which retry connection.
        db.ping(reconnect=True) says to reconnect to DB

        Args
            :param hostname: url/ip SGBD
            :param user: user with access db
            :param password: key of user
            :param connection_timeout: time to wait response SGBD
            :param attempts: tentatives of connection
            :param delay: time to wait between attempts

        Return
            object connection
        """
        try:
            return mysql.connector.connect(host=hostname,
                                           user=user,
                                           passwd=password,
                                           connection_timeout=
                                           int(connection_timeout),
                                           get_warnings=True,
                                           autocommit=True)

        except mysql.connector.errors as err:
            print("Connection failed: {1}\nretry ...").format(err)
            self.__conn.ping(reconnect=True, attempts=attempts,
                             delay=delay)

    def with_database(self, name_db: str):
        """
        :param name_db: database name
        :return: reference of object which it was called
        """
        try:
            self.__cursor.execute("USE %s;" % name_db)
            return self
        except mysql.connector.Error as err:
            print("Failed execute query: %s, name: %s" % (err,
                                                          name_db))
            raise

    def execute_statement(self, table):
        """
        :param query: query SQL
        :return: reference of object which it was called
        """
        try:
            self.__cursor.execute('SELECT * FROM {};'.format(table))
            print(self.__cursor.fetchall())
        except mysql.connector.Error as err:
            print("Failed execute query: %s" % err)
            raise


def main():
    """
    Consult data base
    :return: Query with ETL metrics\n\n
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--version', action='version', version='1.0.0')
    parser.add_argument('-sd', type=str, action='store', required=True,
                        help='Start date, e.g 2019-05-30')
    parser.add_argument('-ed', type=str, action='store', required=True,
                        help='End date including, e.g 2019-05-31')
    parser.add_argument('-table', type=str, action='store', required=True,
                        help='Choose which table [modules, jobs]')
    parser.add_argument('-status', type=str, action='store',
                        help='Status of modules/jobs')

    arguments = parser.parse_args()
    print('Args = ', arguments)

    MySQLHelper(hostname=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                connection_timeout=CONNECTION_TIMEOUT,
                attemps=ATTEMPTS,
                delay=DELAY)\
        .with_database(MYSQL_DB_NAME)\
        .execute_statement(table=arguments.table)


if __name__ == "__main__":
    main()
