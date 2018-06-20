# -*- coding: utf-8 -*-
from flask import request, current_app, url_for, jsonify, g

from app import db
from .decorators import permission_required
from . import api
from ..models.comment import Comment
from ..models.post import Post
from ..models.role import Permission


@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_comments', page=page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_comments', page=page + 1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/commments/<int:cmtid>')
def get_comment(cmtid):
    comment = Comment.query.get_or_404(cmtid)
    return jsonify(comment.to_json())


@api.route('/posts/<int:postid>/comments')
def get_post_comments(postid):
    post = Post.query.get_or_404(postid)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page,
        per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False,
    )
    comments = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_post_comments', postid=postid, page=page - 1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_post_comments', postid=postid, page=page + 1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev_page': prev_page,
        'next_page': next_page,
        'count': pagination.total,
    })


@api.route('/post/<int:postid>/comments', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(postid):
    post = Post.query.get_or_404(postid)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(
        comment.to_json(),
        201,
        {'Location': url_for('api.get_comment', cmtid=comment.id)})
