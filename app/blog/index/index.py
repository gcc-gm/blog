#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.json import jsonify

from flask_login import login_required, current_user

from app.blog import blog
from app.ViewModel.content import ViewArticles
from app.models.content import Article


@blog.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=5, error_out=False
    )

    return render_template('index/index.html', pagination=pagination)


@blog.route('/pageJson/<int:page>', methods=['GET'])
@login_required
def page_json(page):
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=5, error_out=False
    )
    articles = ViewArticles()

    articles.fill(pagination.items)

    return jsonify(articles)
    # a = pagination.items[0]
    # user = current_user.had_like(a.id)
    # return ''


