# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomBindingOperators(models.Model):
    _name = 'syndicom.binding.operators'
    _description = 'Agenten für Bindungsgespräche'
    
    active = fields.Boolean(string='Aktiv',default=True)    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Kontakt')
    