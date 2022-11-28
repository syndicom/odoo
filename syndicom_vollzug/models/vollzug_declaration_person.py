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
    employment_rate = fields.Integer(string='Beschäftigungsgrad')
    duration = fields.Integer(string='Anz. Monate',compute="_compute_duration_in_month")
    total_an = fields.Monetary(string='AN Beitrag',compute="_compute_total_an")
    total_ag = fields.Monetary(string='AG Beitrag',compute="_compute_total_ag")
    salutation = fields.Char(string='Anrede')
    street = fields.Char(string='Adresse')
    zip = fields.Char(string='PLZ')
    city = fields.Char(string='Ort')
    birthday = fields.Date(string='Geburtstag')
    apprentice = fields.Boolean(string='Lehrling')
    ssn = fields.Char(string='AHV-Nummer')
    gender = fields.Selection([('m','Männlich'),('w','Weiblich'),('n','Neutral')])
    salary = fields.Float(string='Bruttolohn')
    zemis = fields.Char(string='Zemis')
    qualification = fields.Char(string='Qualifikation')
    field = fields.Char(string='Einsatzgebiet')
    job = fields.Char(string='Tätigkeit')
    
    
    


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
            #record.duration = delta.months +1
            total_months = delta.months
            if delta.years > 0:
                total_months = delta.years * 12 + total_months
            if delta.days >= 15:
                total_months = total_months + 1
            if total_months < 0:
                total_months = 0                
            record.duration = total_months
           

    # TODO berechnung anhand der GAV Beträge. 
    # TODO Lehrling muss pro GAV als zu berechnen / nicht zu berechenn einstellbar sein
    @api.depends('duration')
    def _compute_total_an(self):
        for record in self:
           
            if record.employment_rate < 50:
                record.total_an = record.duration * 10
            else:
                record.total_an = record.duration * 20
        

    @api.depends('duration')
    def _compute_total_ag(self):
        for record in self:
            
            if record.employment_rate < 50:
                record.total_ag = record.duration * 5
            else:
                record.total_ag = record.duration * 10
           


            