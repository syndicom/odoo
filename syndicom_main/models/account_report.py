# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomAccountReport(models.Model):
    _name = 'syndicom.account.report'
    _description = 'syndicom Kontoauszug für Mitglieder'
    _order = 'date asc'
    active = fields.Boolean(string='Aktiv',default=True)    
    name = fields.Char('Name', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    product_id = fields.Many2one(comodel_name='product.product', string='Produkt')
    move_id = fields.Many2one(comodel_name='account.move', string='Move')
    move_type = fields.Selection(string='Art', selection=[  ('invoice', 'Rechnung'), 
                                                            ('entry', 'Zahlungseingang'), 
                                                            ('payout','Auszahlung'), 
                                                            ('other','Anderes'),
                                                            ('start', 'Saldovortrag'), 
                                                            ('total', 'Total')])
    amount = fields.Float(string='Rechnung')    
    amount_payment = fields.Float(string='Zahlung')
    date = fields.Date(string='Datum')
    
    
