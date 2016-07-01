# -*- coding: utf-8 -*-
""" Modeling EU XSD to sqlalchemy """
from fin_sanctions import app, db
from sqlalchemy import create_engine, MetaData
from datetime import datetime
from jinja2 import Markup
from flask import url_for
import urllib


DEFAULT_CODE_TYPE_LEN = 32
DEFAULT_DESCRIPTION_TYPE_LEN = 256
LARGE_DESCRIPTION_TYPE_LEN = 2048
DEFAULT_URL_TYPE_LEN = 256


def iso_date(iso_string):
    """ from iso string YYYY-MM-DD to python datetime.date
        Note: if only year is supplied, we assume month=1 and day=1
        This function is not longer used, dates from lists always are strings
    """
    if len(iso_string) == 4:
        iso_string = iso_string + '-01-01'
    d = datetime.strptime(iso_string, '%Y-%m-%d')
    return d.date()


def lb_create(legal_basis, reg_date, pdf_link):
    """ tests if a legal basis exists and if not, create it
        always returns the legal basis
        note the reg_date is a python Date object from iso string
    """
    lb = db.session.query(LegalBasis).filter(
        LegalBasis.id == legal_basis).first()
    if lb is None:
        lb = LegalBasis(id=legal_basis,
                        reg_date=reg_date,
                        pdf_link=pdf_link)
        db.session.add(lb)
        db.session.commit()
        lb = db.session.query(LegalBasis).filter(
            LegalBasis.id == legal_basis).first()
    return lb


def pr_create(programme, description=''):
    """ test if programme exists. if not create it and return object """
    pr = db.session.query(Programme).filter(
        Programme.id == programme).first()
    if pr is None:
        pr = Programme(id=programme, description=description)
        db.session.add(pr)
        db.session.commit()
        pr = db.session.query(Programme).filter(
            Programme.id == programme).first()
    return pr


def lg_create(language):
    """ creates and returns a language """
    lg = db.session.query(Language).filter(Language.id == language).first()
    if lg is None:
        lg = Language(id=language)
        db.session.add(lg)
        db.session.commit()
        lg = db.session.query(Language).filter(Language.id == language).first()
    return lg


def pl_create(place):
    """ creates and returns a place """
    pl = db.session.query(Place).filter(Place.id == place).first()
    if pl is None:
        pl = Place(id=place)
        db.session.add(pl)
        db.session.commit()
        pl = db.session.query(Place).filter(Place.id == place).first()
    return pl


def format_maps(pl):
    """ formats a place to a google maps link """
    return Markup(
        u'<a href="http://www.google.com/maps/place/{0}"'
        ' target="_blank">{1}</a>'.format(
            urllib.quote_plus(pl.encode("ascii", "ignore")),
            pl)
    )


def ct_create(country):
    """ creates and returns a country """
    ct = db.session.query(Country).filter(Country.id == country).first()
    if ct is None:
        ct = Country(id=country)
        db.session.add(ct)
        db.session.commit()
        ct = db.session.query(Country).filter(Country.id == country).first()
    return ct


def FK(model, nullable=False):
    """ constructs a fk column to the id field of the model model
        @model db.Model
        @nullable default false
    """
    return db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN),
                     db.ForeignKey(model.__tablename__ + '.id'),
                     nullable=nullable)


def ST(length=DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=False):
    """ constructs a column of type string """
    return db.Column(db.String(length), nullable=nullable,
                     primary_key=primary_key)


def entity_str_names(model):
    """ returns str list of names of the model """
    str_names = u''
    for e in model.entities:
        for n in e.names:
            str_names.join([u'<a href="{0}">{1}</a><br/>'.format(
                url_for('entity.edit_view', id=e.id),
                n.whole_name)])
    return str_names


class LegalBasis(db.Model):
    """ The regulation summary is a type that contains the main information
        about a regulation. """
    __tablename__ = 'legalbasis'
    id = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN), primary_key=True)
    reg_date = ST(DEFAULT_DESCRIPTION_TYPE_LEN)
    pdf_link = ST(DEFAULT_URL_TYPE_LEN)

    entities = db.relationship('Entity', back_populates="legal_basis")

    def __repr__(self):
        return "{0}".format(self.id)


class Country(db.Model):
    """ iso3 country code """
    __tablename__ = 'countries'
    id = ST(3, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)

    def __repr__(self):
        return "{0} {1}".format(self.id, self.description)


class Language(db.Model):
    """iso language code """
    __tablename__ = 'languages'
    id = ST(2, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)

    def __repr__(self):
        return "{0} {1}".format(self.id, self.description)


class Programme(db.Model):
    """ eu programme code (seems iso3) """
    __tablename__ = 'programmes'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)

    entities = db.relationship('Entity', back_populates="programme")

    def __repr__(self):
        return "{0}".format(self.id)


class Place(db.Model):
    """ convenience model to filter by place of birth.
        Place comes from Birth """
    __tablename__ = 'places'
    id = ST(DEFAULT_DESCRIPTION_TYPE_LEN, nullable=False, primary_key=True)

    def __repr__(self):
        return "{0}".format(self.id)


class Entity(db.Model):
    """ Base class for an entity """
    __tablename__ = 'entities'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    ent_type = db.Column(db.Enum('P', 'E', name='entity_type'), nullable=False)
    remark = db.Column(db.Text())

    legal_basis_id = FK(LegalBasis)
    programme_id = FK(Programme)

    legal_basis = db.relationship('LegalBasis', back_populates='entities')

    programme = db.relationship('Programme', back_populates='entities')

    names = db.relationship("Name")
    births = db.relationship("Birth")
    passports = db.relationship("Passport")
    citizens = db.relationship("Citizen")

    def __init__(self, id, ent_type,
                 legal_basis, reg_date,
                 pdf_link, programme, remark):
        """ creates entity from the list """
        self.id = id
        self.ent_type = ent_type
        self.remark = remark

        self.legal_basis_id = lb_create(legal_basis, reg_date, pdf_link).id
        self.programme_id = pr_create(programme).id

    def __repr__(self):
        return u"ENTITY Id: {0} Type: {1} Remark: {2}".format(
            self.id, self.ent_type, self.remark)


class Name(db.Model):
    """ a name of an entity """
    __tablename__ = 'names'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    entity_id = FK(Entity)
    legal_basis_id = FK(LegalBasis)
    programme_id = FK(Programme)
    language_id = FK(Language, True)
    last_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    first_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    whole_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    title = ST(DEFAULT_CODE_TYPE_LEN, True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    function = db.Column(db.Text(), nullable=True)

    def __init__(self, id, entity_id,
                 legal_basis, reg_date, pdf_link,
                 programme,
                 last_name, first_name, whole_name,
                 title, gender, function, language):
        """ creates name from the list """
        self.id = id
        self.entity_id = entity_id
        self.legal_basis_id = lb_create(legal_basis, reg_date, pdf_link).id
        self.programme_id = pr_create(programme).id
        if language is not None:
            self.language_id = lg_create(language).id
        self.last_name = last_name
        self.first_name = first_name
        self.whole_name = whole_name
        self.title = title
        self.gender = gender
        self.function = function

    def __repr__(self):
        return u"{0}".format(self.whole_name)


class Birth(db.Model):
    """ birth date for an entity """
    __tablename__ = 'births'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    entity_id = FK(Entity)
    date = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    legal_basis_id = FK(LegalBasis, False)
    programme_id = FK(Programme)
    place_id = FK(Place, True)
    country_id = FK(Country, True)

    def __init__(self, id, entity_id,
                 legal_basis, reg_date, pdf_link,
                 programme,
                 date, place, country):
        """ creates a birth date from the list """
        self.id = id
        self.entity_id = entity_id
        self.legal_basis_id = lb_create(legal_basis, reg_date, pdf_link).id
        self.programme_id = pr_create(programme).id
        self.date = date
        if place is not None:
            self.place_id = pl_create(place).id
        if country is not None:
            self.country_id = ct_create(country).id

    def __repr__(self):
        pl = self.place_id
        # if self.place_id is not None:
        #    pl = format_maps(u''+self.place_id)

        if self.country_id is not None:
            return Markup(u"{0} {1} {2}".format(self.date,
                                                pl, self.country_id))
        else:
            return Markup(u"{0} {1}".format(self.date, pl))


class Citizen(db.Model):
    """ citizenship of an entity """
    __tablename__ = 'citizens'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    entity_id = FK(Entity)
    legal_basis_id = FK(LegalBasis)
    programme_id = FK(Programme)
    country_id = FK(Country, True)

    def __init__(self, id, entity_id,
                 legal_basis, reg_date, pdf_link,
                 programme,
                 country):
        """ creates a citizen from the list, there is no guarantee that
            the citizen's country is already created  or use iso code
            so we create a new model """
        self.id = id
        self.entity_id = entity_id
        self.legal_basis_id = lb_create(legal_basis, reg_date, pdf_link).id
        self.programme_id = pr_create(programme).id
        if country is not None:
            self.country_id = ct_create(country).id

    def __repr__(self):
        return u"{0}".format(self.country_id)


class Passport(db.Model):
    """ a passport of an entity"""
    __tablename__ = 'passports'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    number = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)  # passport number
    entity_id = FK(Entity)
    legal_basis_id = FK(LegalBasis)
    programme_id = FK(Programme)
    country_id = FK(Country, True)

    def __init__(self, id, entity_id,
                 legal_basis, reg_date, pdf_link,
                 programme,
                 number, country):
        """ creates a passport from the list """
        self.id = id
        self.entity_id = entity_id
        self.legal_basis_id = lb_create(legal_basis, reg_date, pdf_link).id
        self.programme_id = pr_create(programme).id
        self.number = number
        if country is not None:
            self.country_id = ct_create(country).id

    def __repr__(self):
        if self.number is not None:
            return u"{0}".format(self.number)
        else:
            return ''
