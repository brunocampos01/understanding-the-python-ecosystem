# Write a Python program to extract and display all the header tags from en.wikipedia.org/wiki/Main_Page.
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://en.wikipedia.org/wiki/Main_Page')

# Create a parser instance to facilite navigating, seaching and modifying the tree
bs = BeautifulSoup(html, 'html.parser')

# find elements
titles = bs.find_all(['h1', 'h2','h3','h4','h5','h6'])
print('List all the header tags :', *titles, sep='\n\n')