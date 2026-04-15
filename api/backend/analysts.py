from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

analyst_bp = Blueprint('analyst', __name__, url_prefix='/analyst')


@analyst_bp.route('/activity', methods=['GET'])
def analyst_activity():
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    query = '''SELECT al.*, u.first_name, u.last_name, u.email, u.major, u.year, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        query += ' AND u.institution_id = %s'
        params.append(institution_id)
    if major:
        query += ' AND u.major = %s'
        params.append(major)
    if year:
        query += ' AND u.year = %s'
        params.append(year)

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return jsonify({'activity': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/activity/<log_id>', methods=['GET', 'PUT'])
def analyst_activity_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM activity_logs WHERE log_id = %s', (log_id,))
            log = cursor.fetchone()
            if not log:
                return jsonify({'error': 'Log not found'}), 404
            return jsonify({'log': log}), 200

        data = request.get_json() or {}
        if 'is_anomalous' not in data:
            return jsonify({'error': 'is_anomalous is required'}), 400
        cursor.execute('UPDATE activity_logs SET archived = TRUE WHERE log_id = %s', (log_id,))
        get_db().commit()
        return jsonify({'message': 'Log marked anomalous'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/correlations', methods=['GET'])
def analyst_correlations():
    institution_id = request.args.get('institution_id')
    query = '''SELECT u.user_id, u.first_name, u.last_name,
               COALESCE(SUM(al.duration),0) AS total_minutes,
               COALESCE(AVG(ps.score),0) AS avg_productivity
               FROM users u
               LEFT JOIN activity_logs al ON u.user_id = al.user_id
               LEFT JOIN productivity_scores ps ON u.user_id = ps.user_id'''
    params = []
    if institution_id:
        query += ' WHERE u.institution_id = %s'
        params.append(institution_id)
    query += ' GROUP BY u.user_id, u.first_name, u.last_name'

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return jsonify({'correlations': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/breakdown', methods=['GET'])
def analyst_breakdown():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id query parameter is required'}), 400

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            'SELECT category, SUM(duration) AS total_minutes FROM activity_logs WHERE user_id = %s GROUP BY category',
            (user_id,)
        )
        return jsonify({'breakdown': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/institutions', methods=['GET'])
def analyst_institutions():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('SELECT institution_id, name, type FROM institutions')
        return jsonify({'institutions': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/export', methods=['GET'])
def analyst_export():
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    query = '''SELECT al.*, u.first_name, u.last_name, u.email, u.major, u.year, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        query += ' AND u.institution_id = %s'
        params.append(institution_id)
    if major:
        query += ' AND u.major = %s'
        params.append(major)
    if year:
        query += ' AND u.year = %s'
        params.append(year)

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return jsonify({'export': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@analyst_bp.route('/shared', methods=['GET'])
def analyst_shared():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT u.institution_id, COUNT(*) AS log_count, SUM(al.duration) AS total_duration
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE al.archived = FALSE
               GROUP BY u.institution_id'''
        )
        return jsonify({'shared': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
