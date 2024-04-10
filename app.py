from flask import request, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import declarative_base

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)
Base = declarative_base()


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    students = db.relationship('Student', secondary='enrolment', back_populates='courses')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    courses = db.relationship('Course', secondary='enrolment', back_populates='students')


class Enrolment(db.Model):
    student = db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True)
    course = db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)


@flask_app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    output = []

    for student in students:
        student_data = {
            'id': student.id,
            'name': student.name,
            'email': student.email,
            'courses': [course.title for course in student.courses]
        }
        output.append(student_data)

    return jsonify({'students': output})


@flask_app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    output = [{'id': course.id, 'title': course.title, 'description': course.description} for course in courses]
    return jsonify({'courses': output})


@flask_app.route('/enrolments', methods=['GET'])
def get_enrolment():
    students = Enrolment.query.all()
    output = [{'student': student.student, 'course': student.course, } for student in students]
    return jsonify({'enrolled': output})


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


@flask_app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    print("XD ADD")
    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    new_student = Student(name=name, email=email)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully', 'student': {'id': new_student.id, 'name': new_student.name, 'email': new_student.email}})


@flask_app.route('/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    data = request.json
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({'error': 'Course ID is required'}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    student.courses.append(course)

    db.session.commit()
    return jsonify({'message': f'Student with ID {student_id} enrolled in course with ID {course_id} successfully'})


@flask_app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    data = request.json
    name = data.get('name')
    email = data.get('email')

    if name:
        student.name = name

    if email:
        student.email = email

    db.session.commit()

    return jsonify({'message': f'Student with ID {student_id} updated successfully'})


@flask_app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    data = request.json
    title = data.get('title')
    description = data.get('description')

    if title:
        course.title = title
    if description:
        course.description = description

    db.session.commit()

    return jsonify({'message': f'Course with ID {course_id} updated successfully'})


@flask_app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({'message': f'Student with ID {student_id} deleted successfully'})


@flask_app.route('/students', methods=['DELETE'])
def delete_all_students():
    # Delete all students from the database
    num_deleted = Student.query.delete()
    db.session.commit()

    return jsonify({'message': f'{num_deleted} students deleted successfully'})


@flask_app.route('/courses', methods=['DELETE'])
def delete_all_courses():
    # Delete all students from the database
    num_deleted = Course.query.delete()
    db.session.commit()
    return jsonify({'message': f'{num_deleted} students deleted successfully'})


@flask_app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': f'Course with ID {course_id} deleted successfully'})


@flask_app.route('/students/<int:student_id>/enroll/<int:course_id>', methods=['DELETE'])
def un_enroll_student(student_id, course_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    if course not in student.courses:
        return jsonify({'error': 'Student is not enrolled in this course'}), 400

    student.courses.remove(course)
    db.session.commit()

    return jsonify({'message': f'Student with ID {student_id} un enrolled from course with ID {course_id} successfully'})





if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')
