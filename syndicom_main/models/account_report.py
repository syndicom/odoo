# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomAccountReport(models.Model):
    _name = 'syndicom.account.report'
    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    product_id = fields.Many2one(comodel_name='product.product', string='Produkt')
    move_id = fields.Many2one(comodel_name='account.move', string='Move')
    move_type = fields.Selection(string='Art', selection=[('invoice', 'Rechnung'), ('entry', 'Zahlungseingang')])
    amount = fields.Float(string='Betrag')    
    date = fields.Date(string='Datum')
    
    
