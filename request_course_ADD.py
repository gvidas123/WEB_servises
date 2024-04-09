import requests

url = 'http://127.0.0.1:5000/courses'
data = {
    'title': 'Geo',
    'description': 'its A Geo course',
}
response = requests.post(url, json=data)

print(response.json())