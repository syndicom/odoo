# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SyndicomMailSender(models.Model):
    _name = 'syndicom.mail.sender'
    _description = 'syndicom Mass Mailing senders'

    name = fields.Char(string='Name',translate=True)
    mail_from = fields.Char(string='Absender')
    reply_to = fields.Char(string='Antworten an')

    text_line1 = fields.Char(string='Absenderzeile 1')
    text_line2 = fields.Char(string='Absenderzeile 2')
    text_line3 = fields.Char(string='Absenderzeile 3')
    text_line4 = fields.Char(string='Absenderzeile 4')

    user_id = fields.Many2one(comodel_name='res.users', string='Gehört zu Benutzer')    
    user_ids = fields.Many2many(comodel_name='res.users', string='Berechtigte User')
    role_ids = fields.Many2many(
        comodel_name='res.users.role',
        relation="sender_syndicom_role_ids_rel",
        column1="sender_id",
        column2="syndicom_role_id",
        string='Berechtigung Gruppen')
    
    
    