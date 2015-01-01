#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from wordup.app import create_app
from wordup.user.models import User, Role
from wordup.word.models import Word,Prompt,Audio
from wordup.settings import DevConfig, ProdConfig
from wordup.database import db

from flask.ext.security import (
	Security,
	SQLAlchemyUserDatastore, 
	UserMixin, 
	RoleMixin, 
	login_required,
	)
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(user_datastore)

if os.environ.get("WORDUP_ENV") == 'prod':
	app = create_app(ProdConfig)
else:
	app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
	"""Return context dict for a shell session so you can access
	app, db, and the User model by default.
	"""
	return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
	"""Run the tests."""
	import pytest
	exit_code = pytest.main([TEST_PATH, '--verbose'])
	return exit_code

@app.before_first_request
def createme():
	db.create_all()
	try:
		print "hey!"
		# user_datastore.create_user(
		# 	username="dgoodwin",
		# 	email='dgoodwin@gmail.com',
		# 	password='Haukola',
		# 	is_admin=True,
		# 	active=True,
		# 	first_name='Douglas',
		# 	last_name='Goodwin',
		# 	)
		# db.session.commit()
	except:
		print "oof!"
		pass

# # Create a user to test with
# @app.before_first_request
# def create_user():
# 	db.create_all()
# 	user_datastore.create_user(username="dgoodwin", email='dgoodwin@gmail.com', password='shhhh')
# 	db.session.commit()

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
