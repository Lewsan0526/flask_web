# -*- coding: utf-8 -*-

from functools import wraps

from flask_login import current_user
from flask import abort

from ..models.role import Permission


def permisson_required(permisson):
    def decorator(f):
        @wraps(f)
        def decorator_func(*args, **kwargs):
            if not current_user.can(permisson):
                abort(403)
            return f(*args, **kwargs)

        return decorator_func

    return decorator


def admin_required(f):
    return permisson_required(Permission.ADMIN)(f)
