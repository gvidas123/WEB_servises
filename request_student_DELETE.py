import requests
#in the url the lst number is the student being deleted. if the last number and dash are eremoved it will deleta all students
url = 'http://127.0.0.1:5000/students'
requests.delete(url)