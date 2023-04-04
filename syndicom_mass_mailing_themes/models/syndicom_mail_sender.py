# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SyndicomMailSender(models.Model):
    _name = 'syndicom.mail.sender'
    _description = 'syndicom Mass Mailing senders'

    name = fields.Char(string='Name')
    mail_from = fields.Char(string='Absender')
    reply_to = fields.Char(string='Antworten an')
