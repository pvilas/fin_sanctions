# -*- coding: utf-8 -*-
""" views controller """

from flask import render_template, request, redirect
from fin_sanctions import app # , name_list, passport_list
from lev import levenshtein as lev
import timeit
from fin_sanctions import apsw_con
from distance import nlevenshtein


@app.route('/')
@app.route('/index.html')
def index():
    """ render index page """
    return render_template(
        'index.html')



@app.route('/search', methods=['POST'])
def search():
    """ search the database for names or passwords """
    app.logger.debug('entering search')
    try:
        query_name = request.form['inputName'] or None
        query_password = request.form['inputPassword'] or None
        query_distance = request.form['inputDistance'] or '40'
        query_distance = 1.0 - (float(query_distance)/100.0)
        query_name_len = query_password_len = 0

        app.logger.debug(u"{0} {1}".format(query_name, query_password))

        if query_name is not None:
            query_name = query_name.strip()
            query_name_len = len(query_name)

        if query_password is not None:
            query_password = query_password.upper().strip()
            query_password_len = len(query_password)

        score = []
        start_time = timeit.default_timer()
        
        if ((query_name is not None) or 
            (query_password is not None)):

            query_st = u'select rowid, word, distance from spell_{0} where word match ? order by distance limit 10' 

            param = ''
            query_spell_ref = ''
            root_filter= '/admin/entity/?flt0_5='
            query_filter_entity = ''

            if query_name is not None:
                query_stc = query_st.format(u'whole_name', query_distance)
                query_spell_ref = 'select entity_id from names where spell_ref=? limit 1'
                param = query_name
            else:
                query_stc = query_st.format(u'passport', query_distance)
                query_spell_ref = 'select entity_id from passports where spell_ref=? limit 1'
                param = query_password

            app.logger.debug(u''+query_stc+' '+param)            
            cursor=apsw_con.cursor()
            cursor2=apsw_con.cursor()

            for rowid, word, distance in cursor.execute(query_stc, (param,)):

                # distance in % by shortest alignment
                d = nlevenshtein(param.upper(), word.upper(), method=2)

                app.logger.debug(u'Distance between {0} and {1} is {2}'.format(
                            param,
                            word,
                            d
                            ))


                if d<=query_distance:
                    # find spell reference
                    for rf in cursor2.execute(query_spell_ref, (rowid,)):
                        if (len(query_filter_entity)==0):
                            query_filter_entity=rf[0]
                        else:
                            query_filter_entity+='%2C'+rf[0]    

                    score.append( (rowid, word, (1-d)*100) )

            et = 'Execution time: {0} s'.format(
                    timeit.default_timer() - start_time)

            return redirect(root_filter+query_filter_entity)


            # http://localhost:5000/admin/entity/?flt2_5=EU40%2CUN40

            """
            return render_template(
                'index.html',
                query_name=u"{0}".format(param),
                score=score,
                similarity=(1-query_distance)*100,
                execution_time=et)
            """    
        else:
            return render_template('index.html')

    except Exception, e:
        msg="Rendering error: {0}".format(e)
        app.logger.error(msg)
        return render_template('400.html', msg=msg)


"""
@app.route('/sasdf1', methods=['POST'])
def search1():
    def getKey(item):
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
"""        
