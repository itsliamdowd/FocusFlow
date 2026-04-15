from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/logs', methods=['GET'])
def admin_logs():
    institution_id = request.args.get('institution_id')
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    archived = request.args.get('archived')

    query = '''SELECT al.*, u.first_name, u.last_name, u.email, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        query += ' AND u.institution_id = %s'
        params.append(institution_id)
    if user_id:
        query += ' AND al.user_id = %s'
        params.append(user_id)
    if category:
        query += ' AND al.category = %s'
        params.append(category)
    if archived is not None:
        query += ' AND al.archived = %s'
        params.append(archived.lower() in ['1', 'true', 'yes'])

    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return jsonify({'logs': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@admin_bp.route('/logs/<log_id>', methods=['GET', 'PUT'])
def admin_log(log_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM activity_logs WHERE log_id = %s', (log_id,))
            log = cursor.fetchone()
            if not log:
                return jsonify({'error': 'Log not found'}), 404
            return jsonify({'log': log}), 200

        data = request.get_json() or {}
        updates = []
        params = []
        for field in ['duration', 'category']:
            if field in data:
                updates.append(f'{field} = %s')
                params.append(data[field])
        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400
        params.append(log_id)
        cursor.execute('UPDATE activity_logs SET ' + ', '.join(updates) + ' WHERE log_id = %s', tuple(params))
        get_db().commit()
        return jsonify({'message': 'Log updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@admin_bp.route('/logs/duplicates', methods=['GET', 'DELETE'])
def admin_logs_duplicates():
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute(
                '''SELECT al1.*
                   FROM activity_logs al1
                   JOIN activity_logs al2
                     ON al1.user_id = al2.user_id
                    AND al1.task_id = al2.task_id
                    AND al1.duration = al2.duration
                    AND DATE(al1.logged_at) = DATE(al2.logged_at)
                    AND al1.log_id <> al2.log_id
                   GROUP BY al1.log_id'''
            )
            return jsonify({'duplicates': cursor.fetchall()}), 200

        log_id = request.args.get('log_id') or (request.get_json() or {}).get('log_id')
        if not log_id:
            return jsonify({'error': 'log_id is required to delete duplicate'}), 400
        cursor.execute('DELETE FROM activity_logs WHERE log_id = %s', (log_id,))
        get_db().commit()
        return jsonify({'message': 'Duplicate deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@admin_bp.route('/logs/archive', methods=['GET', 'POST'])
def admin_logs_archive():
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT * FROM activity_logs WHERE archived = TRUE')
            return jsonify({'archived': cursor.fetchall()}), 200

        data = request.get_json() or {}
        cutoff_date = data.get('cutoff_date')
        if not cutoff_date:
            return jsonify({'error': 'cutoff_date is required'}), 400
        cursor.execute('UPDATE activity_logs SET archived = TRUE WHERE logged_at < %s', (cutoff_date,))
        get_db().commit()
        return jsonify({'message': 'Logs archived'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@admin_bp.route('/categories', methods=['GET', 'DELETE'])
def admin_categories():
    cursor = get_db().cursor(dictionary=True)
    try:
        if request.method == 'GET':
            cursor.execute('SELECT DISTINCT category FROM activity_logs')
            categories = [row['category'] for row in cursor.fetchall()]
            return jsonify({'categories': categories}), 200

        category = request.args.get('category') or (request.get_json() or {}).get('category')
        if not category:
            return jsonify({'error': 'category is required to delete logs'}), 400
        cursor.execute('DELETE FROM activity_logs WHERE category = %s', (category,))
        get_db().commit()
        return jsonify({'message': 'Logs deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@admin_bp.route('/users', methods=['GET'])
def admin_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            '''SELECT i.institution_id, i.name, COUNT(u.user_id) AS user_count
               FROM institutions i
               LEFT JOIN users u ON i.institution_id = u.institution_id
               GROUP BY i.institution_id, i.name'''
        )
        return jsonify({'users': cursor.fetchall()}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
