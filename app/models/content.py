#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bleach
from markdown import markdown

from app.models.base import Base, db

# 辅助表
association = db.Table(
    'association', db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')))
# 辅助表
sort_article = db.Table(
    'sort_article', db.Column('sort_id', db.Integer,
                              db.ForeignKey('sorts.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')))


class Tag(Base):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    # 多对多关系
    articles = db.relationship(
        'Article', secondary='association', back_populates='tags')

    @classmethod
    def all_tags(cls):
        return cls.query.order_by(cls.timestamp.desc()).all()


class Article(Base):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pre_image = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    intro = db.Column(db.Text)
    body = db.Column(db.Text, unique=False)
    hot = db.Column(db.Boolean, default=False)
    liked = db.relationship(
        'Like', cascade='all', back_populates='articles', lazy='joined')
    author = db.relationship('User', back_populates='articles')
    # 一对多的双向关系
    comments = db.relationship(
        'Comment', cascade='all', back_populates='article')
    # 多对多关系建立
    tags = db.relationship(
        'Tag', secondary='association', back_populates='articles')
    sorts = db.relationship(
        'Sorted', secondary='sort_article', back_populates='articles')

    @property
    def like_info(self):
        likes = self.liked
        return len(likes) if likes else 0

    @classmethod
    def get_new(cls):
        new = cls.query.filter_by(hot=True).order_by(
            cls.timestamp.desc()).all()
        return new


class Sorted(Base):
    __tablename__ = 'sorts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    articles = db.relationship(
        'Article',
        cascade='all',
        secondary='sort_article',
        back_populates='sorts')

    @classmethod
    def total(cls):
        count = cls.articles
        return len(count) if count else 0


class Comment(Base):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    f_id = db.Column(db.Integer, nullable=False)
    f_avatar = db.Column(db.String(30))
    f_name = db.Column(db.String(30))
    to_id = db.Column(db.Integer)
    t_name = db.Column(db.String(30))
    t_content = db.Column(db.Text)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text, nullable=False)

    # 一对多的双向关系
    article = db.relationship('Article', back_populates='comments')

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
            'ol', 'pre', 'strong', 'ul', 'h2', 'h3', 'p'
        ]
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,
                strip=True))


class Like(Base):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    aid = db.Column(db.Integer, db.ForeignKey('articles.id'))
    users = db.relationship('User', back_populates='likes', lazy='joined')
    articles = db.relationship(
        'Article', back_populates='liked', lazy='joined')


db.event.listen(Comment.body, 'set', Comment.on_change_body)
