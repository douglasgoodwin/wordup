from flask.ext.admin import Admin
from flask.ext.admin import (
	Admin, 
	BaseView, 
	expose,
	)
from flask.ext.admin.contrib.sqla import ModelView

from wordup.user.models import (
	User,
	Role,
)
from wordup.word.models import (
	Word,
	# Audio,
	# Prompt,
)
from wordup.extensions import db



admin = Admin(name='WordUp!')

# Add views here
class MyView(BaseView):
	@expose('/')
	def index(self):
		return self.render('index.html')

class UserAdmin(ModelView):
	# Visible columns in the list view
	column_exclude_list = ['password']

# class PlaceAdmin(ModelView):
# 	# Visible columns in the list view
# 	foreign_key_lookups = {
# 		'feature': 'name',
# 		'category': 'name',
# 	}
# 	column_searchable_list = ( Place.name, Place.city )
# 	# place_category = relationship("w_accounts", backref=db.backref('categories', lazy='dynamic'))
# 	# column_select_related_list = ('place_category',)

admin.add_view(MyView(name='Hello'))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Word, db.session))
# admin.add_view(ModelView(UserRoles))
