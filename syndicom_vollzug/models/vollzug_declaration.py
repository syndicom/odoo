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
    total_ag = fields.Monetary(string='AG Beiträge', compute='_compute_total_ag')
    total_an_tz = fields.Monetary(string='AN Beiträge TZ', compute='_compute_total_an_tz')
    total_an_vz = fields.Monetary(string='AN Beiträge VZ', compute='_compute_total_an_vz')
    total_discount = fields.Monetary(string='Rabatt',readonly=True)
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

            for p in person:
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
            




    def _compute_total_ag(self):
        for record in self:
            total = 0
            person = self.env['syndicom.vollzug.declaration.person'].search([('declaration_id','=',record.id)])
            for p in person:
                total = total + p.total_ag
            
            association_imputed = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.association_imputed')
            association_imputed = str(association_imputed) if association_imputed else '0'
            cla_partner_cc = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_cc')
            cla_partner_cc = str(cla_partner_cc) if cla_partner_cc else '0'
            cla_partner_nz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_logic_nz')
            cla_partner_nz = str(cla_partner_nz) if cla_partner_nz else '0'
            # Calculation Logic Call Center
            if cla_partner_cc == str(record.cla_partner.id):
                record.total_ag = total

            # Calculation Logic Netzinfrastruktur
            elif cla_partner_nz == str(record.cla_partner.id):    
                if total > 4800:
                    record.total_ag = 4800
                else:
                    record.total_ag = total
                check_association = self.env['res.partner.relation.all'].search([('active','=',True),('is_inverse','=',False),('this_partner_id','=',record.enterprise_id.id),('type_id','=',int(association_imputed))],limit=1)
                if check_association:
                    record.total_discount = record.total_ag
                else:
                    record.total_discount = 0

            # Logic not found
            else:
                record.total_ag = 0
            
            

    def _compute_total_an_tz(self):
        for record in self:
            total = 0
            person = self.env['syndicom.vollzug.declaration.person'].search([('declaration_id','=',record.id)])
            for p in person:
                if p.employment_rate < 50:
                    total = total + p.total_an
            record.total_an_tz = total

    def _compute_total_an_vz(self):
        for record in self:
            total = 0
            person = self.env['syndicom.vollzug.declaration.person'].search([('declaration_id','=',record.id)])
            for p in person:
                if p.employment_rate >= 50:
                    total = total + p.total_an
            record.total_an_vz = total

    def _read_group_stage_ids(self, stage_id, domain, order):
        stage_ids = self.env['syndicom.vollzug.declaration.stage'].search([])
        return stage_ids

    def _compute_overdue(self):
        for record in self:
            if record.date_deadline < date.today():
                record.overdue = 1
            else:
                record.overdue = 0

    def _check_cla_start_date(self):
        for record in self:
            cla_imputed = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.cla_imputed')
            cla_imputed = str(cla_imputed) if cla_imputed else '0'

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

   
    def create_declaration_bill(self):
        for record in self:

            company = record.enterprise_id.company_id
            company_cc = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_company_cc')
            company_cc = str(company_cc) if company_cc else '0'
            company_nz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_company_nz')
            company_nz = str(company_nz) if company_nz else '0'

            product_ag = 0
            product_tz = 0
            product_vz = 0
            product_discount = 0

            if company == int(company_cc):
                product_ag = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_cc_ag')
                product_tz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_cc_tz')
                product_vz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_cc_vz')
                product_discount = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_cc_discount')
                ertrag_ver = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_ertrag_ver')
                ertrag_ave = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_ertrag_ave')
                ertrag_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_ertrag_org')
                ertrag_n_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_ertrag_n_org')
                deb_ver = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_deb_ver')
                deb_ave = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_deb_ave')
                deb_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_deb_org')
                deb_n_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_cc_deb_n_org')
            else:
                product_ag = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_nz_ag')
                product_tz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_nz_tz')
                product_vz = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_nz_vz')
                product_discount = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_prod_nz_discount')
                ertrag_ver = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_ertrag_ver')
                ertrag_ave = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_ertrag_ave')
                ertrag_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_ertrag_org')
                ertrag_n_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_ertrag_n_org')
                deb_ver = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_deb_ver')
                deb_ave = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_deb_ave')
                deb_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_deb_org')
                deb_n_org = self.env['ir.config_parameter'].sudo().get_param('syndicom_vollzug.syn_account_nz_deb_n_org')

            lines = []

            if record.total_ag > 0:
                lines.append((0, None, {
                    'product_id': int(product_ag),
                    'quantity': 1,
                    'price_unit': record.total_ag,
                    'account_id' : int(ertrag_ave),
                    }))
                lines.append((0, None, {
                    'debit': record.total_ag,
                    'account_id' : int(deb_ave),
                    'exclude_from_invoice_tab' : True,
                    }))

            if record.total_an_tz > 0:
                lines.append((0, None, {
                    'product_id': int(product_tz),
                    'quantity': record.duration_tz,
                    'price_unit': record.total_an_tz / record.duration_tz,
                    'account_id' : int(ertrag_org),
                    }))
                lines.append((0, None, {
                    'debit': record.total_an_tz,
                    'account_id' : int(deb_org),
                    'exclude_from_invoice_tab' : True,
                    }))

            if record.total_an_vz > 0:
                lines.append((0, None, {
                    'product_id': int(product_vz),
                    'quantity': record.duration_vz,
                    'price_unit': record.total_an_vz / record.duration_vz,
                    'account_id' : int(ertrag_org),
                    }))
                lines.append((0, None, {
                    'debit': record.total_an_vz,
                    'account_id' : int(deb_org),
                    'exclude_from_invoice_tab' : True,
                    }))

            if record.total_discount > 0:
                lines.append((0, None, {
                    'product_id': int(product_discount),
                    'quantity': 1,
                    'price_unit': record.total_discount,
                    'account_id' : int(ertrag_ave),
                    }))
                lines.append((0, None, {
                    'debit': record.total_discount,
                    'account_id' : int(deb_ave),
                    'exclude_from_invoice_tab' : True,
                    }))


            move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': record.enterprise_id.id,
            'company_id' : company,
            'currency_id': 5,
            'invoice_line_ids': lines,
            })

            record.move_id = move