# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class VollzugDeclarationStage(models.Model):
    _name = 'syndicom.vollzug.declaration.stage'
    _description = 'Deklarations Stufen'
    _order = 'sequence, id'

    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=50)
    name = fields.Char(required=True, translate=True)
    process_step = fields.Selection(string='Prozess Schritt', selection=[('0','Brief drucken'),('1', 'Erstellt & Aufforderung verschickt'), ('2', 'Antwort erhalten'),('3', 'In Bearbeitung'),('4', 'Erledigt'),('5', 'Abgebrochen'),])
    is_closed = fields.Boolean(string='Abschlusstatus')
    

    mail_template_id = fields.Many2one('mail.template', string='Email Template', domain=[('model', '=', 'syndicom.vollzug.declaration')],
        help="If set, an email will be sent to the customer when the project reaches this step.")
    fold = fields.Boolean('Folded in Kanban', help="This stage is folded in the kanban view.")