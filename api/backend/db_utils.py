from contextlib import contextmanager
from functools import wraps
from flask import jsonify, current_app
from backend.db_connection import get_db
from mysql.connector import Error


@contextmanager
def with_cursor(dictionary=True):
    cursor = get_db().cursor(dictionary=dictionary)
    try:
        yield cursor
    finally:
        cursor.close()


def query(sql, params=(), dictionary=True):
    with with_cursor(dictionary=dictionary) as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def query_one(sql, params=(), dictionary=True):
    with with_cursor(dictionary=dictionary) as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


def insert(sql, params=()):
    with with_cursor(dictionary=False) as cursor:
        cursor.execute(sql, params)
        get_db().commit()
        return cursor.lastrowid


def execute(sql, params=(), commit=False):
    with with_cursor(dictionary=False) as cursor:
        cursor.execute(sql, params)
        if commit:
            get_db().commit()
        return cursor.rowcount


def safe_db(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Error as e:
            current_app.logger.exception('Database operation failed')
            return jsonify({'error': 'Database operation failed'}), 500
    return wrapper
