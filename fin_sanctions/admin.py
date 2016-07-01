# -*- coding: utf-8 -*-
""" site administration """

from fin_sanctions import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup
import urllib

import models


def entities_formatter(view, context, model, name):
    """ Format entities belonging a legal basis or programme """
    return Markup(models.entity_str_names(model))


def names_formatter(view, context, model, name):
    """ Format name's of an entity """
    str_names = u''
    for n in model.names:  # for each name
        str_names += u'{0}'.format(n.whole_name)
        if n.language_id is not None:
            str_names += ' ({0})'.format(n.language_id)
        str_names += '<br/>'
        # str_names += u'{0} ({1}, {2}, {3}, {4})<br/>'.format(
        #     n.whole_name, n.gender, n.title, n.function, n.language_id)

    return Markup(str_names)


def births_formatter(view, context, model, name):
    """ Format birth's date of an entity """
    str_names = u''
    for n in model.births:  # for each birth date
        str_names += u'{0} '.format(n.date)
        if n.place_id is not None:
            str_names += u'<a href="http://www.google.com/maps/place/{0}"\
                 target="_blank">{1}</a>'.format(
                urllib.quote_plus(n.place_id.encode("ascii", "ignore")),
                n.place_id)

        if n.country_id is not None:
            str_names += u', ({0})'.format(n.country_id)
        str_names += '<br/>'

    return Markup(str_names)


def passports_formatter(view, context, model, name):
    """ Format passports and other info of an entity """
    str_names = u''
    for n in model.passports:  # for each birth date
        str_names += u'{0}'.format(n.number)
        if n.country_id is not None:
            str_names += u', ({0})'.format(n.country_id)
        str_names += '<br/>'

    # extra information from names
    if str_names != u'':  # prevent alone hr
        str_names += '<hr/>'

    for n in model.names:  # for each name
        if n.gender is not None:
            if n.gender == 'M':
                str_names += 'Male, '
            else:
                str_names += 'Female, '

        if n.title is not None:
            str_names += u' Title: {0}<br/>'.format(n.title)

        if n.function is not None:
            str_names += u'{0}<br/>'.format(n.function)

        str_names += '<br/>'

    return Markup(str_names)


def remarks_formatter(view, context, model, name):
    """ renders remark and links to the legal basis """
    str_names = u''
    if model.remark is not None:
        str_names += u'{0}<hr/>'.format(model.remark)

    str_names += '<a href="{0}" target="_blank">{1}</a><br/>'.format(
        model.legal_basis.pdf_link, model.legal_basis.id)

    return Markup(str_names)


class GenericModelView(ModelView):
    """ Generic model to admin tables """
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False
    column_display_actions = False
    column_display_pk = True
    can_view_details = True
    page_size = 50  # the number of entries to display on the list view


class EntityModelView(GenericModelView):
    """ customize entity model view """

    list_template = 'admin/entity/list.html'

    def _place_formatter(view, context, model, name):
        """ Format the url of the pdf to a link """
        if model.id is not None:
            pl = urllib.quote_plus(model.id.encode("ascii", "ignore"))
        else:
            pl = ''

        return Markup(u'<a href="{0}" target="_blank">{1}</a>'.format(
            pl, model.id))

    column_formatters = {
        'names': names_formatter,
        'births': births_formatter,
        'passports': passports_formatter,
        'remark': remarks_formatter
    }

    column_searchable_list = ['remark', 'names.whole_name',
                              'births.date', 'births.country_id',
                              'births.place_id',
                              'passports.number'
                              ]
    column_filters = ['names']
    column_sortable_list = ()
    column_list = ('names', 'births', 'passports',
                   'citizens', 'ent_type', 'remark')
    column_labels = dict(citizens='Citizen',
                         ent_type='Type',
                         births='Birth',
                         passports='Id and other info.',
                         remark='Remarks and legal basis')


class ProgrammeModelView(GenericModelView):
    """ customize programme view """
    column_formatters = {
        'entities': entities_formatter
    }

    column_list = ('id', 'entities')

    column_filters = ['id', 'entities']

    # _pr_choices = [(choice, label) for choice, label in [
    #     ('IRQ', 'Irak'),
    #     ('KRA', 'Korea')
    # ]]

    # column_choices = {
    #     'Prog': _pr_choices
    # }


class LegalBasisModelView(GenericModelView):
    """ customize entity model view """

    def _pdf_formatter(view, context, model, name):
        """ Format the url of the pdf to a link """
        return Markup('<a href="{0}" target="_blank">{1}</a>'.format(
            model.pdf_link, model.pdf_link))

    column_formatters = {
        'pdf_link': _pdf_formatter,
        'entities': entities_formatter
    }

    column_list = ('id', 'reg_date', 'entities', 'pdf_link')


class PlaceModelView(GenericModelView):
    """ customize Place list view """
    def _place_formatter(view, context, model, name):
        """ Formats place to link to google maps """
        return models.format_maps(model.id)

    column_formatters = {
        'id': _place_formatter
    }

    column_list = ('id',)

    column_default_sort = 'id'


#
# inicialització admin
admin = Admin(app, name='EU/UN Sanction List', template_mode='bootstrap3')
#admin.add_view(ModelView(models.User, db.session))
admin.add_view(EntityModelView(models.Entity, db.session))
# admin.add_view(LegalBasisModelView(models.LegalBasis, db.session))
# admin.add_view(ProgrammeModelView(models.Programme, db.session))
# admin.add_view(PlaceModelView(models.Place, db.session))
# admin.add_view(GenericModelView(models.Country, db.session))
# admin.add_view(GenericModelView(models.Language, db.session))
