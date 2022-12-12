# -*- coding: utf-8 -*-
from odoo import api, models,fields
from odoo import exceptions
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
import logging

_logger = logging.getLogger(__name__) 

class DeclarationStart(models.TransientModel):
    _name='syndicom.vollzug.declaration.wizard'
    _description='Deklarationen starten für alle in Frage kommenden Betriebe'
    periode_from=fields.Date(string='Von Datum',default=lambda self: date(fields.datetime.now().year,1,1),required=True)
    periode_to=fields.Date(string='Bis Datum',default=lambda self: date(fields.datetime.now().year,12,31),required=True)
 #   enterprise_ids = fields.Many2many('res.partner', 'syn_declaration_wizard_ids', string='Betriebe') #, compute="_get_all_enterprise_ids"
    enterprise_ids = fields.Many2many('syndicom.vollzug.declaration.check', 'declaration_wizard_ids', string='Betriebe') #, compute="_get_all_enterprise_ids"
    mail_template_id = fields.Many2one('mail.template',string="Vorlage")
    responsible_id = fields.Many2one('res.users',string='Verantwortlich')
    date_deadline = fields.Date(string='Frist',default=lambda self: date.today() + timedelta(days=31),required=True) 

    def declaration_create_wizard(self):
        wizard = self.env['syndicom.vollzug.declaration.wizard'].create({        
        'test_field': self.name
        })
        return {        
            'name': 'Assistent Deklarationen',        
            'type': 'ir.actions.act_window',        
            'res_model': 'syndicom.vollzug.declaration.wizard',        
            'view_mode': 'form',        
            'res_id': wizard.id,        
            'target': 'new'
            }


    def declaration_create_from_wizard(self):
        self.ensure_one()
        if not self.enterprise_ids:
            raise exceptions.UserError(
                "Keine Betriebe ausgewählt"
            )
        if not self.mail_template_id:
            raise exceptions.UserError(
                "Keine Mailvorlage ausgewählt"
            )
        for enterprise in self.enterprise_ids:
            nomail = False
            stage_id = self.env['syndicom.vollzug.declaration.stage'].search([('process_step','=',1)],limit=1).id

            this_enterpirse = self.env['res.partner'].search([('id','=',enterprise.id)],limit=1)
            if this_enterpirse.syn_declaration_no_mail == True:
                stage_id = self.env['syndicom.vollzug.declaration.stage'].search([('process_step','=',0)],limit=1).id
                nomail = True


            check_tbl = self.env['syndicom.vollzug.declaration.check'].search([('id','=',enterprise.id)],limit=1)
        
            declaration_date_from = self.periode_from
            declaration_date_to = self.periode_to

            if check_tbl.date_start != False:
                if declaration_date_from < check_tbl.date_start:
                    declaration_date_from = check_tbl.date_start
            if check_tbl.date_end != False:
                if declaration_date_to > check_tbl.date_end:
                    declaration_date_to = check_tbl.date_end

   
            if declaration_date_to > declaration_date_from:
                
                record = self.env['syndicom.vollzug.declaration'].create({  'name':'Deklaration',
                                                                            'enterprise_id':enterprise.id,
                                                                            'date_from':declaration_date_from,
                                                                            'date_to':declaration_date_to,
                                                                            'date_deadline':self.date_deadline,
                                                                            'responsible_id':self.responsible_id.id,
                                                                            'partner_id':check_tbl.partner_id,
                                                                            'email':check_tbl.email,
                                                                            'email_cc':check_tbl.email_cc,
                                                                            'count_mailings':1,
                                                                            'cla_partner':check_tbl.gav_id,
                                                                            'stage_id':stage_id})
                self.env.cr.commit()

                if nomail == False:
                    template = self.env['mail.template'].search([('id','=',self.mail_template_id.id)],limit=1)
                    template.send_mail(record.id)
           
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

class DeclarationStartEnterpriseLine(models.Model): 
    _inherit = "res.partner"
    syn_declaration_wizard_ids = fields.Many2many(
       "syndicom.vollzug.declaration.wizard",
       "enterprise_ids",
       string="Betriebe"  )