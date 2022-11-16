# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta, date


class SyndicomvollzugDeclaration(models.Model):
    _name = 'syndicom.vollzug.declaration'
    _description = 'Vollzug Deklarationen'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char('Name',compute='_compute_name_field')
    currency_id = fields.Many2one('res.currency', 'Währung')
    stage_id = fields.Many2one('syndicom.vollzug.declaration.stage',string='Stufe',group_expand='_read_group_stage_ids')
    enterprise_id = fields.Many2one('res.partner', 'Betrieb')
    partner_id = fields.Many2one('res.partner', 'Kontakt')
    responsible_id = fields.Many2one('res.users','Verantwortlich') 
    email = fields.Text(string="E-Mail")
    email_cc = fields.Text(string="CCs")
    description = fields.Text(string='Beschreibung')
    contact_id = fields.Many2one('res.partner', 'Zuständig')
    person_ids = fields.One2many('syndicom.vollzug.declaration.person','declaration_id', string='Personen')
    date_from = fields.Date(string='Startdatum')#,default=lambda self: date(fields.datetime.now().year,1,1),required=True) #,compute='_check_cla_start_date')
    date_to = fields.Date(string='Enddatum')#,default=lambda self: date(fields.datetime.now().year,12,31),required=True)
    date_deadline = fields.Date(string='Frist')
    count_mailings = fields.Integer(string='Anzahl Aufforderungen')
    total_ag = fields.Monetary(string='AG Beiträge')
    total_an_tz = fields.Monetary(string='AN Beiträge TZ')
    total_an_vz = fields.Monetary(string='AN Beiträge VZ')
    total_discount = fields.Monetary(string='Rabatt')
    bill_count = fields.Integer(compute='_compute_bill_count')
    person_count = fields.Integer(compute="_compute_person_count")
    kanban_state = fields.Selection([   ('normal', 'Grey'),   ('done', 'Green'),   ('blocked', 'Red')], string='Kanban State',   copy=False, default='normal', required=True)
    is_closed = fields.Boolean(string='Abgeschlossen',compute="_check_is_closed")
    color = fields.Integer(string='Farbe')



    @api.model
    def _read_group_stage_ids(self, stage_id, domain, order):
        stage_ids = self.env['syndicom.vollzug.declaration.stage'].search([])
        return stage_ids

    def _check_cla_start_date(self):
        for record in self:
            cla_imputed = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_imputed')
            relation = self.env['res.partner.relation.all'].search([('active','=',True),('is_inverse','=',False),('this_partner_id','=',record.enterprise_id.id),('type_id','=',int(cla_imputed))],limit=1)
            cla_start_date = relation.date_start
            cla_end_date = relation.date_end
            if isinstance(cla_start_date,date) and cla_start_date > record.date_from:
                record.date_from = cla_start_date
            else:
                record.date_from = record.date_from
            if isinstance(cla_end_date,date) and record.date_to < cla_end_date:
                record.date_to = cla_end_date
        
    def button_declaration_bill_backend(self):
        return {
            'name': 'Rechnungen', 
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('id','>',0)]
            }

    def button_declaration_person_backend(self):
        return {
            'name': 'Deklarierte Personen',
            'view_mode': 'tree',
            'view_id' : 'deklarierte_personen_tree_view',
            'res_model': 'syndicom.vollzug.declaration.person', 
            'type': 'ir.actions.act_window', 
            'domain': [('declaration_id','=',self.id)] 
            }
         
    def _compute_person_count(self):
        for res in self:
            res.person_count = len(self.env['syndicom.vollzug.declaration.person'].search([('declaration_id', '=', res.id)]))


    def _compute_bill_count(self):
        for res in self:
            #   TODO Berechnung der anzahl Rechnungen verbunden mit der Deklaration                    total_len = len(self.env['job_applicant'].search([('job_type', '=', res.id)]))
            totel_len = 0
            res.bill_count = totel_len



    def _compute_name_field(self):
        for res in self:
            res.name = 'Deklaration für ' + res.enterprise_id.name

    @api.depends('stage_id')
    def _check_is_closed(self):
        for record in self:
            stage = self.env['syndicom.vollzug.declaration.stage'].search([('id','=',record.stage_id.id)],limit=1)
            if stage.is_closed == True:
                record.is_closed = 1
            else:
                record.is_closed = 0
