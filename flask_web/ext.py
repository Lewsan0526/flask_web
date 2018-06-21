# -*- coding: utf-8 -*-

from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'auth.login'
pagedown = PageDown()
