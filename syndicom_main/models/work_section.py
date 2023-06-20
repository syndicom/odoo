# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools


class SyndicomWorkLocationSection(models.Model):
    _name = 'syndicom.work.section'
    _description = 'Gruppen im Betrieb'
    name = fields.Char(string='Gruppe')
    work_location_id = fields.Many2one("syndicom.work.locations", string="Betrieb")
    parent_section_id = fields.Many2one(comodel_name='syndicom.work.section', string='Übergeordnete Gruppe')
    