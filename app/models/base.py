#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()

            raise e


db = SQLAlchemy()


class Base(db.Model):
    # 不创建实际的表
    __abstract__ = True
    timestamp = db.Column(db.DateTime, index=True)
    status = db.Column(db.Boolean, default=True)

    def __init__(self):
        self.timestamp = datetime.utcnow()

    def delete(self):
        self.status = False
