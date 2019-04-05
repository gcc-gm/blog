#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ViewArticle():
    likes = 0
    postscript = 0

    def __init__(self, article):
        self.id = article.id
        self.pre_image = article.pre_image
        self.author = article.author.nickname or '无名'
        self.name = article.name
        self.body = article.body
        self.summary = article.body[:150]
        self.comments = ''
        self.timestamp = article.timestamp

    def keys(self):
        return ['id', 'name', 'body', 'timestamp', 'per_image']

    def __getitem__(self, item):
        return getattr(self, item)

    def all_like(self, article):
        pass


class ViewArticles():
    def __init__(self):
        self.total = 0
        self.articles = []

    def fill(self, items):
        self.total = len(items)
        self.articles = [ViewArticle(article) for article in items]

    def keys(self):
        return ['total', 'articles']

    def __getitem__(self, item):
        return getattr(self, item)


class Recommend():
    def __init__(self, recommend):
        self.title = self.get_title(recommend) or ''

    @classmethod
    def get_title(cls, recommend):
        from app.models.content import Article
        article = Article.query.filter_by(aid=recommend.aid).first_or_404()
        return article.name
