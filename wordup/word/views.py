# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (
	Blueprint, 
	request, 
	render_template, 
	flash, 
	url_for,
	redirect, 
	session,
	)
from flask.ext.login import (
	login_user, 
	login_required, 
	logout_user,
	)
from  sqlalchemy.sql.expression import func

from wordup.extensions import login_manager
from wordup.user.models import User
from wordup.public.forms import LoginForm
from wordup.user.forms import RegisterForm
from wordup.utils import flash_errors
from wordup.database import db
from wordup.word.models import (
	Word,
	Prompt,
	Audio,
	Definition,
	)
from wordup.word.forms import SpellTry

blueprint = Blueprint('words', __name__, static_folder="../static")

@blueprint.route('/word')
def getword(word=None):
	form = SpellTry
	myword = Word.query.order_by(func.random()).first()
	return render_template('word/word.html', word=myword, myword=myword, spelltry_form=form)

# @blueprint.route('/word/<word>')
# def getword(word=None):
# 	myword = Word.query.filter_by(word=word).first()
# 	return render_template('word/word.html', word=word, myword=myword)
#