# -*- coding: utf-8 -*-
""" site administration """

from fin_sanctions import app, db
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup
import urllib



import models

list_titulo=''

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
    return separator.join(map(unicode, tuple_lst)) + final_mark


def format_country(ctry):
    """ formats a country.
        If is None returns None to chain with join_commas """
    if ctry is not None:
        return u" ({0})".format(ctry)
    else:
        return u''


def format_place(place):
    """ formats a place """
    if place is not None:
        return u'<a href="http://www.google.com/maps/place/{0}" target="_blank">{1}</a>'.format(
            urllib.quote_plus(place.encode("ascii", "ignore")),
            place)
    else:
        return u''


def coalesce_void(s):
    """ returns None if the string is void """
    if s == '':
        return None
    else:
        return s


def first_none(f, s):
    """ returns f+s if f is not None. None otherwise. """
    if f is not None:
        return u"{0} {1}".format(f, s)
    else:
        return None


def second_none(f, s):
    """ returns f+s if s is not None. None otherwise. """
    if s is not None:
        return u"{0} {1}".format(f, s)
    else:
        return None


def format_loc(place, country):
    """ return place (country) """
    return coalesce_void(
        format_place(place) +
        format_country(country))


def entities_formatter(view, context, model, name):
    """ Format entities belonging a legal basis or programme """
    return Markup(models.entity_str_names(model))


def names_formatter(view, context, model, name):
    """ Format name's of an entity """
    str_names = u''
    for n in model.names:  # for each name
        str_names += join_commas(
            [n.whole_name + format_country(n.language_id)],
            separator=" ")

    return Markup(str_names)


def births_formatter(view, context, model, name):
    """ Format birth's date of an entity """
    str_names = u''
    for n in model.births:  # for each birth date
        str_names += join_commas([
            n.date,
            format_loc(n.place_id, n.country_id)
        ])

    if model.addresses:
        if len(model.births) > 0:
            str_names += '<hr/>'
        str_names += 'Addresses:'

    for a in model.addresses:  # for each address
        str_names += '<br/>'

        str_names += join_commas([
            a.number,
            a.street,
            a.zipcode,
            format_loc(a.city, a.country_id),
            a.other
        ])

    return Markup(str_names)


def passports_formatter(view, context, model, name):
    """ Format passports and other info of an entity """
    str_names = u''

    for n in model.passports:  # for each birth date
        p = first_none(n.document_type, ': ') +\
            n.number +\
            format_country(n.country_id)
        if n.other is not None:
            p += u' ({0})'.format(n.other)

        str_names += p + '<br/>'

    # extra information from names
    if str_names != u'':  # prevent alone hr
        str_names += '<hr/>'

    for n in model.names:  # for each name

        str_names += join_commas([
            second_none(u' Title:', n.title),
            second_none(u' Function:', n.function),
            second_none(u'Sex: ', n.gender)
        ])

    return Markup(str_names)


def citizens_formatter(view, context, model, name):
    """ renders id and citizens """
    str_names = u'{0}<br/>{1}<br/>'.format(model.id, model.ent_type)

    for n in model.citizens:
        str_names += u'{0}<br/>'.format(n.country_id)

    return Markup(str_names)


def remarks_formatter(view, context, model, name):
    """ renders remark and links to the legal basis """
    str_names = u''
    if model.remark is not None and model.remark != '':
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
    column_display_actions = True
    can_edit = False

    list_template = 'admin/entity/list.html'

    list_titulo = None
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        # titol nomes amb un us
        if self.list_titulo is not None:
            self._template_args['list_titulo'] = self.list_titulo
            self.list_titulo=None

        app.logger.debug('helooo')
        return super(EntityModelView, self).index_view()


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
        'remark': remarks_formatter,
        'citizens': citizens_formatter
    }

    column_searchable_list = ['id', 'remark', 'names.whole_name',
                              'births.date', 'births.country_id',
                              'births.place_id',
                              'passports.number'
                              ]
    column_filters = ['id', 'names']
    column_sortable_list = ()
    column_list = ('names', 'births', 'passports',
                   'citizens', 'remark')
    column_labels = dict(citizens='List Id, type, citizen',
                         ent_type='Type',
                         births='Birth and address',
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
# admin.add_view(ModelView(models.User, db.session))
ent_ctrl=EntityModelView(models.Entity, db.session)
admin.add_view(ent_ctrl)
admin.add_view(LegalBasisModelView(models.LegalBasis, db.session))
admin.add_view(ProgrammeModelView(models.Programme, db.session))
# admin.add_view(PlaceModelView(models.Place, db.session))
# admin.add_view(GenericModelView(models.Country, db.session))
# admin.add_view(GenericModelView(models.Language, db.session))

"""
@app.context_processor
def admin_context_processor():
    return dict(list_titulo=list_titulo)
"""
