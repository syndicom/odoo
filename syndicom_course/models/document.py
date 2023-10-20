# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomCourseDocuments(models.Model):
    _name = 'syndicom.course.document'

    active = fields.Boolean(string='Aktiv', default=True)
    name = fields.Char('Name', required=True)
    document = fields.Binary(string='Dokument')
    
    
