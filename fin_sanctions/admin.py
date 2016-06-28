# -*- coding: utf-8 -*-
""" site administration """

from fin_sanctions import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import models


#
# inicialització admin
admin = Admin(app, name='EU/UN Sanction List', template_mode='bootstrap3')
#admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Entity, db.session))
admin.add_view(ModelView(models.LegalBasis, db.session))
admin.add_view(ModelView(models.Programme, db.session))
admin.add_view(ModelView(models.Country, db.session))
admin.add_view(ModelView(models.Language, db.session))
admin.add_view(ModelView(models.Place, db.session))

