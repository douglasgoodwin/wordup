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

class Prompt(SurrogatePK, Model):
	__tablename__ = 'prompts'
	prompt = Column(db.String(80), unique=True, nullable=False)
	parent_id = Column(db.Integer, db.ForeignKey('words.id'))

	def __init__(self, prompt, **kwargs):
		db.Model.__init__(self, prompt=prompt, **kwargs)

	def __repr__(self):
		return '{prompt!r}'.format(prompt=self.prompt)

	def __unicode__(self):
		return self.prompt

class Word(SurrogatePK, Model):
	__tablename__ = 'words'
	word = Column(db.String(80), unique=True, nullable=False)
	frequency = db.Column( db.Integer() )
	audiofiles = relationship("Audio", backref="word")
	prompts = relationship("Prompt", backref="word")

	def __init__(self, word, **kwargs):
		db.Model.__init__(self, word=word, **kwargs)

	def __repr__(self):
		return '<Word({word!r})>'.format(word=self.word)

	def __unicode__(self):
		return self.word
