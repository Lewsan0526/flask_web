# -*- coding: utf-8 -*-

from flask import request, current_app, url_for, jsonify, g

from . import api
from .errors import forbidden
from .decorators import permission_required
from flask_web.ext import db
from flask_web.models.post import Post
from flask_web.models.role import Permission


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page + 1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/posts/<int:postid>')
def get_post(postid):
    post = Post.query.get_or_404(postid)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(
        post.to_json()), 201, {'Location': url_for('api.get_post', postid=post.id)}


@api.route('/posts/<int:postid>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(postid):
    post = Post.query.get_or_404(postid)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())
