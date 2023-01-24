# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta, date
from dateutil import relativedelta

class SyndicomvollzugDeclarationPerson(models.Model):
    _name = 'syndicom.vollzug.declaration.person'
    name = fields.Char('Name')
    declaration_id = fields.Many2one('syndicom.vollzug.declaration', 'Deklaration')
    notice_id = fields.Many2one('syndicom.vollzug.notice', 'Meldung')
    place_id = fields.Many2one('syndicom.vollzug.notice.place', 'Einsatzgebiete')
    task_id = fields.Many2one('project.task', 'Personen')
    currency_id = fields.Many2one('res.currency', 'Währung')
    country_id = fields.Many2one('res.country', 'Land')
    firstname = fields.Char('Vorname')
    description = fields.Text(string='Beschreibung')
    contact_id = fields.Many2one('res.partner', 'Verbundener Kontakt')
    employeer_id = fields.Many2one('res.partner', 'Verbundener Betrieb')
    date_entry = fields.Date(string='Eintrittsdatum')
    date_leave = fields.Date(string='Austrittsdatum')
    personal_nr = fields.Char(string='Personalnummer')
    employment_rate = fields.Float(string='Beschäftigungsgrad')
    duration = fields.Integer(string='Anz. Monate',compute="_compute_duration_in_month")
    total_an = fields.Monetary(string='AN Beitrag',compute="_compute_total_an")
    total_ag = fields.Monetary(string='AG Beitrag',compute="_compute_total_ag")
    salutation = fields.Char(string='Anrede')
    street = fields.Char(string='Adresse')
    zip = fields.Char(string='PLZ')
    city = fields.Char(string='Ort')
    birthday = fields.Date(string='Geburtstag')
    apprentice = fields.Char(string='Lehrling')
    is_apprentice = fields.Boolean(string='Ist Lehrling', compute='_compute_apprentice')
    ssn = fields.Char(string='AHV-Nummer')
    gender = fields.Selection([('m','Männlich'),('w','Weiblich'),('n','Neutral')], compute='_compute_gender')
    salary = fields.Float(string='Bruttolohn')
    zemis = fields.Char(string='Zemis')
    qualification = fields.Char(string='Qualifikation')
    field = fields.Char(string='Einsatzgebiet')
    job = fields.Char(string='Tätigkeit')
    cla_partner = fields.Many2one(string='GAV Partner',related='declaration_id.cla_partner')
    duration_correction = fields.Integer(string='Korrektur')
    duration_consolidated = fields.Integer(string='Konsolidierte Anz. Monate', compute='_compute_duration_consolidated')
    
    @api.depends('duration','duration_correction')
    def _compute_duration_consolidated(self):
        for record in self:
            consolidated = record.duration + record.duration_correction
            if consolidated < 0: 
                consolidated = 0
            if consolidated > record.declaration_id.duration_declaration:
                consolidated = record.declaration_id.duration_declaration
            record.duration_consolidated = consolidated

    @api.depends('apprentice')
    def _compute_apprentice(self):
        for record in self:
            if str(record.apprentice).lower() in ['lehrling','apprentice','ja','si','oui','1','true','yes','apprenti','apprendi','apprendista','lernender','azubi','auszubildender']:
                record.is_apprentice = True
            else:
                record.is_apprentice = False

    @api.depends('salutation')
    def _compute_gender(self):
        for record in self:
            record.gender = 'n'
            if record.salutation:
                if record.salutation.lower() in ['herr','monsieur','mister','m','male','signor','mänlich','mrs','mrs.','m.','homme']:
                    record.gender = 'm'
                elif record.salutation.lower() in ['frau','madame','md','weiblich','f','w','female','signora','miss','ms','ms.','mme','femme']:
                    record.gender = 'w'

    @api.depends('date_leave','date_entry','employment_rate','apprentice')
    def _compute_duration_in_month(self):
        for record in self:

            date_entry = record.date_entry
            date_leave = record.date_leave
        
            if date_entry == False:
                date_entry = record.declaration_id.date_from
            if date_leave == False:
                date_leave = record.declaration_id.date_to
            if date_entry < record.declaration_id.date_from:
                date_entry = record.declaration_id.date_from
            if date_leave > record.declaration_id.date_to:
                date_leave = record.declaration_id.date_to


            if date_entry.day <= 14:
                date_entry = date(date_entry.year,date_entry.month,1)
            elif date_entry.month in (4,6,9,11) and date_entry.day in (15,16):
                date_entry = date(date_entry.year,date_entry.month,1)
            elif date_entry.month in (1,3,5,7,8,10,12) and date_entry.day in (15,16,17):
                date_entry = date(date_entry.year,date_entry.month,1)
            else:
                date_entry = date(date_entry.year,date_entry.month + 1,1)
                
            if date_leave.day >= 15:
                if date_leave.month == 2:
                    date_leave = date(date_leave.year,date_leave.month,28)
                elif date_leave.month in (4,6,9,11):
                    date_leave = date(date_leave.year,date_leave.month,30)
                else:
                    date_leave = date(date_leave.year,date_leave.month,31)
            else:
                date_leave = date(date_leave.year,date_leave.month,1)
                date_leave = date_leave - timedelta(days=1)
                
            delta = relativedelta.relativedelta(date_leave,date_entry)
            total_months = delta.months
            if delta.years > 0:
                total_months = delta.years * 12 + total_months
            if delta.days >= 15:
                total_months = total_months + 1
            if total_months < 0:
                total_months = 0                
            record.duration = total_months
           

    @api.depends('duration')
    def _compute_total_an(self):
        for record in self:

            if record.employment_rate:
                if record.employment_rate <= 1 and record.employment_rate > 0:
                    record.employment_rate = record.employment_rate * 100

            cla_partner_cc = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_cc')
            cla_partner_cc = str(cla_partner_cc) if cla_partner_cc else '0'
            cla_partner_nz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_nz')
            cla_partner_nz = str(cla_partner_nz) if cla_partner_nz else '0'

            # Calculation Logic Call Center
            if cla_partner_cc == str(record.cla_partner.id):
                if record.employment_rate < 50:
                    record.total_an = record.duration_consolidated * 10
                else:
                    record.total_an = record.duration_consolidated * 20
            # Calculation Logic Netzinfrastruktur
            elif cla_partner_nz == str(record.cla_partner.id):    
                if record.is_apprentice == True:
                    record.total_an = 0
                else:
                    if record.employment_rate < 50:
                        record.total_an = record.duration_consolidated * 10
                    else:
                        record.total_an = record.duration_consolidated * 20
            else:
                # Logic not found
                record.total_an = 0
               

    @api.depends('duration')
    def _compute_total_ag(self):
        for record in self:
            
            cla_partner_cc = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_cc')
            cla_partner_cc = str(cla_partner_cc) if cla_partner_cc else '0'
            cla_partner_nz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_nz')
            cla_partner_nz = str(cla_partner_nz) if cla_partner_nz else '0'

            # Calculation Logic Call Center
            if cla_partner_cc == str(record.cla_partner.id):
                record.total_ag = 0
            # Calculation Logic Netzinfrastruktur
            elif cla_partner_nz == str(record.cla_partner.id):    
                if record.is_apprentice == True:
                    record.total_ag = 0
                else:
                    record.total_ag = record.duration_consolidated * 5
            else:
                # Logic not found
                record.total_ag = 0
           


            