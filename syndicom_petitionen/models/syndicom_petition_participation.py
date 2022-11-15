# -*- coding: utf-8 -*-

from odoo import models, fields, api


class syndicom_petition_participation(models.Model):
    _name = 'syndicom.petition.participation'
    _description = 'List of all Participations on any Petitions'
    partner_id = fields.Many2one('res.partner', 'Teilnehmer')
    petition_id = fields.Many2one('syndicom.petition', 'Petition')
    category = fields.Selection(related='petition_id.category', readonly=True)    
    membership_state = fields.Selection(related='partner_id.membership_state', readonly=True)    
    lang = fields.Selection(related='partner_id.lang', readonly=True, string='Sprache')
    description = fields.Text(string="Beschreibung")
    date = fields.Date(string="Teilnahmedatum",default=lambda self: fields.datetime.now().date(),required=True)
    email = fields.Char(related='partner_id.email', readonly=True)    
    phone = fields.Char(related='partner_id.phone', readonly=True)
    city = fields.Char(related='partner_id.city', readonly=True)    
    zip = fields.Char(related='partner_id.zip', readonly=True)
    count_participation = fields.Integer(string='Anz. Teilnahmen', compute='_compute_count_participation')

    def _compute_count_participation(self):
        for res in self:
            participation = self.env['syndicom.petition.participation'].search([('partner_id','=',res.partner_id.id)])
            count = len(participation)
            res.count_participation = count
    

