# Write a Python program to extract and display all the image links from https://en.wikipedia.org/wiki/Peter_Jeffrey.
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://en.wikipedia.org/wiki/Peter_Jeffrey')

# Create a parser instance to facilite navigating, seaching and modifying the tree
soup = BeautifulSoup(html, 'html.parser')

# find the tag : <img ... >
image_tags = soup.findAll('img')

for image in image_tags:
    print(image['src'])
