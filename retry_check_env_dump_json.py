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
