# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import
from flask_web.cli import main

if __name__ == '__main__':
    main()

# import os
#
# from flask_script import Manager
# from flask_migrate import MigrateCommand
# from gunicorn.app.wsgiapp import WSGIApplication
#
# # COV = None
# # if os.environ.get('FLASK_COVERAGE'):
# #     import coverage
# #
# #     COV = coverage.coverage(branch=True, include='app/*')
# #     COV.start()
# from flask_web.app import create_app
# from flask_web.ext import db
# from flask_web.models.follow import Follow
# from flask_web.models.post import Post
# from flask_web.models.role import Role, Permission
# from flask_web.models.user import User
#
# app = create_app()
# manager = Manager(app)
# manager.add_command("db", MigrateCommand)
#
#
# @manager.shell
# def make_shell_context():
#     return dict(db=db, User=User, Follow=Follow, Role=Role,
#                 Permission=Permission, Post=Post)
#
#
# @manager.command
# def test(coverage=False):
#     """Run the unit tests."""
#     if coverage and not os.environ.get('FLASK_COVERAGE'):
#         import sys
#         os.environ['FLASK_COVERAGE'] = '1'
#         os.execvp(sys.executable, [sys.executable] + sys.argv)
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#     # if COV:
#     #     COV.stop()
#     #     COV.save()
#     #     print('Coverage Summary:')
#     #     COV.report()
#     #     basedir = os.path.abspath(os.path.dirname(__file__))
#     #     covdir = os.path.join(basedir, 'tmp/coverage')
#     #     COV.html_report(directory=covdir)
#     #     print('HTML version: file://%s/index.html' % covdir)
#     #     COV.erase()
#
#
# @manager.command
# def profile(length=25, profile_dir=None):
#     """Start the application under the code profiler."""
#     from werkzeug.contrib.profiler import ProfilerMiddleware
#     app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
#                                       profile_dir=profile_dir)
#     app.run()
#
#
# @manager.command
# def deploy():
#     """Run deployment tasks."""
#     from flask_migrate import upgrade
#
#     # migrate database to latest revision
#     upgrade()
#
#     # create user roles
#     Role.insert_roles()
#
#     # create self-follows for all users
#     User.add_self_follows()
#
#
# @manager.command
# def runserver(host=None, port=None, workers=None):
#     """Run the app with Gunicorn."""
#     host = host or app.config.get('HTTP_HOST') or '0.0.0.0'
#     port = port or app.config.get('HTTP_PORT') or 5000
#     workers = workers or app.config.get('HTTP_WORKERS') or 1
#     use_evalex = app.config.get('USE_EVALEX', app.debug)
#
#     if app.debug:
#         app.run(host, int(port), use_evalex=use_evalex)
#     else:
#         gunicorn = WSGIApplication()
#         gunicorn.load_wsgiapp = lambda: app
#         gunicorn.cfg.set('bind', '%s:%s' % (host, port))
#         gunicorn.cfg.set('workers', workers)
#         gunicorn.cfg.set('pidfile', None)
#         gunicorn.cfg.set('worker_class', 'gunicorn.workers.ggevent.GeventWorker')
#         gunicorn.cfg.set('accesslog', '-')
#         gunicorn.cfg.set('errorlog', '-')
#         gunicorn.cfg.set('timeout', 300)
#         gunicorn.chdir()
#         gunicorn.run()
#
#
# def main():
#     manager.run()
#
#
# if __name__ == '__main__':
#     manager.run()
