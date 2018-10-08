# Write a Python program to extract and display all the header tags from www.example.com
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://www.facebook.com/?ref=cws')

# Analysis docs HTML and XML
soup = BeautifulSoup(html, "html.parser")
titles = soup.find_all(['h1', 'h2','h3','h4','h5','h6'])
print('List all the header tags :', *titles, sep='\n\n')


