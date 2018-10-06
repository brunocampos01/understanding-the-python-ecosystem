'''1. Write a Python program to test if a given page is found or not on the server. '''
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen('https://www.google.com')
except HTTPError as e:
    print('HTTP error')
except URLError as e:
    print('Server not found !')
else:
    print(html.read())