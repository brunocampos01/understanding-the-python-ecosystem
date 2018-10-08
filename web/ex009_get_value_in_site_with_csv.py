# https://bit.ly/2NyxdAG
import csv
import requests

response = requests.get('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.csv')

rows = list(csv.DictReader(response.text.splitlines()))
print("The number of magnitude 4.5+ earthquakes detected worldwide by the USGS:", len(rows))
