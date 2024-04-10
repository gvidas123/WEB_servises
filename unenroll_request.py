import requests
#url = 'http://127.0.0.1:5000/courses/students/<int:student_id>/un_enroll/<int:course_id>'
url = 'http://127.0.0.1:5000/courses/students/2/enroll/2'

response = requests.delete(url)

print(response.json())