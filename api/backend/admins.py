from flask import Blueprint, jsonify, request
from backend.db_utils import safe_db, query, query_one, execute, insert

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/logs', methods=['GET'])
@safe_db
def admin_logs():
    institution_id = request.args.get('institution_id')
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    archived = request.args.get('archived')

    sql = '''SELECT al.*, u.first_name, u.last_name, u.email, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        sql += ' AND u.institution_id = %s'
        params.append(institution_id)
    if user_id:
        sql += ' AND al.user_id = %s'
        params.append(user_id)
    if category:
        sql += ' AND al.category = %s'
        params.append(category)
    if archived is not None:
        sql += ' AND al.archived = %s'
        params.append(archived.lower() in ['1', 'true', 'yes'])

    return jsonify({'logs': query(sql, tuple(params))}), 200


@admin_bp.route('/logs/<log_id>', methods=['GET', 'PUT'])
@safe_db
def admin_log(log_id):
    if request.method == 'GET':
        log = query_one('SELECT * FROM activity_logs WHERE log_id = %s', (log_id,))
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
    rowcount = execute('UPDATE activity_logs SET ' + ', '.join(updates) + ' WHERE log_id = %s', tuple(params), commit=True)
    if rowcount == 0:
        return jsonify({'error': 'Log not found'}), 404
    return jsonify({'message': 'Log updated'}), 200


@admin_bp.route('/logs/duplicates', methods=['GET', 'DELETE'])
@safe_db
def admin_logs_duplicates():
    if request.method == 'GET':
        return jsonify({'duplicates': query(
            '''SELECT al1.*
               FROM activity_logs al1
               JOIN activity_logs al2
                 ON al1.user_id = al2.user_id
                AND al1.task_id = al2.task_id
                AND al1.duration = al2.duration
                AND DATE(al1.logged_at) = DATE(al2.logged_at)
                AND al1.log_id <> al2.log_id
               GROUP BY al1.log_id'''
        )}), 200

    log_id = request.args.get('log_id') or (request.get_json() or {}).get('log_id')
    if not log_id:
        return jsonify({'error': 'log_id is required to delete duplicate'}), 400
    rowcount = execute('DELETE FROM activity_logs WHERE log_id = %s', (log_id,), commit=True)
    if rowcount == 0:
        return jsonify({'error': 'Duplicate log not found'}), 404
    return jsonify({'message': 'Duplicate deleted'}), 200


@admin_bp.route('/logs/archive', methods=['GET', 'POST'])
@safe_db
def admin_logs_archive():
    if request.method == 'GET':
        return jsonify({'archived': query('SELECT * FROM activity_logs WHERE archived = TRUE')}), 200

    data = request.get_json() or {}
    cutoff_date = data.get('cutoff_date')
    if not cutoff_date:
        return jsonify({'error': 'cutoff_date is required'}), 400
    execute('UPDATE activity_logs SET archived = TRUE WHERE logged_at < %s', (cutoff_date,), commit=True)
    return jsonify({'message': 'Logs archived'}), 200


@admin_bp.route('/categories', methods=['GET', 'DELETE'])
@safe_db
def admin_categories():
    if request.method == 'GET':
        return jsonify({'categories': [row['category'] for row in query('SELECT DISTINCT category FROM activity_logs')]}), 200

    category = request.args.get('category') or (request.get_json() or {}).get('category')
    if not category:
        return jsonify({'error': 'category is required to delete logs'}), 400
    rowcount = execute('DELETE FROM activity_logs WHERE category = %s', (category,), commit=True)
    if rowcount == 0:
        return jsonify({'error': 'No logs found for category'}), 404
    return jsonify({'message': 'Logs deleted'}), 200


@admin_bp.route('/users', methods=['GET'])
@safe_db
def admin_users():
    return jsonify({'users': query(
        '''SELECT i.institution_id, i.name, COUNT(u.user_id) AS user_count
           FROM institutions i
           LEFT JOIN users u ON i.institution_id = u.institution_id
           GROUP BY i.institution_id, i.name'''
    )}), 200

@admin_bp.route('/admins', methods=['GET'])
@safe_db
def get_admins():
    return jsonify({'admins': query(
        'SELECT user_id, first_name, last_name, email, institution_id FROM users WHERE role = %s',
        ('admin',)
    )}), 200