#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bleach
from markdown import markdown

from app.models.base import Base, db

# 辅助表
association = db.Table('association',
                       db.Column('tag_id', db.Integer,
                                 db.ForeignKey('tags.id')),
                       db.Column('article_id', db.Integer,
                                 db.ForeignKey('articles.id')))


class Tag(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    # 多对多关系
    articles = db.relationship('Article',
                               secondary='association', back_populates='tags')


class Article(Base):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pre_image = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    body = db.Column(db.Text, unique=False)

    liked = db.relationship('Like', cascade='all', back_populates='articles', lazy='joined')
    author = db.relationship('User', back_populates='articles')
    # 一对多的双向关系
    comments = db.relationship('Comment', cascade='all', back_populates='article')
    # 多对多关系建立
    tags = db.relationship('Tag', secondary='association', back_populates='articles')

    def get_comments(self):
        if self.comments is None:
            return []


        comments = [self.comments]
        return ['']


class Comment(Base):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text, nullable=False)
    like = db.Column(db.Integer, default=0)
    # 一对多的双向关系
    article = db.relationship('Article', back_populates='comments')
    # 后评
    postscripts = db.relationship('Postscript', cascade='all', back_populates='comment')
    # 仅建立单向关系
    author = db.relationship('User')

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags,
                                                       strip=True))


class Like(Base):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    aid = db.Column(db.Integer, db.ForeignKey('articles.id'))
    users = db.relationship('User', back_populates='likes', lazy='joined')
    articles = db.relationship('Article', back_populates='liked', lazy='joined')


class Postscript(Base):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    like = db.Column(db.Integer, default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    # 建立关系
    comment = db.relationship('Comment', back_populates='postscripts')

    def __repr__(self):
        return self.name

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags,
                                                       strip=True))


db.event.listen(Postscript.body, 'set', Postscript.on_change_body)
db.event.listen(Comment.body, 'set', Postscript.on_change_body)
