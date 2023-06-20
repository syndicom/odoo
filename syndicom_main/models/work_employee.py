# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools


class SyndicomWorkLocationEmployee(models.Model):
    _name = 'syndicom.work.employee'
    _description = 'Mitarbeiter bei Betrieb'
    _inherit = ['mail.thread','mail.activity.mixin']
    active = fields.Boolean(string='Aktiv',default=True)
    
    partner_id = fields.Many2one('res.partner', 'Kontakt')
    #member_service_id = fields.Many2one("member.service", string='Kontakt')
    work_location_id = fields.Many2one("syndicom.work.locations", string="Betrieb")
    section_id = fields.Many2one(comodel_name='syndicom.work.section', string='Gruppe', domain="[('work_location_id','=',work_location_id)]"  )
    
    confidant_partner_id = fields.Many2one(comodel_name='res.partner', string='Vertrauensperson')
    
    is_syndicom_member = fields.Boolean(related='partner_id.is_syndicom_member', readonly=True)  
    email = fields.Char(related='partner_id.email', readonly=True)  
    mobile = fields.Char(related='partner_id.mobile', readonly=True)  
    #language  = fields.Many2one(related='partner_id.lang', readonly=True)  

    rating = fields.Selection(string='Rating', selection=[('1', '1 - Top')
                                                        , ('2', '2')
                                                        , ('3', '3')
                                                        , ('4', '4')
                                                        , ('5', '5')
                                                        , ('6', '6 - Andere Gewerkschaft')])
    
    def open_to_employee_form(self):
 
        return {
            'name': ('Mitarbeitende bearbeiten'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('syndicom_main.work_employee_form_view').id,
            'res_model': 'syndicom.work.employee', 
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': self.id,
        }