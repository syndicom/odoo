# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SyndicomWordLocations(models.Model):
    _name = 'syndicom.work.locations'
    _description = 'Betriebe und Unternehmensstandorte'
    _inherit = ['mail.thread','mail.activity.mixin']
    active = fields.Boolean(string='Aktiv',default=True)    
    name = fields.Char('Name', required=True)
    name_secondary = fields.Char(string='Zusatzname')

    building = fields.Char(string='Gebäude Kürzel')
    
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Arbeitgeber')
    city_id = fields.Many2one(comodel_name='res.city', string='Ort')
    street = fields.Char(string='Strasse')

    contact_phone = fields.Char(string='Kontaktnummer')

    total_employees = fields.Integer(string='Anzahl Mitarbeiter')

    responsible_id = fields.Many2one(comodel_name='res.users', string='Verantwortlich')
    access_ids = fields.Many2many(comodel_name='res.users', string='Zugriff für')
    employee_ids = fields.One2many('syndicom.work.employee', 'work_location_id', string='Mitarbeiter:innen')
    section_ids =  fields.One2many('syndicom.work.section', 'work_location_id', string='Gruppen')

    level_of_organization = fields.Float(string='Organisationsgrad',compute='_compute_level_of_organization')

    om_ref = fields.Integer(string='OM Kundennummer')
    

    def _compute_level_of_organization(self):
        for rec in self:

            level = 0

            if rec.total_employees:
                if rec.total_employees > 0:
                    level = 100 / rec.total_employees * len(rec.employee_ids) / 100

            rec.level_of_organization = level
    
    
    
    
    
    
