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




# prova = models.LegalBasis(id=u"hrrrla", reg_date=models.iso_date(
#     '2003-07-08'), pdf_link='http://adfasdfas.com/')
# db.session.add(prova)

# prova2 = models.LegalBasis(id=u"hrrrla", reg_date=models.iso_date(
#     '2003-07-08'), pdf_link='http://adfasdfas.com/')
# db.session.add(prova2)






# test if legal_basis exists
lb = db.session.query(LegalBasis).filter(LegalBasis.id == '2016/218 (OJ L40)')
if lb is None:
    lb = LegalBasis('2016/218 (OJ L40)', iso_date(reg_date), pdf_link)
self.legal_basis_id = lb

# test if programme exists
pr = db.session.query(Programme).filter(Programme.id == programme)
if pr is None:
    pr = Programme(id=programme)
self.programme = pr


o_entity = models.Entity(id='1',
                         ent_type='P',
                         legal_basis='2016/218 (OJ L40)',
                         reg_date='2016-02-18',
                         pdf_link="http://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0218&amp;from=EN",
                         programme="ZWE",
                         remark="(Entity is sanctioned in regime 310/2002 (OJ L50) of programme ZWE, in regime 314/2004 (OJ L55) of programme ZWE)"
                         )
db.session.add(o_entity)
logger.debug('commitant')
db.session.commit()
exit(0)


try:

    # parse EU list and bypass root element (WHOLE)
    root = ET.parse(EU_LIST_PATH).findall('.')[0]

    entities = root.findall('ENTITY')
    logger.info('{0} entities on the list'.format(len(entities)))

    # foreach entity
    for e in entities:
        print u'Id={0} Tipus={1} lb={2}'.format(e.attrib['Id'],
                                                e.attrib['Type'],
                                                e.attrib['legal_basis'])
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
        logger.debug(e.attrib['Id']+' added')

        # names of the entity
        noms = list(e.iter('NAME'))
        print "\tName list:"
        for n in noms:
            print u'\t\t{0}, {1} ({2})'.format(n.find('LASTNAME').text,
                                               n.find('FIRSTNAME').text,
                                               n.find('WHOLENAME').text)

        # birth
        births = list(e.iter('BIRTH'))
        print "\tBirth list:"
        for b in births:
            print u'\t\t{0} {1} {2}'.format(b.find('DATE').text,
                                            b.find('PLACE').text,
                                            b.find('COUNTRY').text)

        # passport
        passp = list(e.iter('PASSPORT'))
        print "\tPassport list:"
        for p in passp:
            print u'\t\tNumber: {0} Issued: {1}'.format(
                p.find('NUMBER').text,
                p.find('COUNTRY').text)

    # commit changes
    db.session.commit()

except Exception, e:
    logger.error(e.message)


