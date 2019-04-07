#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import abort
from flask_login import current_user


# 单个权限管理
def permission_required(permission_name):
    def decorated(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.can(permission_name.upper()):
                abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorated


# 角色控制
def auth_required(identify):
    def decorated(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not current_user.auth(identify.upper()):
                abort(403)
            return f(*args, **kwargs)

        return decorated_func

    return decorated
