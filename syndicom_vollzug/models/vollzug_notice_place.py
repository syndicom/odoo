# -*- coding: utf-8 -*-
from odoo import models, fields



class SyndicomVollzugNoticePlace(models.Model):
    _name = 'syndicom.vollzug.notice.place'
    _description = 'Vollzug Meldungen Place'
    name = fields.Char('Einsatzort')
    notice_id = fields.Many2one('syndicom.vollzug.notice', 'Meldung')
    date_from = fields.Date(string='Von')
    date_to = fields.Date(string='Bis')
    place = fields.Char(string='Genaue Adresse')
    remark = fields.Char(string='Bemerkung')
    person_ids = fields.One2many('syndicom.vollzug.declaration.person','place_id', string='Personen')
     