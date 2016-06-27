""" App entry point """
# -*- coding: utf-8 -*-

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

import views


"""
from database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    #app.logger.debug('Tancant DB')
    db_session.remove()
"""
