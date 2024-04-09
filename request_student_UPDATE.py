import requests
#url = 'http://127.0.0.1:5000/students/<student:id>'
url = 'http://127.0.0.1:5000/students/2'  #with id being the last number in the url
data = {
    'name': 'John',
    'email': 'Wick@lol',
}
response = requests.put(url, json=data)

print(response.json())