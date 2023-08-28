# -*- coding: utf-8 -*-
from odoo import models, fields, api



class SyndicomVollzugContactType(models.Model):
    _name = 'syndicom.vollzug.contact.type'
    _description = 'Vollzug Contact Type'
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', index=True)
    enterprise_id = fields.Many2one(comodel_name='res.partner', string='Betrieb', compute='_compute_enterprise_id', store=True, index=True)
    
    
    name = fields.Selection(string='Typ', selection=[('declaration', 'Deklaration'), 
                                                     ('information', 'GAV-Info'),
                                                     ('invoice', 'Rechnungen'),
                                                     ('controls', 'Kontrollen'),
                                                     ('privat', 'Privatadresse'),
                                                     ], index=True)

    is_main = fields.Boolean(string='Hauptkontakt')
    is_copy = fields.Boolean(string='Kopiekontakt')
    
    actual_main = fields.Many2one(comodel_name='res.partner', string='Aktueller Hauptkontakt', compute='_compute_actual_main', store=True)
    
    
    @api.depends('partner_id')
    def _compute_enterprise_id(self):
        for record in self:
            enterprise = record.partner_id
            if record.partner_id.parent_id != False:
                enterprise = record.partner_id.parent_id.id
            record.enterprise_id = enterprise


    @api.depends('is_main','is_copy','name')
    def _compute_actual_main(self):
        for record in self:

            return True
            # Set all Connections to the same Type for this Company to is_copy
            # if this record should be main
            """
            if record.is_main:
                update = self.env['syndicom.vollzug.contact.type'].search([('enterprise_id','=',record.enterprise_id.id),
                                                                ('name','=',record.name),
                                                                ('is_main','=',True),
                                                                ('partner_id','!=',record.partner_id.id)])
                for r in update:
                    u.write({'is_main': False, 'is_copy': True})

                record.actual_main = record.partner_id
            
            else:
                return True

            """
    