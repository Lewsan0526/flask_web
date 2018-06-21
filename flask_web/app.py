# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.utils import import_string

from config import config

extensions = [
    'flask_web.ext.db',
    'flask_web.ext.mail',
    'flask_web.ext.moment',
    'flask_web.ext.bootstrap',
    'flask_web.ext.login_manager',
    'flask_web.ext.pagedown',
]


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in extensions:
        extension = import_string(ext)
        extension.init_app(app)

    from flask_web.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from flask_web.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from flask_web.views.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
