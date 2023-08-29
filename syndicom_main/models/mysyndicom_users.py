# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from passlib.hash import bcrypt

class MySyndicomUsers(models.Model):
    _name = 'mysyndicom.users'
    _description = 'mysyndicom Benutzeraccounts'
    _inherit = ['mail.thread','mail.activity.mixin']
    active = fields.Boolean(string='Aktiv',default=True)
    partner_id = fields.Many2one('res.partner', 'Kontakt')
    username = fields.Char(string='Username')
    password = fields.Char(string='Passwort')
    password_hash = fields.Char(string='Hash')
    ticket_id = fields.Many2one(comodel_name='helpdesk.ticket', string='Registrationsanfrage')
    login_count = fields.Integer(string='Anz. Logins')
    
    is_initial = fields.Boolean(string='Initialpasswort')

    date_change = fields.Datetime(string='Letzte Passwortänderung')
    date_last_login = fields.Datetime(string='Letzter Anmeldeversuch')    

    wrong_password_count = fields.Integer(string='Anzahl Fehlversuche')
    
    
    
    
    @api.model
    @api.onchange('password')
    def _compute_password_hash(self):
        for record in self:
            if record.password:
                h = bcrypt.hash(record.password)
                record.is_initial = True
                record.password_hash = h                
            else:
                record.password_hash = record.password_hash

    @api.onchange('is_initial')
    def _compute_initial(self):
        for record in self:
            if record.is_initial == False:
                record.password = ''