# -*- coding: utf-8 -*-
import datetime as dt
from flask import url_for

# from flask.ext.login import UserMixin
from flask.ext.security import (
	# Security,
	# SQLAlchemyUserDatastore,
	UserMixin, 
	RoleMixin, 
	# login_required,
	)

from wordup.extensions import bcrypt
from wordup.database import (
	Column,
	db,
	Model,
	ReferenceCol,
	relationship,
	SurrogatePK,
)

class Audio(SurrogatePK, Model):
	__tablename__ = 'audios'
	audiofile = Column(db.String(80), unique=True, nullable=False)
	parent_id = Column(db.Integer, db.ForeignKey('words.id'))

	def __init__(self, audiofile, **kwargs):
		db.Model.__init__(self, audiofile=audiofile, **kwargs)

	def __repr__(self):
		return '<Audio({audiofile!r})>'.format(audiofile=self.audiofile)

	def __unicode__(self):
		return '<Audio({audiofile!r})>'.format(audiofile=self.audiofile)

	def link(self):
		return "/static/mp3/%s" %(self.audiofile)

class Definition(SurrogatePK, Model):
	__tablename__ = 'definitions'
	definition = Column(db.String(80), unique=True, nullable=False)
	parent_id = Column(db.Integer, db.ForeignKey('words.id'))

	def __init__(self, definition, **kwargs):
		db.Model.__init__(self, definition=definition, **kwargs)

	def __repr__(self):
		return '{definition!r}'.format(definition=self.definition)

	def __unicode__(self):
		return self.definition

class Prompt(SurrogatePK, Model):
	""" 'provider',
		 'rating',
		 'score',
		 'sentence',
		 'swaggerTypes',
		 'text',
		 'title',
		 'url',
		 'word',
		 'year'
	"""
	__tablename__ = 'prompts'
	prompt = Column(db.String(80), unique=True, nullable=False)
	parent_id = Column(db.Integer, db.ForeignKey('words.id'))
	provider = Column(db.String(80), nullable=True)
	sentence = Column(db.String(120), nullable=True)
	text = Column(db.String(120), nullable=True)
	title = Column(db.String(80), nullable=True)
	year = Column(db.String(80), nullable=True)
	url = Column(db.String(120), nullable=True)

	def __init__(self, prompt, title, year, **kwargs):
		db.Model.__init__(self, prompt=prompt, title=title, year=year, **kwargs)

	def __repr__(self):
		return '{prompt!r}'.format(prompt=self.prompt)

	def __unicode__(self):
		return self.prompt

class Word(SurrogatePK, Model):
	__tablename__ = 'words'
	word = Column(db.String(80), unique=True, nullable=False)
	pronunciation = Column(db.String(80), unique=True, nullable=False)
	frequency = db.Column( db.Integer() )
	topprompt = Column(db.String(120))	# slam this in here
	audiofiles = relationship("Audio", backref="audioword")
	prompts = relationship("Prompt", backref="promptword")
	definitions = relationship("Definition", backref="definitionword")

	def __init__(self, word, **kwargs):
		db.Model.__init__(self, word=word, **kwargs)

	def __repr__(self):
		return '<Word({word!r})>'.format(word=self.word)

	def __unicode__(self):
		return self.word
