# -*- coding: utf-8 -*-
from odoo import models, fields


class SyndicomSpeaker(models.Model):
    _name = 'syndicom.course.speaker'
    name = fields.Char(string='Name', compute='_compute_name')
    active = fields.Boolean(string='Aktiv', default=True)    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Referent', required=True)
    employeer = fields.Char('Arbeitgeber')
    cv = fields.Char('Biografie', translate=True)
    
    def _compute_name(self):
        for record in self:
            if record.partner_id:
                record.name = record.partner_id.name
            else:
                record.name = 'unbekannt'