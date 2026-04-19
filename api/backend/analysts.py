from flask import Blueprint, jsonify, request
from backend.db_utils import safe_db, query, query_one, execute

analyst_bp = Blueprint('analyst', __name__, url_prefix='/analyst')


def build_activity_query(institution_id, major, year):
    """Build SQL query and params for activity logs with optional filters."""
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
    return sql, params


@analyst_bp.route('/activity', methods=['GET'])
@safe_db
def analyst_activity():
    """Get activity logs with optional filters for institution, major, and year."""
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    sql, params = build_activity_query(institution_id, major, year)
    return jsonify({'activity': query(sql, tuple(params))}), 200


@analyst_bp.route('/activity/<log_id>', methods=['GET', 'PUT'])
@safe_db
def analyst_activity_log(log_id):
    """Get or update an activity log by ID."""
    if request.method == 'GET':
        log = query_one('SELECT * FROM activity_logs WHERE log_id = %s', (log_id,))
        if not log:
            return jsonify({'error': 'Log not found'}), 404
        return jsonify({'log': log}), 200

    data = request.get_json() or {}
    if not data.get('is_anomalous', False):
        return jsonify({'error': 'is_anomalous must be true to mark as anomalous'}), 400
    rowcount = execute('UPDATE activity_logs SET archived = TRUE WHERE log_id = %s', (log_id,), commit=True)
    if rowcount == 0:
        return jsonify({'error': 'Log not found'}), 404
    return jsonify({'message': 'Log marked as anomalous and archived'}), 200


@analyst_bp.route('/correlations', methods=['GET'])
@safe_db
def analyst_correlations():
    """Get student correlations with study minutes and average productivity scores."""
    institution_id = request.args.get('institution_id')
    params = []
    student_filter = "u.role = 'student'"
    if institution_id:
        student_filter += ' AND u.institution_id = %s'
        params.append(institution_id)

    sql = f'''SELECT u.user_id, u.first_name, u.last_name,
               COALESCE(st.total_minutes, 0) AS total_minutes,
               COALESCE(prod.avg_productivity, 0) AS avg_productivity
               FROM users u
               LEFT JOIN (
                   SELECT user_id, SUM(duration) AS total_minutes
                   FROM activity_logs
                   WHERE archived = FALSE
                   GROUP BY user_id
               ) st ON st.user_id = u.user_id
               LEFT JOIN (
                   SELECT user_id, AVG(score) AS avg_productivity
                   FROM productivity_scores
                   GROUP BY user_id
               ) prod ON prod.user_id = u.user_id
               WHERE {student_filter}
               ORDER BY u.user_id'''

    return jsonify({'correlations': query(sql, tuple(params))}), 200


@analyst_bp.route('/breakdown', methods=['GET'])
@safe_db
def analyst_breakdown():
    """Get activity breakdown by category for a specific user."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id query parameter is required'}), 400
    return jsonify({'breakdown': query('SELECT category, SUM(duration) AS total_minutes FROM activity_logs WHERE user_id = %s GROUP BY category', (user_id,))}), 200


@analyst_bp.route('/institutions', methods=['GET'])
@safe_db
def analyst_institutions():
    """Get list of all institutions."""
    return jsonify({'institutions': query('SELECT institution_id, name, type FROM institutions')}), 200


@analyst_bp.route('/export', methods=['GET'])
@safe_db
def analyst_export():
    """Export activity logs with optional filters for institution, major, and year."""
    institution_id = request.args.get('institution_id')
    major = request.args.get('major')
    year = request.args.get('year')

    sql, params = build_activity_query(institution_id, major, year)
    return jsonify({'export': query(sql, tuple(params))}), 200


@analyst_bp.route('/shared', methods=['GET'])
@safe_db
def analyst_shared():
    """Get shared activity data aggregated by institution."""
    return jsonify({'shared': query(
        '''SELECT u.institution_id, COUNT(*) AS log_count, SUM(al.duration) AS total_duration
           FROM activity_logs al
           JOIN users u ON al.user_id = u.user_id
           WHERE al.archived = FALSE
           GROUP BY u.institution_id'''
    )}), 200

@analyst_bp.route('/users', methods=['GET'])
@safe_db
def get_analysts():
    return jsonify({'analysts': query(
        'SELECT user_id, first_name, last_name, email, institution_id FROM users WHERE role = %s',
        ('analyst',)
    )}), 200
