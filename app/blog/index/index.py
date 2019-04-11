#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request
from flask.json import jsonify
from flask_login import login_required

from app.blog import blog
from app.form.content import CommentForm
from app.models.content import Article, Sorted, Tag
from app.ViewModel.content import Recommend, ViewArticle, ViewArticles


@blog.route('/')
def index():
    viewarticles = ViewArticles()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=8, error_out=False)
    viewarticles.fill(pagination.items)
    sorts = Sorted.query.all()
    recommend = Recommend()
    recommend.get_new()
    return render_template(
        'index/index.html',
        pagination=pagination,
        sorts=sorts,
        articles=viewarticles.articles,
        rec=recommend.articles[:8])


@blog.route('/pageJson/<int:page>', methods=['GET'])
@login_required
def page_json(page):
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
        page, per_page=8, error_out=False)
    articles = ViewArticles()
    articles.fill(pagination.items)
    return jsonify(articles)


@blog.route('/detail/<int:aid>')
def detail(aid):
    article = Article.query.get_or_404(aid)
    tags = article.tags
    sorts = Sorted.query.all()
    comments = article.comments
    counts = len(comments)
    viewarticle = ViewArticle(article)
    tags_cloud = Tag.all_tags()
    form = CommentForm()
    return render_template(
        'content/detail.html',
        article=viewarticle,
        tags_cloud=tags_cloud,
        comments=comments,
        sorts=sorts,
        tags=tags,
        form=form,
        counts=counts)
