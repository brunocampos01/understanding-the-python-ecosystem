# Write a Python program to download and display the content of https://en.wikipedia.org/robots.txt.
import requests

response = requests.get('https://en.wikipedia.org/robots.txt')
text = response.text

# Analysis http
print(response.status_code)
print(response.encoding)
print(response.request)

print("\nrobots.txt for http://www.wikipedia.org/")
print("===================================================")
print(text)