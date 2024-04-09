import requests
#in the url the lst number is the course being deleted. if the number and the last dash are removed it will delete all courses
url = 'http://127.0.0.1:5000/courses'
requests.delete(url)