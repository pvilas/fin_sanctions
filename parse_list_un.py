# -*- coding: utf-8 -*-
""" Parse xml UN data list and save on the DB.
    
    The mapping for the UN->EU list is:

        - individual -> entity
        - entity -> entity
        - 



 """


import os
import logging
import xml.etree.ElementTree as ET

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from fin_sanctions import models


__author__ = 'https://github.com/pvilas'

# to be added to each index
LIST_SUFFIX = 'UN'

DB_PATH = str(os.path.join('',
                           'fin_sanctions/list.db'))
LIST_PATH = 'fin_sanctions/lists/un.xml'


app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    app.logger.debug('DB openned at ' + DB_PATH)
except Exception, e:
    app.logger.error(e.message)
    exit(1)

num_names = 0
num_pass = 0
num_births = 0
num_city = 0
num_addresses = 0


counter = 0  # to generate unique ids

try:

    # parse UN list and bypass root element (WHOLE)
    root = ET.parse(LIST_PATH).findall('./INDIVIDUALS')[0]

    entities = root.findall('INDIVIDUAL')

    # app.logger.debug(entities)

    app.logger.debug("{0} entities to parse.".format(len(entities)))

    for e in entities:

        # entity
        o_entity = models.Entity(
            id=LIST_SUFFIX + e.find('DATAID').text,
            ent_type='P',  # always person
            legal_basis=e.find('REFERENCE_NUMBER').text,
            reg_date=e.find('LISTED_ON').text,
            pdf_link=None,
            programme=LIST_SUFFIX + e.find('UN_LIST_TYPE').text,
            remark=e.find('COMMENTS1').text + ' Updated: ' + \
            e.find('LAST_DAY_UPDATED').text
        )
        db.session.add(o_entity)
        db.session.commit()
        app.logger.debug(e.find('DATAID').text + ' added')

        # make an str with all designations
        str_desig = u''
        desig = e.iter('DESIGNATION')
        for d in desig:
            str_desig += d.find('VALUE') + '; '

        # basic name
        o_name = models.Name(id=LIST_SUFFIX + str(++counter),
                             entity_id=LIST_SUFFIX + e.find('DATAID').text,
                             legal_basis=e.find('REFERENCE_NUMBER').text,
                             reg_date=e.find('LISTED_ON').text,
                             pdf_link=None,
                             programme=LIST_SUFFIX +
                             e.find('UN_LIST_TYPE').text,
                             last_name=e.find('SECOND_NAME').text,
                             first_name=e.find('FIRST_TNAME').text,
                             whole_name=e.find(
                                 'SECOND_NAME').text + e.find(
                                 'FIRST_TNAME').text,
                             title=None,
                             gender=None,
                             function=str_desig,
                             language=None
                             )
        db.session.add(o_name)
        db.session.commit()

        # names (alias ) of the entity
        noms = list(e.findall('INDIVIDUAL_ALIAS'))
        num_names += len(noms)
        # print "\tName list:"
        for n in noms:
            o_name = models.Name(id=LIST_SUFFIX + str(++counter),
                                 entity_id=LIST_SUFFIX + e.find('DATAID').text,
                                 legal_basis=e.find('REFERENCE_NUMBER').text,
                                 reg_date=e.find('LISTED_ON').text,
                                 pdf_link=None,
                                 programme=None,
                                 last_name=None,
                                 first_name=None,
                                 whole_name=n.find('ALIAS_NAME').text,
                                 title=None,
                                 gender=None,
                                 function=None,
                                 language=None
                                 )
            db.session.add(o_name)
            db.session.commit()

        # births
        births = list(e.findall('INDIVIDUAL_DATE_OF_BIRTH'))
        num_births += len(births)
        # print "\tBirth list:"
        for b in births:
            # print u'\t\t{0} {1} {2}'.format(b.find('DATE').text,
            #                                 b.find('PLACE').text,
            #                                 b.find('COUNTRY').text)
            o_birth = models.Birth(
                id=LIST_SUFFIX + str(++counter),
                entity_id=LIST_SUFFIX + e.find('DATAID').text,
                legal_basis=e.find('REFERENCE_NUMBER').text,
                reg_date=e.find('LISTED_ON').text,
                pdf_link=None,
                programme=None,
                date=b.find('DATE').text + b.find('YEAR').text,
                place=None,
                country=None
            )
            db.session.add(o_birth)
            db.session.commit()

        births = list(e.findall('INDIVIDUAL_PLACE_OF_BIRTH'))
        num_births += len(births)
        # print "\tBirth list:"
        for b in births:
            # print u'\t\t{0} {1} {2}'.format(b.find('DATE').text,
            #                                 b.find('PLACE').text,
            #                                 b.find('COUNTRY').text)
            o_birth = models.Birth(
                id=LIST_SUFFIX + str(++counter),
                entity_id=LIST_SUFFIX + e.find('DATAID').text,
                legal_basis=e.find('REFERENCE_NUMBER').text,
                reg_date=e.find('LISTED_ON').text,
                pdf_link=None,
                programme=None,
                date=None,
                place=b.find('CITY').text,
                country=b.find('COUNTRY').text
            )
            db.session.add(o_birth)
            db.session.commit()

        # passport
        passp = list(e.findall('INDIVIDUAL_DOCUMENT'))
        num_pass += len(passp)
        # print "\tPassport list:"
        for p in passp:
            # print u'\t\tNumber: {0} Issued: {1}'.format(
            #     p.find('NUMBER').text,
            #     p.find('COUNTRY').text)
            o_pass = models.Passport(
                id=LIST_SUFFIX + str(++counter),
                entity_id=LIST_SUFFIX + e.find('DATAID').text,
                legal_basis=e.find('REFERENCE_NUMBER').text,
                reg_date=e.find('LISTED_ON').text,
                pdf_link=None,
                programme=None,
                number=p.find('NUMBER').text,
                country=p.find('COUNTRY_OF_ISSUE').text,
                document_type=p.find('TYPE_OF_DOCUMENT').text
            )
            db.session.add(o_pass)
            db.session.commit()


except Exception, e:
    app.logger.error(e.message)
