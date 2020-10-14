import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

    
@bp.app_errorhandler(404)
def page_not_found(e):
    return "<h1 style='text-align:center'>404</h1><h3 style='text-align:center'>The page could not be found.</h3>", 404

@bp.route('/resources/posts/all', methods=['GET'])
def api_posts_all():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        'SELECT     p.id, title, body, created, username'
        ' FROM post p JOIN user u ON p.author_id = u.id' 
        ' ORDER BY created DESC'
    )
    posts = cursor.fetchall()
    
    return jsonify(posts)
    
@bp.route('/resources/posts', methods=['GET'])
def api_post_filter():
    
    query_parameters = request.args

    pid = query_parameters.get('id')
    title = query_parameters.get('title')
    author_id = query_parameters.get('author_id')
    date = query_parameters.get('created')
    
    query = 'SELECT p.id, title, body, created, username'
    query+= ' FROM post p JOIN user u ON p.author_id = u.id WHERE'
    to_filter = []

    if pid:
        query += ' p.id=%s AND'
        to_filter.append(pid)
    if title:
        query += ' title=%s AND'
        to_filter.append(title)
    if author_id:
        query += ' author_id=%s AND'
        to_filter.append(author_id)
    if date:
        query += ' created=%s AND'
        to_filter.append(date) 
    if not (pid or title or author_id or date):
        return page_not_found(404)

    query = query[:-4] + ';'

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, to_filter)
    posts = cursor.fetchall()
    return jsonify(posts)
