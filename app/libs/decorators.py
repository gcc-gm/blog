#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import abort, current_app
from flask_login import current_user


def permission_required(permission_name):
    def decorated(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorated


# 针对超管
def admin_required(f):
    return permission_required(current_app.config['SUPERADMIN'])(f)
