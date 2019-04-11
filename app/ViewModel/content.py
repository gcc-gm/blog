#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.content import Article


class ViewArticle:
    likes = 0

    def __init__(self, article):
        self.id = article.id
        self.pre_image = article.pre_image
        self.author = article.author.nickname if article.author else ''
        self.name = article.name
        self.body = article.body
        self.summary = article.body[:150]
        self.timestamp = article.timestamp
        self.like_info = article.like_info
        self.pre_name, self.pre_id = self.pre_or_next(article.id - 1)
        self.next_name, self.next_id = self.pre_or_next(article.id + 1)

    @staticmethod
    def pre_or_next(aid):
        a = Article.query.get(aid)
        if a:
            return a.name, a.id
        return '没有了', -1

    def keys(self):
        return ['id', 'name', 'body', 'timestamp', 'pre_image', 'author']

    def __getitem__(self, item):
        return getattr(self, item)

    def all_like(self, article):
        pass


class ViewArticles:
    def __init__(self):
        self.total = 0
        self.articles = []

    def fill(self, items):
        if items:
            self.total = len(items)
            self.articles = [ViewArticle(article) for article in items]

    def keys(self):
        return ['total', 'articles']

    def __getitem__(self, item):
        return getattr(self, item)


class Recommend(ViewArticles):
    def __init__(self):
        super(Recommend, self).__init__()

    def get_new(self):
        from app.models.content import Article
        rec = Article.get_new()
        if rec:
            self.fill(rec)


class ViewComment:
    def __init__(self, comment):
        self.f_id = comment.f_id
        self.t_id = comment.t_id
        self.f_name = comment.f_name
        self.t_name = comment.t_name
        self.body = comment.body_html
        self.timestamp = comment.timestamp

    def keys(self):
        return ['f_id', 'f_name', 't_id', 't_name', 'body', 'timestamp']

    def __getitem__(self, item):
        return getattr(self, item)


class ViewComments:
    def __init__(self):
        self.total = 0
        self.comments = []

    def fill(self, items):
        if items:
            self.total = len(items)
            self.comments = [ViewComment(com) for com in items]

    def keys(self):
        return ['total', 'comments']

    def __getitem__(self, item):
        return getattr(self, item)
