# Write a Python program to download IMDB's Top 250 data (movie name, Initial release, director name and stars).
from bs4 import BeautifulSoup
import requests

# Download IMDB's Top 250 data
response = requests.get('http://www.imdb.com/chart/top')

# create lxml to navigate in tree
soup = BeautifulSoup(response.text, 'lxml')

# navigate into <td class="titleColumn">
movies = soup.select('td.titleColumn')

# into <td class="titleColumn">, search atributes 'href' and 'title'
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

imdb = []

# Store each item into dictionary (data), then put those into a list (imdb)
for index in range(0, len(movies)):

    # Seperate movie into: 'place', 'title', 'director'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index)) + 1:-7]
    place = movie[:len(str(index)) - (len(movie))]
    data = {"movie_title": movie_title,
            "place": place,
            "star_cast": crew[index],
            "link": links[index]}
    imdb.append(data)

for item in imdb:
    print(item['place'], '-', item['movie_title'], 'Starring:', item['star_cast'])