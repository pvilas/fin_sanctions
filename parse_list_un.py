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
LIST_PATH = 'fin_sanctions/lists/consolidated.xml'


# logger inicialization
logger = logging.getLogger('parse_list_un')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    logger.debug('DB openned at ' + DB_PATH)
except Exception, e:
    logger.error(str(e))
    exit(1)

num_names = 0
num_pass = 0
num_births = 0
num_city = 0
num_addresses = 0


def nt(node, tag):
    """ returns text of the tag or None if the
        tag does not exist """
    if node.find(tag) is not None and node.find(tag).text is not None:
        return node.find(tag).text
    else:
        return None


def coalesce(lst):
    """ returns first item not None """
    for d in lst:
        if d is not None:
            return d

    return None


def join_commas(str_list, separator=u", ", final_mark='<br/>'):
    """ joins string with commas and appends a final mark """
    str_list = list(str_list)  # always a list

    # remove Nones
    try:
        while str_list.count(None):
            str_list.remove(None)
    except Exception, e:
        pass

    tuple_lst = tuple(str_list)
    str_pre = separator.join(map(unicode, tuple_lst))
    if str_pre != '':
        str_pre += final_mark
    return unicode(str_pre)


counter = 0  # to generate unique ids

try:

    # parse UN list and bypass root element (WHOLE)
    root = ET.parse(LIST_PATH).findall('./INDIVIDUALS')[0]

    entities = root.findall('INDIVIDUAL')

    # logger.debug(entities)

    logger.info("{0} entities to parse.".format(len(entities)))

    for e in entities:

        # entity
        o_entity = models.Entity(
            id=u'{0}{1}'.format(LIST_SUFFIX, nt(e, 'DATAID')),
            ent_type='P',  # always person
            legal_basis=nt(e, 'REFERENCE_NUMBER'),
            reg_date=nt(e, 'LISTED_ON'),
            pdf_link=None,
            programme=u'{0}{1}'.format(LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),
            remark=u'{0} Updated: {1}'.format(
                nt(e, 'COMMENTS1'),
                nt(e, 'LAST_DAY_UPDATED'))
        )
        try:
            db.session.add(o_entity)
            # logger.debug('Entity {0} added'.format(nt(e, 'DATAID')))
        except Exception, err:
            logger.error('Entity ' + str(err))
            exit(1)

        # make an str with all designations
        lst_desig = []
        desig = e.find('DESIGNATION')
        if desig is not None:
            desig = desig.findall('VALUE')
            if desig is not None:
                # logger.debug('Los valores de designacion son ' + str(desig))
                for d in desig:
                    lst_desig.append(unicode(d.text))
                    #logger.debug('afeixint ' + unicode(d.text))
                    # += u'{0}'.format(nt(d, 'VALUE')) + '; '

        str_desig = join_commas(lst_desig, separator=", ", final_mark=" ")

        # basic name
        logger.debug('creating base name')
        counter += 1

        g = nt(e, 'GENDER')
        if (g is None):
            g = 'Unknown'

        str_name = join_commas([
            nt(e, 'FIRST_NAME'),
            nt(e, 'SECOND_NAME'),
            nt(e, 'THIRD_NAME'),
            nt(e, 'FOURTH_NAME')],
            separator=" ",
            final_mark="")

        o_name = models.Name(id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                             entity_id=u'{0}{1}'.format(
            LIST_SUFFIX, nt(e, 'DATAID')),
            legal_basis=nt(e, 'REFERENCE_NUMBER'),
            reg_date=nt(e, 'LISTED_ON'),
            pdf_link=None,
            programme=u'{0}{1}'.format(
            LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

            last_name=nt(e, 'SECOND_NAME'),
            first_name=nt(e, 'FIRST_NAME'),
            whole_name=str_name,
            title=None,
            gender=g,
            function=str_desig,
            language=None,
            other=nt(e, 'NOTE')
        )
        try:
            db.session.add(o_name)
            # logger.debug(u'Name {0} added'.format(nt(e, 'SECOND_NAME')))
        except Exception, err:
            logger.error('Base name ' + str(err))
            exit(1)

        # names (alias ) of the entity
        noms = list(e.findall('INDIVIDUAL_ALIAS'))
        for n in noms:
            if nt(n, 'ALIAS_NAME') is not None:
                # alias can come separated by semicolon
                alias_list = map(unicode,
                                 nt(n, 'ALIAS_NAME').split(";"))
                alias_list = map(unicode.strip, alias_list)
                for al in alias_list:
                    counter += 1
                    num_names += 1
                    o_name = models.Name(
                        id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                        entity_id=u'{0}{1}'.format(
                            LIST_SUFFIX, nt(e, 'DATAID')),
                        legal_basis=nt(e, 'REFERENCE_NUMBER'),
                        reg_date=nt(e, 'LISTED_ON'),
                        pdf_link=None,
                        programme=u'{0}{1}'.format(
                            LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

                        last_name=None,
                        first_name=None,
                        whole_name=al,
                        title=None,
                        gender=None,
                        function=None,
                        language=None,
                        other=nt(n, 'NOTE')
                    )
                    try:
                        db.session.add(o_name)
                        # logger.debug(u'Alias {0} added'.format(al))
                    except Exception, err:
                        logger.error('Alias ' + str(err))
                        exit(1)

        # births
        births = list(e.findall('INDIVIDUAL_DATE_OF_BIRTH'))
        num_births += len(births)
        for b in births:
            p_date = coalesce([nt(b, 'DATE'), nt(b, 'YEAR')])
            if p_date is not None:
                counter += 1
                o_birth = models.Birth(
                    id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                    entity_id='{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'DATAID')),
                    legal_basis=nt(e, 'REFERENCE_NUMBER'),
                    reg_date=nt(e, 'LISTED_ON'),
                    pdf_link=None,
                    programme=u'{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

                    date=u'{0}'.format(p_date),
                    place=None,
                    country=None,
                    other=nt(b, 'NOTE')
                )
                try:
                    db.session.add(o_birth)
                    # logger.debug(
                    #     u'Date of birth {0} added'.format(nt(b, 'DATE')))
                except Exception, err:
                    logger.error('Date of birth ' + str(err))
                    exit(1)

        births = list(e.findall('INDIVIDUAL_PLACE_OF_BIRTH'))
        num_city += len(births)
        for b in births:
            if (nt(b, 'CITY') is not None) or (nt(b, 'COUNTRY') is not None):
                counter += 1
                o_birth = models.Birth(
                    id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                    entity_id=u'{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'DATAID')),
                    legal_basis=nt(e, 'REFERENCE_NUMBER'),
                    reg_date=nt(e, 'LISTED_ON'),
                    pdf_link=None,
                    programme=u'{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

                    date=None,
                    place=nt(b, 'CITY'),
                    country=nt(b, 'COUNTRY'),
                    other=nt(b, 'NOTE')
                )
                try:
                    db.session.add(o_birth)
                    # logger.debug(
                    #     u'Place of birth {0} added'.format(nt(b, 'CITY')))
                except Exception, err:
                    logger.error(
                        'Place of birth {0} '.format(
                            err))
                    exit(1)

        # passport
        passp = list(e.findall('INDIVIDUAL_DOCUMENT'))
        num_pass += len(passp)
        for p in passp:
            if nt(p, 'NUMBER') is not None:
                counter += 1
                o_pass = models.Passport(
                    id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                    entity_id=u'{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'DATAID')),
                    legal_basis=nt(e, 'REFERENCE_NUMBER'),
                    reg_date=nt(e, 'LISTED_ON'),
                    pdf_link=None,
                    programme=u'{0}{1}'.format(
                        LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

                    number=nt(p, 'NUMBER'),
                    country=nt(p, 'COUNTRY_OF_ISSUE'),
                    document_type=nt(p, 'TYPE_OF_DOCUMENT'),
                    other=nt(p, 'NOTE')
                )
                try:
                    db.session.add(o_pass)
                    # logger.debug(
                    #     u'Document {0} added'.format(nt(p, 'NUMBER')))
                except Exception, err:
                    logger.error('Passport ' + str(err))
                    exit(1)

        # address
        paddrs = list(e.findall('INDIVIDUAL_ADDRESS'))
        num_addresses += len(paddrs)
        for p in paddrs:
            counter += 1
            o_address = models.Address(
                id=u'{0}{1}'.format(LIST_SUFFIX, str(counter)),
                entity_id=u'{0}{1}'.format(
                    LIST_SUFFIX, nt(e, 'DATAID')),
                legal_basis=nt(e, 'REFERENCE_NUMBER'),
                reg_date=nt(e, 'LISTED_ON'),
                pdf_link=None,
                programme=u'{0}{1}'.format(
                    LIST_SUFFIX, nt(e, 'UN_LIST_TYPE')),

                number=nt(p, 'STATE_PROVINCE'),
                street=nt(p, 'STREET'),
                city=nt(p, 'CITY'),
                zipcode=nt(p, 'ZIP_CODE'),
                country=nt(p, 'COUNTRY'),
                other=nt(p, 'NOTE')
            )
            try:
                db.session.add(o_address)
                # logger.debug(
                #     u'Address {0} added'.format(nt(p, 'NUMBER')))
            except Exception, err:
                logger.error('Address ' + str(err))
                exit(1)

    # commit changes
    db.session.commit()

    logger.info('{0} entities, {1} names, {2} birth dates, {3} citizenship, {4} passports and {5} addresses created'.format(
        len(entities), num_names, num_births, num_city, num_pass, num_addresses))


except Exception, err:
    logger.error(str(err))
