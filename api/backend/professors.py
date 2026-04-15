from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')


@professor_bp.route('/courses', methods=['GET', 'POST'])
def professor_courses():
    if request.method == 'GET':
        professor_id = request.args.get('professor_id')
        if not professor_id:
            return jsonify({'error': 'professor_id query parameter is required'}), 400

        cursor = get_db().cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM courses WHERE professor_id = %s', (professor_id,))
            return jsonify({'courses': cursor.fetchall()}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    data = request.get_json() or {}
    required = ['professor_id', 'department_id', 'title', 'course_code']
    if not all(field in data for field in required):
        return jsonify({'error': f'Missing one of required fields: {required}'}), 400

    cursor = get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO courses (professor_id, department_id, title, course_code) VALUES (%s, %s, %s, %s)',
            (data['professor_id'], data['department_id'], data['title'], data['course_code'])
        )
        get_db().commit()
        return jsonify({'message': 'Course created', 'course_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@professor_bp.route('/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def professor_course(course_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM courses WHERE course_id = %s', (course_id,))
            course = cursor.fetchone()
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            return jsonify({'course': course}), 200

        if request.method == 'PUT':
            data = request.get_json() or {}
            updates = []
            params = []
            for field in ['title', 'course_code']:
                if field in data:
                    updates.append(f'{field} = %s')
                    params.append(data[field])
            if not updates:
                return jsonify({'error': 'No valid fields to update'}), 400
            params.append(course_id)
            cursor.execute('UPDATE courses SET ' + ', '.join(updates) + ' WHERE course_id = %s', tuple(params))
            get_db().commit()
            return jsonify({'message': 'Course updated'}), 200

        if request.method == 'DELETE':
            cursor.execute('DELETE FROM courses WHERE course_id = %s', (course_id,))
            get_db().commit()
            return jsonify({'message': 'Course deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@professor_bp.route('/courses/<course_id>/students', methods=['GET', 'POST', 'DELETE'])
def professor_course_students(course_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute(
                '''SELECT u.user_id, u.first_name, u.last_name, u.email, IFNULL(SUM(ts.duration),0) AS total_time_logged
                   FROM enrollments e
                   JOIN users u ON e.user_id = u.user_id
                   LEFT JOIN timer_sessions ts ON ts.user_id = u.user_id
                   WHERE e.course_id = %s
                   GROUP BY u.user_id, u.first_name, u.last_name, u.email''',
                (course_id,)
            )
            return jsonify({'students': cursor.fetchall()}), 200

        if request.method == 'POST':
            data = request.get_json() or {}
            user_id = data.get('user_id')
            if not user_id:
                return jsonify({'error': 'user_id is required'}), 400
            cursor.execute('INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)', (user_id, course_id))
            get_db().commit()
            return jsonify({'message': 'Student added'}), 201

        if request.method == 'DELETE':
            user_id = request.args.get('user_id') or (request.get_json() or {}).get('user_id')
            if not user_id:
                return jsonify({'error': 'user_id is required to remove student'}), 400
            cursor.execute('DELETE FROM enrollments WHERE course_id = %s AND user_id = %s', (course_id, user_id))
            get_db().commit()
            return jsonify({'message': 'Student removed'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@professor_bp.route('/courses/<course_id>/assignments', methods=['GET', 'POST'])
def professor_course_assignments(course_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM assignments WHERE course_id = %s', (course_id,))
            return jsonify({'assignments': cursor.fetchall()}), 200

        data = request.get_json() or {}
        if 'title' not in data:
            return jsonify({'error': 'title is required'}), 400

        cursor.execute(
            'INSERT INTO assignments (course_id, title, description, due_date, time_benchmark) VALUES (%s, %s, %s, %s, %s)',
            (course_id, data['title'], data.get('description'), data.get('due_date'), data.get('time_benchmark'))
        )
        get_db().commit()
        return jsonify({'message': 'Assignment created', 'assignment_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@professor_bp.route('/assignments/<assignment_id>', methods=['GET', 'PUT', 'DELETE'])
def professor_assignment(assignment_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM assignments WHERE assignment_id = %s', (assignment_id,))
            assignment = cursor.fetchone()
            if not assignment:
                return jsonify({'error': 'Assignment not found'}), 404
            return jsonify({'assignment': assignment}), 200

        if request.method == 'PUT':
            data = request.get_json() or {}
            updates = []
            params = []
            for field in ['title', 'description', 'due_date', 'time_benchmark']:
                if field in data:
                    updates.append(f'{field} = %s')
                    params.append(data[field])
            if not updates:
                return jsonify({'error': 'No valid fields to update'}), 400
            params.append(assignment_id)
            cursor.execute('UPDATE assignments SET ' + ', '.join(updates) + ' WHERE assignment_id = %s', tuple(params))
            get_db().commit()
            return jsonify({'message': 'Assignment updated'}), 200

        if request.method == 'DELETE':
            cursor.execute('DELETE FROM assignments WHERE assignment_id = %s', (assignment_id,))
            get_db().commit()
            return jsonify({'message': 'Assignment deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@professor_bp.route('/courses/<course_id>/distribution', methods=['GET'])
def professor_course_distribution(course_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT u.user_id, u.first_name, u.last_name, IFNULL(SUM(ts.duration),0) AS total_time
               FROM enrollments e
               JOIN users u ON e.user_id = u.user_id
               LEFT JOIN timer_sessions ts ON ts.user_id = u.user_id
               WHERE e.course_id = %s
               GROUP BY u.user_id, u.first_name, u.last_name''',
            (course_id,)
        )
        return jsonify({'distribution': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
