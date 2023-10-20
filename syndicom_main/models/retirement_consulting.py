# -*- coding: utf-8 -*-
from odoo import models, fields


class RetirementConsulting(models.Model):
    _name = 'syndicom.retirement.consulting'         
    _description = 'Alle Pensionierungsberatungen'
    _inherit = ['mail.thread','mail.activity.mixin']

    active = fields.Boolean(string='Aktiv',default=True)    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Kontakt')
    consulter_id = fields.Many2one(comodel_name='res.partner', string='Berater')

    stage = fields.Selection(string='Stufe', selection=[('new', 'Neu'), 
                                                        ('open', 'Offen'),
                                                        ('done', 'Erledigt'),
                                                        ('cancel','Abgebrochen')])

    
    description = fields.Char(string='Informationen')
    contact_me_by = fields.Char(string='Kontaktaufnahme durch')

    date_takeover = fields.Datetime(string='Übernahmedatum')
    date_meeting = fields.Datetime(string='Termin Datum')
    date_done = fields.Datetime(string='Abschlussdatum')

    meeting_place = fields.Char(string='Termin Situngsort')
    meeting_remarks = fields.Char(string='Termin Bemerkungen')
    final_remarks = fields.Char(string='Abschluss Bemerkungen')

    expenses_travel = fields.Float(string='Reisespesen')
    expenses_catering = fields.Float(string='Verpflegungsspesen')
    expenses_overnight = fields.Float(string='Übernachtungsspesen')
    expenses_others = fields.Float(string='Spesen')
    fee = fields.Float(string='Honorar')
    expenses_ids = fields.Many2many(comodel_name='hr.expense', string='Aufwände')
    
    done_by = fields.Many2one(comodel_name='res.partner', string='Abgeschlossen durch')
    inactive_by = fields.Many2one(comodel_name='res.partner', string='Gelöscht durch')
    inactive_at = fields.Datetime(string='Inaktiv gestellt am')
    
    mail_feedback = fields.Boolean(string='Feedback Fragebogen verschickt')
    mail_operators = fields.Boolean(string='Benachrichtigung an Berater verschickt')
    


    
    
    
    
    


    