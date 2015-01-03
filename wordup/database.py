# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
from sqlalchemy.orm import relationship

from .extensions import db
from .compat import basestring

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

class CRUDMixin(object):
	"""Mixin that adds convenience methods for CRUD (create, read, update, delete)
	operations.
	"""

	@classmethod
	def create(cls, **kwargs):
		"""Create a new record and save it the database."""
		instance = cls(**kwargs)
		return instance.save()

	def update(self, commit=True, **kwargs):
		"""Update specific fields of a record."""
		for attr, value in kwargs.iteritems():
			setattr(self, attr, value)
		return commit and self.save() or self

	def save(self, commit=True):
		"""Save the record."""
		db.session.add(self)
		if commit:
			db.session.commit()
		return self

	def delete(self, commit=True):
		"""Remove the record from the database."""
		db.session.delete(self)
		return commit and db.session.commit()

class Model(CRUDMixin, db.Model):
	"""Base model class that includes CRUD convenience methods."""
	__abstract__ = True

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
	"""A mixin that adds a surrogate integer 'primary key' column named
	``id`` to any declarative-mapped class.
	"""
	__table_args__ = {'extend_existing': True}

	id = db.Column(db.Integer, primary_key=True)

	@classmethod
	def get_by_id(cls, id):
		if any(
			(isinstance(id, basestring) and id.isdigit(),
			 isinstance(id, (int, float))),
		):
			return cls.query.get(int(id))
		return None


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
	"""Column that adds primary key foreign key reference.

	Usage: ::

		category_id = ReferenceCol('category')
		category = relationship('Category', backref='categories')
	"""
	return db.Column(
		db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
		nullable=nullable, **kwargs)



top300 = ['to','you','they','not','go','her','as','think','take','come','then','way','more',
	'very','give','through','may','still','too','between','family','mean','talk','same','might',
	'over','company','so','small','next','live','home','lot','national','though','far','game',
	'important','after','ever','law','set','nothing','white','minute','back','door','stop',
	'teacher','history','morning','guy','although','able','music','human','experience',
	'plan','effect','development','care','show','pass','up','report','model','mind','drive',
	'receive','even','wear','site','early','event','table','oil','recent','news','hair','face',
	'cover','baby','organization','open','listen','behavior','plant','realize','choice','husband',
	'call','thousand','west','private','upon','fill','quickly','movement','store','hot','other',
	'analysis','identify','animal','occur','save','despite','attack','protect','simple','success',
	'knowledge','staff','section','deal','feeling','authority','democratic','hang','professor',
	'clearly','rather','cell','firm','claim','enjoy','main','imagine','finish','shoulder',
	'employee','specific','charge','politics','somebody','interview','top','pain','range','finger',
	'conference','purpose','property','address','owner','positive','score','painting','yard','cause',
	'victim','citizen','figure','reform','customer','assume','effective','therefore','critical','like',
	'southern','sky','hurt','scale','investigation','attend','generally','nine','replace','camp',
	'possibility','vision','stick','spot','roll','European','distance','understanding','supposed',
	'gold','crowd','associate','tool','guard','contribute','additional','band','earn','document',
	'marry','faith','annual','native','female','order','voter','gather','intelligence','classroom',
	'search','gift','ignore','until','moral','focus','twice','literature','appropriate','extend',
	'neighbor','promise','neck','medicine','instruction','visit','writing','device','famous','theater',
	'clean','sugar','software','northern','complex','scientific','map','mental','consequence','fourth',
	'minority','alone','trail','aid','revenue','bear','gender','prime','human','notion','anymore','like',
	'feature','currently','ought','bridge','fear','due','cat','perception','ad','accident','search','root',
	'hardly','frequently','chief','slow','funny','crazy','English','faculty','bond','ancient','eliminate',
	'producer','his','appeal','long','interaction','complain','initial','stretch','clear','improvement',
	'clean','check','rural','fashion','below','necessarily','seriously','wheel','bomb','dance','lack',
	'useful','noise','question','apart','milk','explanation','guilty','potential','celebrate','height',
	'first','depression','review','others']

