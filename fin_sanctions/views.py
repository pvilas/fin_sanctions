# -*- coding: utf-8 -*-
""" views controller """

from flask import render_template, request
from fin_sanctions import app, name_list, passport_list
from lev import levenshtein as lev
import timeit


@app.route('/')
@app.route('/index.html')
def index():
    return render_template(
        'index.html')


@app.route('/search', methods=['POST'])
def search():

    def getKey(item):
        """ return the position of the element that acts as
            a key to sort
            the score list """
        return -1 * item[3]

    query_name = request.form['name'] or None
    sorted_score = []
    et = 0

    if query_name is not None:
        query_name = query_name.upper()
        query_name_len = len(query_name)
        score = []

        start_time = timeit.default_timer()
        # perform lev for names_list and create score
        for n in name_list:
            # n[0] is the whole_name
            # n[1] is the entity_id
            # n[2] is the whole_name length in characters

            # edit distance from query_name to this whole_name
            s = lev(query_name, n[0])

            # the distance in % must be (len(word) - distance)/query_name_len
            percentual_distance = (1.0 * (n[2] - s)) / n[2]

            # app.logger.debug(u"{0}: {1} a {2} amb {3}%".format(
            #     n[0], s, query_name, percentual_distance))

            score.append(
                (s, n[1], n[0], percentual_distance)
            )

        # sort the list for the score
        sorted_score = sorted(score, key=getKey)
        sorted_score = sorted_score[:20]  # only 20 results

        et = 'Execution time: {0} s'.format(
            timeit.default_timer() - start_time)

    return render_template(
        'index.html',
        query_name=query_name,
        score=sorted_score,
        execution_time=et)
