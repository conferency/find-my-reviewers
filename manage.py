#!/usr/bin/env python
import os
import shutil
import glob
from app import create_app, db
from app.models import *
from flask.ext.script import Manager, Shell, Server
from config import config, Config

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


# get config
app = create_app(os.getenv('FMR_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def create_table():
    db.create_all()


@manager.command
def test_logging():
    """test logging"""
    app.logger.error('This is a error log test')
    app.logger.info('This is a info log test')


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def runserver():
    app.run(use_reloader=False)


@manager.command
def rundebug():
    app.run(use_reloader=True)


if __name__ == '__main__':
    manager.run()
