# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomBindingConversation(models.Model):
    _name = 'syndicom.binding.conversations'
    _description = 'Durchgeführte Telefongespräche'
    
    
    operator_id = fields.Many2one(comodel_name='res.partner', string='Agent') 
    partner_id = fields.Many2one(comodel_name='res.partner', string='Kontakt')
    date_call = fields.Datetime(string='Zeitpunkt des Gesprächs')
    
    amount = fields.Float(string='Betrag')
    invalid = fields.Boolean(string='Ungültig')

    typ = fields.Selection(string='Typ', selection=[('feedback', 'Feedback'), 
                                                    ('treue', 'Treuegespräch'),
                                                    ('austritt', 'Austrittsgespräch'),
                                                    ])
    
    ticket_ids = fields.Many2many(comodel_name='helpdesk.ticket', string='Tickets')
    

    notes = fields.Char(string='Gesprächsnotizen')
    


    
