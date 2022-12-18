# -*- coding: utf-8 -*-

from odoo import fields,models,api

class HelpdeskTeam(models.Model):
   _inherit = "helpdesk.ticket"
   currency_id = fields.Many2one('res.currency', 'Währung')
   syn_is_legal = fields.Boolean(string='Is Legal',related='team_id.is_legal')
   syn_is_firstlevel = fields.Boolean(string='Is Firstelevel',related='team_id.is_firstlevel')
   syn_received_on = fields.Date(string="Eingang am")
   syn_closed_on = fields.Date(string="Abgeschlossen am")
   syn_no_lock = fields.Boolean(string="Keine Austrittssperre")
   syn_external_lawyer_id = fields.Many2one('res.partner', 'Externer Anwalt')
   syn_cost_approved = fields.Monetary(string="Kostengutsprache")
   syn_final_comment = fields.Text(string="Abschlussergebnis")
   syn_legal_cost_ids = fields.One2many(
       "syndicom_ticket.costs",
       "ticket_id",
       string="Legal Costs"  )
   syn_total_cost = fields.Float(string='Total Kosten', compute='_compute_total_ticket_cost')
   syn_legal_request_type = fields.Selection(string='Anliegen', selection=[('privat', 'Privatrechtsschutz'),
                                                                           ('kollektiv', 'Kollektivfall'), 
                                                                           ('kuendigung', 'Kündigung'), 
                                                                           ('sozial', 'Sozialversicherungsrecht'),
                                                                           ('anderes', 'Anderes Thema'),
                                                                           ('non-member', 'Nicht- Mitglied')])
   syn_legal_request_notes = fields.Text(string='Bemerkungen')
   syn_legal_request_deadline = fields.Date(string='Frist')
   syn_legal_request_employer = fields.Char(string='Arbeitgeber')
   syn_legal_request_workplace = fields.Char(string='Arbeitsort')
   syn_legal_request_notice_date = fields.Date(string='Datum der Kündigung')
   syn_legal_request_notice_termination_date = fields.Date(string='Ende Arbeitsverhältnis gemäss Kündigungsschreiben')
   syn_legal_request_notice_working_since = fields.Date(string='Im Betrieb angestellt seit')
   syn_legal_request_notice_periode = fields.Char(string='Kündigungsfrist')
   syn_legal_request_notice_reason = fields.Text(string='Kündigungsgrund')
   syn_withdrawal_repayment = fields.Monetary(string='Betrag vorzeitiger Austritt')
   syn_is_non_member = fields.Boolean(string='Nicht Mitglied',default=False)
   syn_is_non_member_entry = fields.Boolean(string='Beitritt vollzogen',default=False)
   syn_legal_nonmember_sel = fields.Selection(string='Nicht-Mitglied Anliegen', selection=[('gav', 'GAV-Auskunft'),
                                                                           ('kollektiv', 'Kollektivfall'), 
                                                                           ('einzel', 'Einzelfall'), 
                                                                           ])

     
   
   def _compute_total_ticket_cost(self):
      for res in self:
         res.syn_total_cost = sum(self.env['syndicom_ticket.costs'].search([('ticket_id', '=', res.id)]).mapped('amount'))

