# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''
import re
from flask import flash

def flash_errors(form, category="warning"):
	'''Flash all errors for a form.'''
	for field, errors in form.errors.items():
		for error in errors:
			flash("{0} - {1}"
					.format(getattr(form, field).label.text, error), category)

def strip_target(exampletext,theword):
	preen = exampletext.strip()
	aword = r'(%s)' %(theword)
	return re.sub(aword, '______', preen, flags=re.IGNORECASE)