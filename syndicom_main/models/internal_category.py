# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomInternalCategory(models.Model):
    _name = 'syndicom.internal.category'
    _description = 'Kategorien für interne Kommunikation'
    
    name = fields.Char(string='Name')
    image = fields.Binary(string='Bild')
    

    html_before = fields.Html(sanitize=False)
    html_after = fields.Html(sanitize=False)

