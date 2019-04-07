#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.json import jsonify
from flask_login import login_required, current_user

from app.ViewModel.content import ViewArticles
from app.blog import blog
from app.form.content import CommentForm
from app.models.base import db
from app.models.content import Article, Comment, Sorted


@blog.route('/newComment/<int:aid>', methods=['POST', 'GET'])
@login_required
def new_comment(aid):
    form = CommentForm()
    if form.validate_on_submit():
        article = Article.query.get_or_404(aid)
        comment = Comment()
        with db.auto_commit():
            comment.uid = current_user.id
            comment.body = form.body.data
            article.comments.append(comment)
        return 'success'
    return render_template('content/postscript.html', form=form)


@blog.route('/likeComment/<int:cid>')
def like_comment(cid):
    comment = Comment.query.get_or_404(cid)
    with db.auto_commit():
        comment.like += 1
        db.session.add(comment)
        return 'success'


@blog.route('/get_sorted', methods=['GET'])
def get_sorted():
    sid = request.args.get('sid', type=int)
    if sid:
        sorted = Sorted.query.get_or_404(sid)
        viewarticles = ViewArticles()
        articles = sorted.articles
        viewarticles.fill(articles)
        return jsonify(viewarticles)
    return jsonify(ViewArticles())

