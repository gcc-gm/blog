#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid

from flask import request, current_app, url_for
from flask_ckeditor import upload_success, upload_fail


def filer_save(BasePath):
    if 'upload' in request.files:
        f = request.files['upload']
        if f and allow_ext(f.filename):
            _, ext = os.path.splitext(f.filename)
            path = os.path.join(BasePath, 'upload')
            f.filename = uuid.uuid4().hex + ext
            try:
                f.save(os.path.join(path, f.filename))
            except Exception as e:
                return upload_fail(message=e.args)
            url = url_for('blog.uploaded_files', filename=f.filename)
            return upload_success(url, f.filename)


def allow_ext(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXT']
