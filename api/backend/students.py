from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

student_bp = Blueprint('student', __name__, url_prefix='/student')


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


@student_bp.route('/tasks', methods=['GET', 'POST'])
def student_tasks():
    if request.method == 'GET':
        user_id = parse_int(request.args.get('user_id'))
        if user_id is None:
            return jsonify({'error': 'user_id query parameter is required'}), 400

        category = request.args.get('category')
        status = request.args.get('status')
        query = 'SELECT * FROM tasks WHERE user_id = %s'
        params = [user_id]

        if category:
            query += ' AND category = %s'
            params.append(category)
        if status:
            query += ' AND status = %s'
            params.append(status)

        cursor = get_db().cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return jsonify({'tasks': cursor.fetchall()}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    data = request.get_json() or {}
    user_id = parse_int(data.get('user_id'))
    title = data.get('title')
    category = data.get('category')
    priority = data.get('priority')
    time_allocated = data.get('time_allocated')
    assignment_id = data.get('assignment_id')

    if user_id is None or not title or not category:
        return jsonify({'error': 'user_id, title, and category are required'}), 400

    cursor = get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO tasks (user_id, assignment_id, title, category, priority, time_allocated) VALUES (%s, %s, %s, %s, %s, %s)',
            (user_id, assignment_id, title, category, priority, time_allocated)
        )
        get_db().commit()
        return jsonify({'message': 'Task created', 'task_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@student_bp.route('/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def student_task(task_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM tasks WHERE task_id = %s', (task_id,))
            task = cursor.fetchone()
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            return jsonify({'task': task}), 200

        if request.method == 'PUT':
            data = request.get_json() or {}
            updates = []
            params = []
            for field in ['status', 'priority', 'time_allocated']:
                if field in data:
                    updates.append(f'{field} = %s')
                    params.append(data[field])
            if not updates:
                return jsonify({'error': 'No valid fields to update'}), 400
            params.append(task_id)
            cursor.execute('UPDATE tasks SET ' + ', '.join(updates) + ' WHERE task_id = %s', tuple(params))
            get_db().commit()
            return jsonify({'message': 'Task updated'}), 200

        if request.method == 'DELETE':
            cursor.execute('DELETE FROM tasks WHERE task_id = %s', (task_id,))
            get_db().commit()
            return jsonify({'message': 'Task deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@student_bp.route('/tasks/<task_id>/sessions', methods=['GET', 'POST', 'PUT'])
def student_task_sessions(task_id):
    if request.method == 'GET':
        cursor = get_db().cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM timer_sessions WHERE task_id = %s', (task_id,))
            sessions = cursor.fetchall()
            cursor.execute('SELECT COALESCE(SUM(duration), 0) AS total_time FROM timer_sessions WHERE task_id = %s', (task_id,))
            total_time = cursor.fetchone()['total_time']
            return jsonify({'sessions': sessions, 'total_time': total_time}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    data = request.get_json() or {}
    if request.method == 'POST':
        user_id = parse_int(data.get('user_id'))
        start_time = data.get('start_time')
        session_type = data.get('session_type')
        duration = data.get('duration')

        if user_id is None or not start_time or not session_type:
            return jsonify({'error': 'user_id, start_time, and session_type are required'}), 400

        cursor = get_db().cursor()
        try:
            cursor.execute(
                'INSERT INTO timer_sessions (task_id, user_id, start_time, end_time, duration, session_type) VALUES (%s, %s, %s, %s, %s, %s)',
                (task_id, user_id, start_time, None, duration, session_type)
            )
            get_db().commit()
            return jsonify({'message': 'Session started', 'session_id': cursor.lastrowid}), 201
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

    if request.method == 'PUT':
        session_id = parse_int(data.get('session_id'))
        end_time = data.get('end_time')
        duration = data.get('duration')
        if session_id is None or not end_time or duration is None:
            return jsonify({'error': 'session_id, end_time, and duration are required'}), 400

        cursor = get_db().cursor()
        try:
            cursor.execute(
                'UPDATE timer_sessions SET end_time = %s, duration = %s WHERE session_id = %s AND task_id = %s',
                (end_time, duration, session_id, task_id)
            )
            if cursor.rowcount == 0:
                return jsonify({'error': 'Session not found'}), 404
            get_db().commit()
            return jsonify({'message': 'Session updated'}), 200
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()


@student_bp.route('/productivity', methods=['GET'])
def student_productivity():
    user_id = parse_int(request.args.get('user_id'))
    if user_id is None:
        return jsonify({'error': 'user_id query parameter is required'}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM productivity_scores WHERE user_id = %s ORDER BY week_start_date', (user_id,))
        return jsonify({'productivity': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@student_bp.route('/leaderboard', methods=['GET'])
def student_leaderboard():
    institution_id = parse_int(request.args.get('institution_id'))
    if institution_id is None:
        return jsonify({'error': 'institution_id query parameter is required'}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT u.user_id, u.first_name, u.last_name, AVG(p.score) AS avg_score
               FROM users u
               JOIN productivity_scores p ON u.user_id = p.user_id
               WHERE u.institution_id = %s
               GROUP BY u.user_id, u.first_name, u.last_name
               ORDER BY avg_score DESC''',
            (institution_id,)
        )
        return jsonify({'leaderboard': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@student_bp.route('/courses', methods=['GET'])
def student_courses():
    user_id = parse_int(request.args.get('user_id'))
    if user_id is None:
        return jsonify({'error': 'user_id query parameter is required'}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT c.*
               FROM courses c
               JOIN enrollments e ON c.course_id = e.course_id
               WHERE e.user_id = %s''',
            (user_id,)
        )
        return jsonify({'courses': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@student_bp.route('/activity', methods=['GET'])
def student_activity():
    user_id = parse_int(request.args.get('user_id'))
    if user_id is None:
        return jsonify({'error': 'user_id query parameter is required'}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT category, DATE(logged_at) AS log_date, SUM(duration) AS total_duration
               FROM activity_logs
               WHERE user_id = %s
               GROUP BY category, DATE(logged_at)
               ORDER BY DATE(logged_at) DESC''',
            (user_id,)
        )
        return jsonify({'activity': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
