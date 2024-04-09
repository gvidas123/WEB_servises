import requests

url = 'http://127.0.0.1:5000/students'
data = {
    'name': 'Beatrice',
    'email': 'Beatrice@lol.com',
}
response = requests.post(url, json=data)

print(response.json())