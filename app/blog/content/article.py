#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
from flask import current_app, render_template, request, send_from_directory, abort, flash, redirect, url_for
from flask_login import current_user, login_required

from app.ViewModel.content import ViewArticles, Recommend
from app.blog import blog
from app.form.content import ArticleForm, SearchForm
from app.libs.decorators import auth_required
from app.libs.ImageUload import filer_save
from app.models.base import db
from app.models.content import Article, Sorted
from app.models.user import User


@blog.route('/submit', methods=['POST', 'GET'])
@login_required
@auth_required('superadmin')
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        pre_image = form.pre_image.data
        if pre_image.filename:
            _, ext = os.path.splitext(pre_image.filename)
            base_path = os.path.join(current_app.root_path, 'static')
            path = os.path.join(base_path, 'pre_image')
            pre_image.filename = uuid.uuid4().hex + ext
            try:
                pre_image.save(os.path.join(path, pre_image.filename))
            except Exception as e:
                raise e
        with db.auto_commit():
            user = User.query.get_or_404(current_user.id)
            article = Article()
            article.name = form.name.data
            article.body = form.body.data
            article.pre_image = pre_image.filename
            article.intro = form.intro.data
            user.articles.append(article)
        return redirect(url_for('blog.admin'))
    return render_template('content/newArticle.html', form=form)


@blog.route('/files/<path:filename>')
def uploaded_files(filename):
    base_path = os.path.join(current_app.root_path, 'static')
    path = os.path.join(base_path, 'upload')
    return send_from_directory(path, filename)


@blog.route('/upload', methods=['POST'])
@login_required
def save_upload():
    if request.method == "POST":
        base_path = os.path.join(current_app.root_path, 'static')
        return filer_save(base_path)


@blog.route('/edit/<int:aid>', methods=['POST', 'GET'])
@login_required
@auth_required('superadmin')
def editArticle(aid):
    form = ArticleForm()
    article = Article.query.get_or_404(aid)
    if form.validate_on_submit():
        with db.auto_commit():
            article.name = form.name.data
            article.body = form.body.data
            db.session.add(article)
            return 'success'
    form.name.data = article.name
    form.body.data = article.body
    return render_template('content/editArticle.html', form=form)


@blog.route('/likeArticle', methods=["POST"])
@login_required
def like_article():
    """
    用户点赞
    :return:
    """
    aid = request.form.get('aid')
    if aid is None:
        flash('参数异常')
        return redirect(url_for('blog.index'))
    article = Article.query.get(aid)
    if article and current_user.like(article):
        flash('操作成功!')
        return redirect(url_for('blog.detail', aid=aid))
    flash('fail')
    return redirect(url_for('blog.detail', aid=aid))


@blog.route('/unlike/<int:aid>')
@login_required
def unlike(aid):
    """
    用户撤销点赞
    :param aid: article_id
    :return: 撤销后重定向至首页
    """
    article = Article.query.get(aid)
    if article and current_user.unlike(article):
        flash('操作成功!')
        return redirect(url_for('blog.detail', aid=aid))
    flash('fail')
    return redirect(url_for('blog.detail', aid=aid))


@blog.route('/pre/<int:aid>')
def pre(aid):
    article = Article.query.get_or_404(aid)
    return render_template('content/ArticleView.html', data=article.body)


@blog.route('/search')
def search():
    form = SearchForm(request.args)
    if form.validate():
        viewarticles = ViewArticles()
        articles = Article.query.filter(Article.name.like("%" + form.keyboard.data + "%")).order_by(
            Article.timestamp).all()
        viewarticles.fill(articles)
        sorts = Sorted.query.all()
        recommend = Recommend()
        recommend.get_new()
        flash('一共找到%s条记录' % len(articles))
        return render_template(
            'index/index.html',
            sorts=sorts,
            articles=viewarticles.articles,
            rec=recommend.articles[:8])
    abort(404)


@blog.route('/class_article/<int:sid>')
def class_articles(sid):
    sort = Sorted.query.get_or_404(sid)
    viewarticles = ViewArticles()
    viewarticles.fill(sort.articles)
    sorts = Sorted.query.all()
    recommend = Recommend()
    recommend.get_new()
    return render_template(
        'index/index.html',
        sorts=sorts,
        articles=viewarticles.articles,
        rec=recommend.articles[:8]
    )
