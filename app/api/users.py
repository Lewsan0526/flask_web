# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app, url_for
from . import api
from ..models.user import User
from ..models.post import Post


@api.route('/users/<int:userid>')
def get_user(userid):
    user = User.query.get_or_404(userid)
    return jsonify(user.to_json())


@api.route('/users/<int:postid>/posts/')
def get_user_posts(postid):
    user = User.query.get_or_404(postid)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_user_posts', postid=postid, page=page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_user_posts', postid=postid, page=page + 1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/users/<int:userid>/timeline/')
def get_user_followed_posts(userid):
    user = User.query.get_or_404(userid)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_user_followed_posts', userid=userid, page=page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_user_followed_posts', userid=userid, page=page + 1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })
