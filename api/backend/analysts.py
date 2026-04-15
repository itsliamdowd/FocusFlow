from flask import Blueprint, jsonify, request
from backend.db_utils import safe_db, query, query_one, execute

analyst_bp = Blueprint('analyst', __name__, url_prefix='/analyst')


@analyst_bp.route('/activity', methods=['GET'])
@safe_db
def analyst_activity():
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    sql = '''SELECT al.*, u.first_name, u.last_name, u.email, u.major, u.year, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        sql += ' AND u.institution_id = %s'
        params.append(institution_id)
    if major:
        sql += ' AND u.major = %s'
        params.append(major)
    if year:
        sql += ' AND u.year = %s'
        params.append(year)

    return jsonify({'activity': query(sql, tuple(params))}), 200


@analyst_bp.route('/activity/<log_id>', methods=['GET', 'PUT'])
@safe_db
def analyst_activity_log(log_id):
    if request.method == 'GET':
        log = query_one('SELECT * FROM activity_logs WHERE log_id = %s', (log_id,))
        if not log:
            return jsonify({'error': 'Log not found'}), 404
        return jsonify({'log': log}), 200

    data = request.get_json() or {}
    if 'is_anomalous' not in data:
        return jsonify({'error': 'is_anomalous is required'}), 400
    execute('UPDATE activity_logs SET archived = TRUE WHERE log_id = %s', (log_id,), commit=True)
    return jsonify({'message': 'Log marked anomalous'}), 200


@analyst_bp.route('/correlations', methods=['GET'])
@safe_db
def analyst_correlations():
    institution_id = request.args.get('institution_id')
    sql = '''SELECT u.user_id, u.first_name, u.last_name,
               COALESCE(SUM(al.duration),0) AS total_minutes,
               COALESCE(AVG(ps.score),0) AS avg_productivity
               FROM users u
               LEFT JOIN activity_logs al ON u.user_id = al.user_id
               LEFT JOIN productivity_scores ps ON u.user_id = ps.user_id'''
    params = []
    if institution_id:
        sql += ' WHERE u.institution_id = %s'
        params.append(institution_id)
    sql += ' GROUP BY u.user_id, u.first_name, u.last_name'

    return jsonify({'correlations': query(sql, tuple(params))}), 200


@analyst_bp.route('/breakdown', methods=['GET'])
@safe_db
def analyst_breakdown():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id query parameter is required'}), 400
    return jsonify({'breakdown': query('SELECT category, SUM(duration) AS total_minutes FROM activity_logs WHERE user_id = %s GROUP BY category', (user_id,))}), 200


@analyst_bp.route('/institutions', methods=['GET'])
@safe_db
def analyst_institutions():
    return jsonify({'institutions': query('SELECT institution_id, name, type FROM institutions')}), 200


@analyst_bp.route('/export', methods=['GET'])
@safe_db
def analyst_export():
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    sql = '''SELECT al.*, u.first_name, u.last_name, u.email, u.major, u.year, u.institution_id
               FROM activity_logs al
               JOIN users u ON al.user_id = u.user_id
               WHERE 1=1'''
    params = []
    if institution_id:
        sql += ' AND u.institution_id = %s'
        params.append(institution_id)
    if major:
        sql += ' AND u.major = %s'
        params.append(major)
    if year:
        sql += ' AND u.year = %s'
        params.append(year)

    return jsonify({'export': query(sql, tuple(params))}), 200


@analyst_bp.route('/shared', methods=['GET'])
@safe_db
def analyst_shared():
    return jsonify({'shared': query(
        '''SELECT u.institution_id, COUNT(*) AS log_count, SUM(al.duration) AS total_duration
           FROM activity_logs al
           JOIN users u ON al.user_id = u.user_id
           WHERE al.archived = FALSE
           GROUP BY u.institution_id'''
    )}), 200
