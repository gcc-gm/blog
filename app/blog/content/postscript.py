#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask_login import login_required, current_user

from app.blog import blog
from app.form.content import PostscriptForm
from app.models.base import db
from app.models.content import Postscript, Comment


@blog.route('/newPostscript/<int:cid>', methods=['POST', 'GET'])
@login_required
def new_postscript(cid):
    form = PostscriptForm()
    if form.validate_on_submit():
        comment = Comment.query.get_or_404(cid)

        with db.auto_commit():
            postscript = Postscript()
            comment.postscripts.append(postscript)
            postscript.uid = current_user.id
            postscript.body = form.body.data

        return 'success'
    return render_template('content/postscript.html', form=form)
