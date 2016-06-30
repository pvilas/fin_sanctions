# -*- coding: utf-8 -*-
""" site administration """

from fin_sanctions import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup
import urllib

import models


class GenericModelView(ModelView):
    """ Generic model to admin tables """
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False
    column_display_actions = False
    column_display_pk = True
    page_size = 50  # the number of entries to display on the list view


class EntityModelView(GenericModelView):
    """ customize entity model view """

    def _place_formatter(view, context, model, name):
        """ Format the url of the pdf to a link """
        if model.id is not None:
            pl = urllib.quote_plus(model.id.encode("ascii","ignore"))
        else:
            pl = ''    
        
        return Markup(u'<a href="{0}" target="_blank">{1}</a>'.format(
            pl, model.id))



    column_searchable_list = ['remark', 'names.whole_name',
                              'births.date', 'births.country_id', 
                              'births.place_id',
                              'passports.number'
                              ]
    column_filters = ['legal_basis.id', 'programme.id', 'names']
    column_list = ('names', 'births', 'passports', 'ent_type', 'remark')


class LegalBasisModelView(GenericModelView):
    """ customize entity model view """
    # column_searchable_list = ['remark', 'names.whole_name',
    #                           'births.date', 'births.country_id', 'births.place_id',
    #                           'passports.number'
    #                           ]
    # column_filters = ['legal_basis.id', 'programme.id', 'names']

    def _pdf_formatter(view, context, model, name):
        """ Format the url of the pdf to a link """
        return Markup('<a href="{0}" target="_blank">{1}</a>'.format(
            model.pdf_link, model.pdf_link))
        # Markup(
        #url_for('user.edit_view', id=model.user.id),
        # model.user
        #)
        # if model.pdf_link else ""

    column_formatters = {
        'pdf_link': _pdf_formatter
    }

    column_list = ('id', 'reg_date', 'pdf_link')


class PlaceModelView(GenericModelView):
    """ customize Place list view """
    def _place_formatter(view, context, model, name):
        """ Formats place to link to google maps """
        return models.format_maps(model.id)
 
    column_formatters = {
        'id': _place_formatter
    }

    column_list=('id',)

    column_default_sort='id'



#
# inicialització admin
admin = Admin(app, name='EU/UN Sanction List', template_mode='bootstrap3')
#admin.add_view(ModelView(models.User, db.session))
admin.add_view(EntityModelView(models.Entity, db.session))
admin.add_view(LegalBasisModelView(models.LegalBasis, db.session))
admin.add_view(GenericModelView(models.Programme, db.session))
admin.add_view(GenericModelView(models.Country, db.session))
admin.add_view(GenericModelView(models.Language, db.session))
admin.add_view(PlaceModelView(models.Place, db.session))
