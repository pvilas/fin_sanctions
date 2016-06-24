""" Modeling EU XSD to sqlalchemy """
# -*- coding: utf-8 -*-
import enum
from fin_sanctions import db


class EntityType(enum.Enum):
    P = "Person"
    E = "Enterprise"

class GenderType(enum.Enum):
    M = "Male"
    F = "Female"    

class CalendarType(enum.Enum):
    G : "Gregorian"
    I : "Islamic"
    B : "Buddist"
    C : "Coptic"
    E : "Ethiopic"

    