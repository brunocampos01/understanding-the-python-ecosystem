import time
import requests


URL_CLIENTS = ""
TIMEOUT = 5
MAX_RETRIES = 1


def retry(url, timeout, max_retries, user, password):
   """
   Function to retry connection in url
   """
   for retry in range(0, max_retries):
      r = requests.get(url,
                        timeout=timeout,
                        auth=(user, password))

      if r.status_code == 200:
         return r.json()
      else:
         print('Retry: ', retry)
         time.sleep(timeout)

   raise Exception('Request Error in ', url)




    def __init__(self, db_hostname, user, password, connection_timeout, limit_retries):
        self.db_hostname = db_hostname
        self.user = user
        self.password = password
        self.connection_timeout = connection_timeout
        self.limit_retries = limit_retries
        
        
    def connect_db(self, limit_retries, timeout):
        """
        :return: object of connection
        """
        for retry in xrange(0, limit_retries):
            try:
                mysql.connector.connect(host=self.db_hostname,
                                        user=self.user,
                                        passwd=self.password,
                                        connection_timeout=self.connection_timeout,
                                        get_warnings=True)
            except mysql.connector.Error:

                if retry <= limit_retries:
                    retry += 1
                    logging.error("Connection failed. Retry [%s / %s]" % (retry, limit_retries))
                    time.sleep(timeout)

                else:
                    logging.exception("Connection failed: "
                                      "db_hostname: %s, user: %s, password: %s, "
                                      "connection_timeout: %s, limit_retries: %s"
                                      % (self.db_hostname,
                                         self.user,
                                         self.password,
                                         self.connection_timeout,
                                         self.limit_retries))


        raise Exception('Retries FAILED !')
