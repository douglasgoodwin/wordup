from flask.ext.wtf import Form
from wtforms.fields import TextField
from wtforms.validators import Required

from wordup.word.models import (
	Word,
	# Prompt,
	# Audio,
	# Definition,
	)

class SpellTry(Form):
	word = TextField('Word', validators=[Required()])

