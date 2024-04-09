import requests

url = 'http://127.0.0.1:5000/students/1/enroll'# the number in beetween students and enroll is the id of the student you wish to enroll in the course.
data = {
 "course_id": 2 #the number is witch course you want to add to the student.
}
response = requests.post(url, json=data)
# Check if the request was successful
print(response.json())
