#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import login_manager
from app.models.base import db, Base

# role和permission的关联表
# 访客(Gust)
# 被封禁user(Limiter)
# 被锁定user(Locked)
# 普通user(User)
# 普通管理(Admin)
# 超管(SuperAdmin)
from app.models.content import Like

roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship(
        'Role', secondary=roles_permissions, back_populates='permissions')


# blog中的权限定义:
#     操作                           权限名称
# 点赞文章(like)                LIKE
# 文章下评论(comment)            COMMENT
# 删除comment                 UNCOMMENT
# 追评(postscript)            POSTSCRIPT
# 删追评                        UNPOSTSCRIPT
# 发表文章(发布, 编辑)          CREATE
# 上传图                       UPLOAD
# 普通管理                  ADMIN
# 超级管理                  SUPERADMIN


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    permissions = db.relationship(
        'Permission', secondary=roles_permissions, back_populates='roles')
    users = db.relationship('User', back_populates='role')

    @staticmethod
    def role_init():
        roles_permissions_map = {
            'User': ('LIKE', 'COMMENT', 'POSTSCRIPT'),
            'Admin': ('LIKE', 'COMMENT', 'POSTSCRIPT', 'UNCOMMENT',
                      'UNPOSTSCRIPT', 'CREATE', 'UPLOAD', 'ADMIN'),
            'SuperAdmin':
            ('LIKE', 'COMMENT', 'POSTSCRIPT', 'UNCOMMENT', 'UNPOSTSCRIPT',
             'CREATE', 'UPLOAD', 'ADMIN', 'SUPERADMIN')
        }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
                role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(
                    name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                db.session.add(permission)
                role.permissions.append(permission)
                db.session.commit()


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    nickname = db.Column(db.String(30))
    avatar = db.Column(db.String(30))
    email = db.Column(db.String(30))
    _password = db.Column('password', db.String(256))
    articles = db.relationship('Article', back_populates='author')
    likes = db.relationship(
        'Like', cascade='all', back_populates='users', lazy='joined')
    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            with db.auto_commit():
                if self.email == current_app.config['ADMIN']:
                    self.role = Role.query.filter_by(name='ADMIN').first()
                elif self.email == current_app.config['SUPERADMIN']:
                    self.role = Role.query.filter_by(name='SUPERADMIN').first()
                else:
                    self.role = Role.query.filter_by(name='User').first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 利用此函数来实现验证， 返回的是True, False
    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return self.role is not None and permission is not None and permission in self.role.permissions

    def auth(self, identify):
        return self.role.name.upper() == identify.upper()

    def had_like(self, article):
        if self.likes is None:
            return False
        return Like.query.with_parent(self, property='likes').filter_by(aid=article.id).first()  is not None

    def like(self, article):
        if self.had_like(article):
            with db.auto_commit():
                newLike = Like()
                newLike.articles = article
                newLike.users = self

    def unlike(self, article):
        theLike = Like.query.with_parent(
            self, property='likes').filter_by(aid=article.id).first()
        if theLike:
            with db.auto_commit():
                db.session.delete(theLike)


class Gust(AnonymousUserMixin):
    def can(self, permission_name):
        return False

    def is_administrator(self):
        return False


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


login_manager.anonymous_user = Gust
