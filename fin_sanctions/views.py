# -*- coding: utf-8 -*-
""" views controller """

from fin_sanctions import app


@app.route('/')
def index():
    return 'Hello World!'
