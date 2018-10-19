import requests

response = requests.get('https://analytics.usa.gov/data/live/realtime.json')
response = response.json()

print("Number of people visiting a U.S. government website-")
print("Active Users Right Now:")
print(response['data'][0]['active_visitors'])