# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from flask_web.models.role import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
