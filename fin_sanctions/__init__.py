# -*- coding: utf-8 -*-
""" App entry point """

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'https://github.com/pvilas'

app = Flask(__name__)

#
# inicialització db
db_path = str(os.path.join(app.root_path, 'list.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# convert_unicode=True)

import models
name_list = []
passport_list = []

# load all whole_names to a list
name_list = []  # list of all names
wn = models.Name.query.all()
for w in wn:
    name_list.append((w.whole_name.upper(), w.entity_id, len(w.whole_name)))
app.logger.debug("{0} names loaded".format(len(name_list)))

passport_list = []
pn = models.Passport.query.all()
for w in pn:
    passport_list.append((w.number.upper(), w.entity_id, len(w.number)))
app.logger.debug("{0} passports loaded".format(len(passport_list)))


import views
import admin


"""
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    #app.logger.debug('Tancant DB')
    db_session.remove()
"""
