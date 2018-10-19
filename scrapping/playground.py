import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.crummy.com/software/BeautifulSoup/')

# create parser
soup = BeautifulSoup(response.content, "html.parser")

link = soup.find_all("a")

for i in link:
    if 'href' in i.attrs:
        print(i.attrs['href'])