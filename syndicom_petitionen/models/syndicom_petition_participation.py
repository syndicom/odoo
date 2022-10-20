# -*- coding: utf-8 -*-

from odoo import models, fields, api


class syndicom_petition_participation(models.Model):
    _name = 'syndicom.petition.participation'
    _description = 'List of all Participations on any Petitions'
    partner_id = fields.Many2one('res.partner', 'Teilnehmer')
    petition_id = fields.Many2one('syndicom.petition', 'Petition')
    description = fields.Text(string="Beschreibung")
    date = fields.Date(string="Teilnahmedatum")
    email = fields.Char(related='partner_id.email', readonly=True)    
    phone = fields.Char(related='partner_id.phone', readonly=True)
    city = fields.Char(related='partner_id.city', readonly=True)    
    zip = fields.Char(related='partner_id.zip', readonly=True)

