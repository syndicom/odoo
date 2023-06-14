# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SyndicomRecipientFilter(models.Model):
    _name = 'syndicom.recipient.filter'
    _description = 'syndicom Filter for generic Domains'

    name = fields.Char(string='Name',translate=True)
    description = fields.Char(string='Beschreibung')
    domain = fields.Char(string='Filter')
