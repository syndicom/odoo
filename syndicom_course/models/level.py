# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomLevel(models.Model):
    _name = 'syndicom.course.level'
    active = fields.Boolean(string='Aktiv', default=True)    
    name = fields.Char(string='Level', required=True, translate=True)
    
    
