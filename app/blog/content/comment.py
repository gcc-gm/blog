#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask_login import login_required, current_user
from app.blog import blog
from app.form.content import CommentForm
from app.models.base import db
from app.models.content import Article, Comment


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
