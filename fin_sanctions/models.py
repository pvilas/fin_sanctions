""" Modeling EU XSD to sqlalchemy """
# -*- coding: utf-8 -*-
from fin_sanctions import db

DEFAULT_CODE_TYPE_LEN = 32
DEFAULT_DESCRIPTION_TYPE_LEN = 256
LARGE_DESCRIPTION_TYPE_LEN = 2048
DEFAULT_URL_TYPE_LEN = 256


class EntityType(db.Enum):
    """ entity type """
    P = "Person"
    E = "Enterprise"


class GenderType(db.Enum):
    """ Entity gender if person """
    M = "Male"
    F = "Female"


class CalendarType(db.Enum):
    """ Calendar type """
    G = "Gregorian"
    I = "Islamic"
    B = "Buddist"
    C = "Coptic"
    E = "Ethiopic"


class LegalBasis(db.Model):
    """ The regulation summary is a type that contains the main information
        about a regulation. """
    id = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN), primary_key=True)
    reg_date = db.Column(db.Date(), nullable=False)
    pdf_link = db.Column(db.String(DEFAULT_URL_TYPE_LEN), nullable=False)


class Country(db.Model):
    """ iso3 country code """
    id = db.Column(db.String(3), primary_key=True)
    description = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN),
                            nullable=False)


class Language(db.Model):
    """iso language code """
    id = db.Column(db.String(2), primary_key=True)
    description = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN),
                            nullable=False)


class Programme(db.Model):
    """ eu programme code (seems iso3) """
    id = db.Column(db.String(DEFAULT_CODE_TYPE_LEN), primary_key=True)
    description = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN),
                            nullable=True)


class Place(db.Model):
    """ convenience model to filter by place of birth.
        Place comes from Birth """
    id = db.Column(db.Integer(), primary_key=True)  # autoincremental
    # content of the place tag
    description = db.Column(
        db.String(DEFAULT_DESCRIPTION_TYPE_LEN), nullable=False)


class Entity(db.Model):
    """ Base class for an entity """
    id = db.Column(db.String(DEFAULT_CODE_TYPE_LEN), primary_key=True)
    ent_type = db.Enum(EntityType)
    legal_basis_id = db.Column(db.ForeignKey('legalbasis.id'), nullable=False)
    programme = db.Column(db.ForeignKey('programmes.id'), nullable=False)
    remark = db.Column(db.Text())


class Birth(db.Model):
    """ birth date for an entity """
    id = db.Column(db.String(DEFAULT_CODE_TYPE_LEN),
                   nullable=False,
                   primary_key=True)  # list code id
    entity_id = db.Column(db.ForeignKey('entity.id'), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    legal_basis_id = db.Column(db.ForeignKey('legalbasis.id'), nullable=False)
    place_id = db.Column(db.ForeignKey('place.id'), nullable=True)
    country = db.Column(db.ForeignKey('country.id'), nullable=True)


class Passport(db.Model):
    """ a passport of an entity"""
    id = db.Column(db.String(DEFAULT_CODE_TYPE_LEN),
                   nullable=False,
                   primary_key=True)  # list code id
    entity_id = db.Column(db.ForeignKey('entity.id'), nullable=False)
    legal_basis_id = db.Column(db.ForeignKey('legalbasis.id'), nullable=False)
    country = db.Column(db.ForeignKey('country.id'), nullable=True)
    number = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN))


class Name(db.Model):
    """ a name of an entity """
    id = db.Column(db.String(DEFAULT_CODE_TYPE_LEN),
                   nullable=False,
                   primary_key=True)  # list code id
    entity_id = db.Column(db.ForeignKey('entity.id'), nullable=False)
    legal_basis_id = db.Column(db.ForeignKey('legalbasis.id'), nullable=False)
    last_name = db.Column(
        db.String(DEFAULT_DESCRIPTION_TYPE_LEN), nullable=True)
    first_name = db.Column(
        db.String(DEFAULT_DESCRIPTION_TYPE_LEN), nullable=True)
    whole_name = db.Column(
        db.String(DEFAULT_DESCRIPTION_TYPE_LEN), nullable=True)
    gender = db.Enum(GenderType, nullable=True)
    title = db.Column(db.String(DEFAULT_CODE_TYPE_LEN), nullable=True)
    function = db.Column(db.Text(), nullable=True)
    language = db.Column(db.ForeignKey('entity.id'), nullable=True)
