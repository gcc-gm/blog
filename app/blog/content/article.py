#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask_login import login_required, current_user

from app.blog import blog
from app.form.content import ArticleForm
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
