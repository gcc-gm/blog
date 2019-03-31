#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Flask as _Flask
from flask.json import JSONEncoder


class BlogJSONEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')
        else:
            super(BlogJSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = BlogJSONEncoder
