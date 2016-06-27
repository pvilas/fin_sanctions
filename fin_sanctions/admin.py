""" site administration """
# -*- coding: utf-8 -*-

from fin_sanctions import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import models


#
# inicialització admin
admin = Admin(app, name='EU/UN Sanction List', template_mode='bootstrap3')
#admin.add_view(ModelView(models.User, db.session))
