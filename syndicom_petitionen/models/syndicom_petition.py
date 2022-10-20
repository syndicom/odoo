# -*- coding: utf-8 -*-

from odoo import models, fields, api


class syndicom_petition(models.Model):
    _name = 'syndicom.petition'
    _description = 'List of all Petitions'
    name = fields.Char(string="Petition",translate=True,required=True)
    description = fields.Text(string="Beschreibung")
    date = fields.Date(string="Datum")
    total_participants = fields.Integer(string='Anzahl Teilnehmer',compute="_compute_total_participants")

    def _compute_total_participants(self):
        for res in self:
            res.total_participants = len(self.env['syndicom.petition.participation'].search([('petition_id', '=', res.id)]))
