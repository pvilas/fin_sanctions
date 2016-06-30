# -*- coding: utf-8 -*-
""" Parse xml EU data list and save on the DB """

import os
import sys
import logging
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from fin_sanctions import models

DB_PATH = str(os.path.join('',
                           'fin_sanctions/list.db'))
EU_LIST_PATH = 'fin_sanctions/lists/global.xml'


__author__ = 'https://github.com/pvilas'

app = Flask(__name__)

# logger inicialization
logger = logging.getLogger('parse_list_eu')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

engine = None
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    logger.debug('DB openned at ' + DB_PATH)
except Exception, e:
    logger.error(e.message)
    exit(1)

num_names = 0
num_pass = 0
num_births = 0

try:

    # parse EU list and bypass root element (WHOLE)
    root = ET.parse(EU_LIST_PATH).findall('.')[0]

    entities = root.findall('ENTITY')

    # foreach entity
    for e in entities:
        # print u'Id={0} Tipus={1} lb={2}'.format(e.attrib['Id'],
        #                                         e.attrib['Type'],
        #                                         e.attrib['legal_basis'])
        o_entity = models.Entity(id=e.attrib['Id'],
                                 ent_type=e.attrib['Type'],
                                 legal_basis=e.attrib['legal_basis'],
                                 reg_date=e.attrib['reg_date'],
                                 pdf_link=e.attrib['pdf_link'],
                                 programme=e.attrib['programme'],
                                 remark=e.attrib['remark']
                                 )
        db.session.add(o_entity)
        db.session.commit()
        logger.debug(e.attrib['Id'] + ' added')

        # names of the entity
        noms = list(e.iter('NAME'))
        num_names += len(noms)
        # print "\tName list:"
        for n in noms:
            # print u'\t\t{0}, {1} ({2})'.format(n.find('LASTNAME').text,
            #                                    n.find('FIRSTNAME').text,
            #                                    n.find('WHOLENAME').text)
            o_name = models.Name(id=n.attrib['Id'],
                                 entity_id=n.attrib['Entity_id'],
                                 legal_basis=n.attrib['legal_basis'],
                                 reg_date=n.attrib['reg_date'],
                                 pdf_link=n.attrib['pdf_link'],
                                 programme=n.attrib['programme'],
                                 last_name=n.find('LASTNAME').text,
                                 first_name=n.find('FIRSTNAME').text,
                                 whole_name=n.find('WHOLENAME').text,
                                 title=n.find('TITLE').text,
                                 gender=n.find('GENDER').text,
                                 function=n.find('FUNCTION').text,
                                 language=n.find('LANGUAGE').text
                                 )
            db.session.add(o_name)
            db.session.commit()
            logger.debug('\tName ' + n.attrib['Id'] + ' added')

        # births
        births = list(e.iter('BIRTH'))
        num_births += len(births)
        # print "\tBirth list:"
        for b in births:
            # print u'\t\t{0} {1} {2}'.format(b.find('DATE').text,
            #                                 b.find('PLACE').text,
            #                                 b.find('COUNTRY').text)
            o_birth = models.Birth(id=b.attrib['Id'],
                                   entity_id=b.attrib['Entity_id'],
                                   legal_basis=b.attrib['legal_basis'],
                                   reg_date=b.attrib['reg_date'],
                                   pdf_link=b.attrib['pdf_link'],
                                   programme=b.attrib['programme'],
                                   date=b.find('DATE').text,
                                   place=b.find('PLACE').text,
                                   country=b.find('COUNTRY').text
                                   )
            db.session.add(o_birth)
            db.session.commit()
            logger.debug('\tBirth ' + b.attrib['Id'] + ' added')

        # passport
        passp = list(e.iter('PASSPORT'))
        num_pass += len(passp)
        # print "\tPassport list:"
        for p in passp:
            # print u'\t\tNumber: {0} Issued: {1}'.format(
            #     p.find('NUMBER').text,
            #     p.find('COUNTRY').text)
            o_pass = models.Passport(
                id=p.attrib['Id'],
                entity_id=p.attrib['Entity_id'],
                legal_basis=p.attrib['legal_basis'],
                reg_date=p.attrib['reg_date'],
                pdf_link=p.attrib['pdf_link'],
                programme=p.attrib['programme'],
                number=p.find('NUMBER').text,
                country=p.find('COUNTRY').text
            )
            db.session.add(o_pass)
            db.session.commit()
            logger.debug('\tPassport ' + p.attrib['Id'] + ' added')

    # commit changes
    db.session.commit()

    logger.info('{0} entities, {1} names, {2} birth dates and {3} passports created'.format(
        len(entities), num_names, num_births, num_pass))


except Exception, e:
    logger.error(e.message)