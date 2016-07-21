# -*- coding: utf-8 -*-
""" App entry point """

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
db_path = str(os.path.join(app.root_path, 'list.db'))

#
# we use apsw to access directly to sqlite and its extensions
# we load spellfix1 extensionto match names and 
# passwords using levenshtein 
try:
    import apsw
    apsw_con=apsw.Connection(db_path)
    apsw_con.enableloadextension(True)
    apsw_con.loadextension('./fin_sanctions/spellfix1.so')
    app.logger.debug('spellfix1 extension loaded')
except Exception, e:
    app.logger.error("Failed to load apsw machinery: {0}".format(e))
    exit(1)

__author__ = 'https://github.com/pvilas'


#
# inicialització db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# convert_unicode=True)

import models

# create spell vocabulary
# models.create_vocabulary()

"""
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
"""

import views
import admin


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    app.logger.debug('set pragma')
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


"""
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    #app.logger.debug('Tancant DB')
    db_session.remove()
"""
