from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://en.wikipedia.org/wiki/Python')

# Create a parser instance
links = BeautifulSoup(html, "html.parser")

# find all
for link in links.find_all('a'):
    if 'href' in link.attrs:
        print(link.attrs['href'])