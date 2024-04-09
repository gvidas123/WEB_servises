import requests

url = 'http://127.0.0.1:5000/courses/2'  #with id being the last number in the url
data = {
    'title': 'mathamatics',
    'description': 'Real'
}
response = requests.put(url, json=data)

print(response.json())