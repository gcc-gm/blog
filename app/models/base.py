#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from werkzeug.exceptions import abort


class BlogQuery(BaseQuery):
    """
        改下BaseQuery 的某些查询方法
    """

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None or rv.status != 1:
            abort(404)
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None or rv.status != 1:
            abort(404)
        return rv

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(BlogQuery, self).filter_by(**kwargs)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy(query_class=BlogQuery)


class Base(db.Model):
    # 不创建实际的表
    __abstract__ = True
    timestamp = db.Column(db.DateTime, index=True)
    status = db.Column(db.Boolean, default=True)

    def __init__(self):
        self.timestamp = datetime.utcnow()

    def delete(self):
        self.status = False
