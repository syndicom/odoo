# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta, date


class SyndicomvollzugDeclaration(models.Model):
    _name = 'syndicom.vollzug.declaration'
    _description = 'Vollzug Deklarationen'
    _inherit = ['mail.thread','mail.activity.mixin']
    name = fields.Char('Name',compute='_compute_name_field')
    active = fields.Boolean(string='Aktiv',default=True)  
    currency_id = fields.Many2one('res.currency', 'Währung')
    stage_id = fields.Many2one('syndicom.vollzug.declaration.stage',string='Stufe',group_expand='_read_group_stage_ids')
    enterprise_id = fields.Many2one('res.partner', 'Betrieb', index=True)
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
    total_ag = fields.Monetary(string='AG Beiträge', compute='_compute_billing_totals')
    total_an_tz = fields.Monetary(string='AN Beiträge TZ', compute='_compute_billing_totals')
    total_an_vz = fields.Monetary(string='AN Beiträge VZ', compute='_compute_billing_totals')
    total_an = fields.Monetary(string="AN Beiträge total", compute='_compute_billing_totals')
    total_total = fields.Monetary(string="AN + AG Beiträge total", compute='_compute_billing_totals')
    total_discount = fields.Monetary(string='Rabatt', compute='_compute_billing_totals')

    bill_count = fields.Integer(compute='_compute_bill_count')
    person_count = fields.Integer(compute="_compute_person_count")
    kanban_state = fields.Selection([   ('normal', 'Grey'),   ('done', 'Green'),   ('blocked', 'Red')], string='Kanban State',   copy=False, default='normal', required=True)
    is_closed = fields.Boolean(string='Abgeschlossen',compute="_check_is_closed")
    color = fields.Integer(string='Farbe')
    cla_partner = fields.Many2one(comodel_name='res.partner', string='GAV Partner')
    overdue = fields.Boolean(string='Fällig', compute='_compute_overdue')
    total_m = fields.Integer(string='Anz M.',readonly=True,compute='_compute_ma')
    total_w = fields.Integer(string='Anz W.',readonly=True,compute='_compute_ma')
    total_n = fields.Integer(string='Anz N.',readonly=True,compute='_compute_ma')    
    total_a = fields.Integer(string='Anz Lehrlinge',readonly=True,compute='_compute_ma')
    total_ma = fields.Integer(string='Anzahl Mitarbeiter',readonly=True, compute='_compute_ma')
    total_records = fields.Integer(string='Anz. Zeilen',readonly=True, compute='_compute_ma')
    move_id = fields.Many2one(comodel_name='account.move', string='Rechnung')
    duration_tz = fields.Integer(string='Anz. TZ',readonly=True,compute='_compute_duration')
    duration_vz = fields.Integer(string='Anz. VZ',readonly=True,compute='_compute_duration')
    duration = fields.Integer(string='Anz. Monate',readonly=True,compute='_compute_duration')
    duration_declaration = fields.Integer(string='Anz. Deklarationsmonate',readonly=True,compute='_compute_declaration_months')
    

    @api.model
    def _compute_declaration_months(self):
        for record in self:
            months = 0
            if record.date_from and record.date_to:
                months = (record.date_to.year - record.date_from.year) * 12 + (record.date_to.month - record.date_from.month)
                months = months + 1
            record.duration_declaration = months


    def _compute_duration(self):
        for record in self:
            person = self.env['syndicom.vollzug.declaration.person'].search([('declaration_id','=',record.id)])
            duration = 0
            duration_tz = 0
            duration_vz = 0
            for p in person:
                if p.employment_rate < 50:
                    duration_tz = duration_tz + p.duration_consolidated
                else:
                    duration_vz = duration_vz + p.duration_consolidated
                duration = duration + p.duration_consolidated
            record.duration_tz = duration_tz
            record.duration_vz = duration_vz
            record.duration = duration


    def _compute_ma(self):
        for record in self:
            person = self.env['syndicom.vollzug.declaration.person'].search([('declaration_id','=',record.id)])

            record.total_records = len(person)

            total_m = 0
            total_w = 0
            total_n = 0
            total_a = 0
            ahv = []
# Wenn es ein Datum Von hat, dann darf es nicht nach dem record.date_to sein
# Wenn es ein Datum Bis hat, dann darf es nicht vor dem record.date_from sein
            for p in person:
                is_valid = True
                
                #gueltig berechnen
                if p.date_entry != False:
                    if p.date_entry >= record.date_to:
                        is_valid = False
                        
                if p.date_leave != False:
                    if p.date_leave <= record.date_from:
                        is_valid = False
                        
                if p.date_leave == False and p.date_entry == False:
                    is_valid = False
                    
                #if (p.date_entry and (not p.date_entry > record.date_to)) and (p.date_leave and (not p.date_leave < record.date_from)):
                if is_valid == True:
                    if p.ssn not in ahv:
                        ahv.append(p.ssn)
                        if p.gender == 'w':
                            total_w+=1
                        elif p.gender == 'n':
                            total_n+=1
                        else:
                            total_m+=1
                        if p.is_apprentice == True:
                            total_a+=1

            record.total_m = total_m
            record.total_w = total_w
            record.total_n = total_n
            record.total_ma = len(ahv)
            record.total_a = total_a

    def _compute_billing_totals(self):
        """Compute billing data totals for company and employees."""
        # Getting settings records
        association_imputed_id = int(
            self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.association_imputed'),
        )
        ev_imputed_id = int(self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.ev_imputed'))
        for declaration in self:
            # Compute the AG totals
            persons = self.env['syndicom.vollzug.declaration.person'].search(
                [
                    ('declaration_id', '=', declaration.id),
                ],
            )
            declaration.total_ag = sum(persons.mapped('total_ag'))
            total_discount = sum(persons.mapped('discount_ag'))

            # Check the relation table to see if the enterprise is in a association, a ev or none of them
            is_association_this_month = self.env['res.partner.relation.all'].search(
                [
                    "&", "&", "&",
                    ("is_inverse", "=", False),
                    ("this_partner_id", "=", declaration.enterprise_id.id),
                    ("type_id", "=", association_imputed_id),
                    "|",
                    ("date_start", "<=", declaration.date_to),
                    "&",
                    ("date_end", "=", False),
                    ("date_end", ">=", declaration.date_from),
                ],
            )
            logic = 'nicht'
            for mon in is_association_this_month:
                if mon.other_partner_id.id == ev_imputed_id and logic != 'verband':
                    logic = 'ev'
                else:
                    logic = 'verband'

            discount_max = self.env['syndicom.vollzug.pricelist'].search(
                [
                    "&", "&", "&", "&",
                    ("gav_id", "=", declaration.cla_partner.id),
                    ("date_from", "<=", declaration.date_to),
                    ("category", "=", logic),
                    "|",
                    ("date_to", "=", False),
                    ("date_to", ">=", declaration.date_to),
                    "|",
                    ("active", "=", True), ("active", "=", False),
                ],
                limit=1,
            )

            max_discount = declaration.duration_declaration * discount_max.discount_max

            if total_discount <= max_discount:
                declaration.total_discount = total_discount
            else:
                declaration.total_discount = max_discount
            # Compute the AN totals
            declaration.total_an_tz = sum(persons.mapped(lambda p: p.total_an if p.employment_rate < 50 else 0))
            declaration.total_an_vz = sum(persons.mapped(lambda p: p.total_an if p.employment_rate >= 50 else 0))
            declaration.total_an = declaration.total_an_tz + declaration.total_an_vz
            # And finally the summed up total amount
            declaration.total_total = declaration.total_discount + declaration.total_an

    def _read_group_stage_ids(self, stage_id, domain, order):
        stage_ids = self.env['syndicom.vollzug.declaration.stage'].search([])
        return stage_ids

    def _compute_overdue(self):
        for record in self:
            if record.date_deadline < date.today():
                record.overdue = 1
            else:
                record.overdue = 0

    def button_declaration_bill_backend(self):
        return {
            'name': 'Rechnungen', 
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('id','=',self.move_id.id)]
            }

    def button_declaration_person_backend(self):
        return {
            'name': 'Deklarierte Personen',
            'view_mode': 'tree',
            #'view_id' : 'deklarierte_personen_tree_view',
            'res_model': 'syndicom.vollzug.declaration.person', 
            'type': 'ir.actions.act_window', 
            'domain': [('declaration_id','=',self.id)] 
            }
         
    def _compute_person_count(self):
        for res in self:
            res.person_count = len(self.env['syndicom.vollzug.declaration.person'].search([('declaration_id', '=', res.id)]))


    def _compute_bill_count(self):
        for res in self:
            if res.move_id.id > 0:
                res.bill_count = res.move_id.amount_total
            else:
                res.bill_count = 0



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
