#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import render_template, request, send_from_directory, current_app
from flask_login import login_required, current_user

from app.blog import blog
from app.form.content import ArticleForm
from app.libs.ImageUload import filer_save
from app.models.base import db
from app.models.content import Article
from app.models.user import User


@blog.route('/submit', methods=['POST', 'GET'])
@login_required
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        with db.auto_commit():
            user = User.query.get_or_404(current_user.id)
            article = Article()
            article.name = form.name.data
            article.body = form.body.data
            user.articles.append(article)

        return render_template('content/ArticleView.html', data=form.body.data)

    return render_template('content/newArticle.html', form=form)


@blog.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/the/uploaded/directory'
    return send_from_directory(path, filename)


@blog.route('/upload', methods=['POST'])
def save_upload():
    if request.method == "POST":
        BasePath = os.path.join(current_app.root_path, 'static')
        filer_save(BasePath)


@blog.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def editArticle(id):
    form = ArticleForm()
    article = Article.query.get_or_404(id)
    if form.validate_on_submit():
        with db.auto_commit():
            article.name = form.name.data
            article.body = form.body.data
            db.session.add(article)
            return 'success'
    form.name.data = article.name
    form.body.data = article.body
    return render_template('content/editArticle.html', form=form)


@blog.route('/likeArticle/<int:aid>')
def like_article(aid):
    article = Article.query.get_or_404(aid)
    with db.auto_commit():
        article.like += 1
        db.session.add(article)
        return 'success'
