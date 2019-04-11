import os
import sys
import time
import requests


URL_CLIENTS = ""
TIMEOUT = 5
MAX_RETRIES = 1
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']

def check_env(var):
   """
   Function to check if env exists
   """
   try:
      os.environ[var]
   except KeyError:
      print("Not found environment variable: ", var)
      sys.exit(1)

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
