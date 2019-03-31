#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

blog = Blueprint('blog', __name__)

from app.blog.user import user
from app.blog.content import article, postscript, comment
from app.blog.index import index
