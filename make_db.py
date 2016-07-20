# -*- coding: utf-8 -*-

""" initialize db, please remove manuallythe database file first """

from fin_sanctions import db
# from fin_sanctions.security import user_datastore

db.create_all()  # creates all tables

# add user
# user_datastore.create_user(email="pvilas@gmail.com", password="pp")
db.session.commit()
