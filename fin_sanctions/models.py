# -*- coding: utf-8 -*-
""" Modeling EU XSD to sqlalchemy """
from fin_sanctions import app, db
from sqlalchemy import create_engine, MetaData

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


def FK(model, nullable=False):
    """ constructs a fk column to the id field of the model model
        @model db.Model
        @nullable default false
    """
    return db.Column(db.ForeignKey(model.__tablename__ + '.id'), nullable=nullable)


def ST(length=DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=False):
    """ constructs a column of type string """
    return db.Column(db.String(length), nullable=nullable, primary_key=primary_key)


class LegalBasis(db.Model):
    """ The regulation summary is a type that contains the main information
        about a regulation. """
    __tablename__ = 'legalbasis'
    id = db.Column(db.String(DEFAULT_DESCRIPTION_TYPE_LEN), primary_key=True)
    reg_date = db.Column(db.Date(), nullable=False)
    pdf_link = db.Column(db.String(DEFAULT_URL_TYPE_LEN), nullable=False)


class Country(db.Model):
    """ iso3 country code """
    __tablename__ = 'country'
    id = ST(3, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN)


class Language(db.Model):
    """iso language code """
    __tablename__ = 'language'
    id = ST(2, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN)


class Programme(db.Model):
    """ eu programme code (seems iso3) """
    __tablename__ = 'programme'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)


class Place(db.Model):
    """ convenience model to filter by place of birth.
        Place comes from Birth """
    __tablename__ = 'place'
    id = db.Column(db.Integer(), primary_key=True)  # autoincremental
    # content of the place tag
    description = ST(DEFAULT_DESCRIPTION_TYPE_LEN, False)


class Entity(db.Model):
    """ Base class for an entity """
    __tablename__ = 'entity'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    ent_type = db.Column(db.Enum('P', 'E'), nullable=False)
    legal_basis_id = FK(LegalBasis)
    programme = FK(Programme)
    remark = db.Column(db.Text())


class Birth(db.Model):
    """ birth date for an entity """
    __tablename__ = 'birth'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    entity_id = FK(Entity)
    date = db.Column(db.Date(), nullable=False)
    legal_basis_id = FK(LegalBasis, False)
    place_id = FK(Place, True)
    country = FK(Country, True)


class Passport(db.Model):
    """ a passport of an entity"""
    __tablename__ = 'passport'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    number = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)  # passport number
    entity_id = FK(Entity)
    legal_basis = FK(LegalBasis)


class Name(db.Model):
    """ a name of an entity """
    __tablename__ = 'name'
    id = ST(DEFAULT_CODE_TYPE_LEN, nullable=False, primary_key=True)
    entity_id = FK(Entity)
    legal_basis = FK(LegalBasis)
    last_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    first_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    whole_name = ST(DEFAULT_DESCRIPTION_TYPE_LEN, True)
    title = ST(DEFAULT_CODE_TYPE_LEN, True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    function = db.Column(db.Text(), nullable=True)
    language = FK(Language, True)
