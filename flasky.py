# -*- coding: utf-8 -*-

import os
from flask_migrate import Migrate

from flask_web.app import create_app
from flask_web.ext import db
from flask_web.models.role import Role
from flask_web.models.user import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
