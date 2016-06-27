""" views controller """
# -*- coding: utf-8 -*-

from fin_sanctions import app


@app.route('/')
def index():
    return 'Hello World!'
