# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.utils import import_string

extensions = [
    'flask_web.ext.db',
    'flask_web.ext.mail',
    'flask_web.ext.moment',
    'flask_web.ext.bootstrap',
    'flask_web.ext.login_manager',
    'flask_web.ext.pagedown',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object('envcfg.json.flask_web')
    print(app.config)
    if not app.config['DEBUG']:
        init_app(app)

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


def init_app(app):
    """
    email errors to the administrators
    """
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None
    if app.config.get('MAIL_USERNAME'):
        credentials = (app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD'))
        if app.config.get('MAIL_USE_TLS', None):
            secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config.get('MAIL_SERVER'),
                  app.config.get('MAIL_PORT')),
        fromaddr=app.config.get('MAIL_SENDER'),
        toaddrs=[app.config.get('ADMIN')],
        subject=app.config.get('MAIL_SUBJECT_PREFIX', '') + ' Application Error',
        credentials=credentials,
        secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
