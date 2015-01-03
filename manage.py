#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os,sys,subprocess,time
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
import requests
from wordnik import (
	swagger, 
	WordApi,
	)

from wordup.app import create_app
from wordup.user.models import User, Role
from wordup.word.models import Word,Prompt,Audio, Definition
from wordup.settings import DevConfig, ProdConfig
from wordup.database import db, top300
from wordup.utils import strip_target

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

# wordnik
apiUrl = 'http://api.wordnik.com/v4'
apiKey='58be09f4810e9061d96730672b908d53e4516ce123b6aae3e'
client = swagger.ApiClient(apiKey, apiUrl)
wordapi = WordApi.WordApi(client)

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

@manager.command
def init():
	db.create_all()
	try:
		print "hey!"
		user_datastore.create_user(
			username="dgoodwin",
			email='dgoodwin@gmail.com',
			password='Haukola',
			is_admin=True,
			active=True,
			first_name='Douglas',
			last_name='Goodwin',
			)
		db.session.commit()
	except:
		print "oof!"

	for one in top300:
		print "(shhh, the word is *%s*)" %(one)
		getexamples = wordapi.getExamples(one)
		getfrequency = wordapi.getWordFrequency(one)
		gettopexample = wordapi.getTopExample(one)
		getdefinitions = wordapi.getDefinitions(one)
		gettextpronunciations = wordapi.getTextPronunciations(one)
		getwordfrequency = wordapi.getWordFrequency(one)
		getetymologies = wordapi.getEtymologies(one)
		frequency=getfrequency.totalCount
		getaudio = wordapi.getAudio(one)
		#
		prompts=[]
		audios=[]
		examples=[]
		definitions=[]
		# etymologies=[]
		pronunciations=[]
		#
		mypr = gettextpronunciations[0].raw
		mytop = strip_target(gettopexample.text,one)
		for ex in getexamples.examples:
			p = strip_target(ex.text,one)
			ppp = Prompt.create(prompt=p,
							title=ex.title,
							year=ex.year,
							)
			db.session.commit()
			prompts.append( ppp )
		for i,df in enumerate(getdefinitions, start=1):
			mydft = "%s. %s" %(i,strip_target(df.text,one))
			mydf = Definition.create(definition=mydft)
			print "{{{{{{{{{{{ mydef }}}}}}}}}}}"
			print mydf
			db.session.commit()
			definitions.append( mydf )
		#
		for au in getaudio:
			ftype = au.audioType
			if ftype=='pronunciation':
				furl = au.fileUrl
				fuuid = furl.split("/")[-1]
				fname = "%s.mp3" %(fuuid)
				with open(fname, 'wb') as handle:
					response = requests.get(furl, stream=True)
					if not response.ok:
						# Something went wrong
						print "blargh!"
					else:
						for block in response.iter_content(1024):
							if not block:
								break
							handle.write(block)
						audios.append( Audio.create(audiofile=fname) )
						db.session.commit()
		Word.create(
			word=one,
			audiofiles=audios,
			prompts=prompts,
			frequency=frequency,
			pronunciation=gettextpronunciations[0].raw,
			topprompt=mytop,
			definitions=definitions,
			)
		db.session.commit()
		time.sleep(2)

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
