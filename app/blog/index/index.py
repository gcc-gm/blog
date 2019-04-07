#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.json import jsonify
from flask_login import login_required

from app.blog import blog
from app.models.content import Article, Sorted
from app.ViewModel.content import Recommend, ViewArticle, ViewArticles


@blog.route('/')
def index():
    viewarticles = ViewArticles()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=15, error_out=False)
    viewarticles.fill(pagination.items)
    sorts = Sorted.query.all()
    recommend = Recommend()
    recommend.get_new()
    print(recommend.articles)

    return render_template(
        'index/index.html',
        sorts=sorts,
        articles=viewarticles.articles,
        rec=recommend.articles)


@blog.route('/pageJson/<int:page>', methods=['GET'])
@login_required
def page_json(page):
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=5, error_out=False)
    articles = ViewArticles()
    articles.fill(pagination.items)
    return jsonify(articles)


@blog.route('/detail/<int:aid>')
def detail(aid):
    article = Article.query.get_or_404(aid)
    tags = article.tags
    comments = article.comments
    counts = len(comments)
    viewarticle = ViewArticle(article)
    return render_template(
        'content/detail.html',
        article=viewarticle,
        tags=tags,
        comments=comments,
        counts=counts)
