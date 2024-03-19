from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)


@flask_app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    new_student = Student(name=name, email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully', 'student': {'id': new_student.id, 'name': new_student.name, 'email': new_student.email}})


@flask_app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []
    for student in students:
        student_data = {'id': student.id, 'name': student.name, 'email': student.email}
        output.append(student_data)
    return jsonify({'students': output})


@flask_app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    # Query the database to find the student with the specified ID
    student = Student.query.get(student_id)

    # Check if the student exists
    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    # Extract updated data from the request JSON
    data = request.json
    name = data.get('name')
    email = data.get('email')

    # Update student data if provided
    if name:
        student.name = name
    if email:
        student.email = email

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': f'Student with ID {student_id} updated successfully'})


@flask_app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):

    course = Course.query.get(course_id)

    if course is None:
        return jsonify({'error': 'Course not found'}), 404

    # Delete the course from the database
    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': f'Course with ID {course_id} deleted successfully'})


@flask_app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': f'Student with ID {student_id} deleted successfully'})


@flask_app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    output = []
    for course in courses:
        course_data = {'description': course.description, 'title': course.title, 'id': course.id}
        output.append(course_data)
    return jsonify({'courses': output})


@flask_app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)

    if course is None:
        return jsonify({'error': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': f'Course with ID {course_id} deleted successfully'})


@flask_app.route('/courses', methods=['POST'])
def add_course():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    new_course = Course(title=title, description=description)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Course added successfully', 'course': {'id': new_course.id, 'title': new_course.title, 'description': new_course.description}})


@flask_app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    # Query the database to find the course with the specified ID
    course = Course.query.get(course_id)

    # Check if the course exists
    if course is None:
        return jsonify({'error': 'Course not found'}), 404

    # Extract updated data from the request JSON
    data = request.json
    title = data.get('title')
    description = data.get('description')

    # Update course data if provided
    if title:
        course.title = title
    if description:
        course.description = description

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': f'Course with ID {course_id} updated successfully'})


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)


if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')
