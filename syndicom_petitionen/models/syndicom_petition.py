# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta, date


class syndicom_petition(models.Model):
    _name = 'syndicom.petition'
    _description = 'List of all Petitions'
    name = fields.Char(string="Petition",translate=True,required=True)
    description = fields.Text(string="Beschreibung")
    date = fields.Date(string="Datum")
    date_end = fields.Date(string="Datum Ende")
    total_participants = fields.Integer(string='Anzahl Teilnehmer',compute="_compute_total_participants")
    category = fields.Selection(string='Kategorie', selection=[('s1', 'Sektor Logistik'), ('s2', 'Sektor ICT'),('s3', 'Sektor Medien'),('syn', 'syndicom'),('ig', 'Interessensgruppen'),])
    is_active = fields.Boolean(string='Aktiv',compute="_compute_is_active")
    
    
    def _compute_is_active(self):
        for res in self:
            print(fields.datetime.now().date())
            print(res.date)

            if res.date == False:
                date_start = fields.datetime.now().date()
            else:
                date_start = res.date

            if res.date_end == False:
                date_end = fields.datetime.now().date()
            else:
                date_end = res.date_end

            if date_start <= fields.datetime.now().date() and date_end >= fields.datetime.now().date():
                res.is_active = True
            else:
                res.is_active = False
           
    def _compute_total_participants(self):
        for res in self:
            res.total_participants = len(self.env['syndicom.petition.participation'].search([('petition_id', '=', res.id)]))

