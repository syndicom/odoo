# -*- coding: utf-8 -*-
from odoo import api, models,fields,tools
from odoo import exceptions
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
import logging

_logger = logging.getLogger(__name__) 

class DeclarationStartReminder(models.TransientModel):
    _name='syndicom.vollzug.declaration.wizard.reminder'
    _description='Deklarationen Reminder starten für alle in Frage kommenden Betriebe'
    mail_template_remind_first_id = fields.Many2one('mail.template',string="Vorlage")
    mail_template_remind_second_id = fields.Many2one('mail.template',string="Vorlage")
    enterprise_ids = fields.Many2many('syndicom.vollzug.declaration.wizard.reminder.enterprise', 'declaration_wizard_reminder_ids', string='Betriebe') #, compute="_get_all_enterprise_ids"
    date_deadline = fields.Date(string='Neue Frist',default=lambda self: date.today() + timedelta(days=10),required=True) 

    def declaration_create_wizard_reminder(self):
        wizard = self.env['syndicom.vollzug.declaration.wizard.reminder'].create({        
        'test_field': self.name
        })
        return {        
            'name': 'Assistent Deklarationen Mahnungen',        
            'type': 'ir.actions.act_window',        
            'res_model': 'syndicom.vollzug.declaration.wizard.reminder',        
            'view_mode': 'form',        
            'res_id': wizard.id,        
            'target': 'new'
            }

    def declaration_create_from_wizard_reminder(self):

        self.ensure_one()
        if not self.enterprise_ids:
            raise exceptions.UserError(
                "Keine Betriebe ausgewählt"
            )
        if not self.mail_template_remind_first_id:
            raise exceptions.UserError(
                "Keine Mailvorlage ausgewählt"
            )
        for enterprise in self.enterprise_ids:
            stage_id = self.env['syndicom.vollzug.declaration.stage'].search([('process_step','=',1)],limit=1).id
            check_tbl = self.env['syndicom.vollzug.declaration.check'].search([('id','=',enterprise.id)],limit=1)
            declaration = self.env['syndicom.vollzug.declaration'].search([('id','=',enterprise.declaration_id)])
            for dec in declaration:
                dec.write({  
                    'date_deadline':self.date_deadline, 
                    'count_mailings': dec.count_mailings + 1,
                    'stage_id':stage_id})
                self.env.cr.commit()

                if dec.count_mailings == 2:            
                    template = self.env['mail.template'].search([('id','=',self.mail_template_remind_first_id.id)],limit=1)
                    template.send_mail(declaration.id)
                else:
                    template2 = self.env['mail.template'].search([('id','=',self.mail_template_remind_second_id.id)],limit=1)
                    template2.send_mail(declaration.id)
            
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

       

class DeclarationEnterpriseToRemind(models.Model):
    _name='syndicom.vollzug.declaration.wizard.reminder.enterprise'
    _auto=False
    _description='Enterprise to Remind'
    name = fields.Char('Name')
    gav = fields.Char(string='GAV')    
    zip = fields.Char(string='PLZ')
    city = fields.Char('Stadt')
    name_an = fields.Char(string='Hauptempfänger')
    email = fields.Char(string='An')
    email_cc = fields.Char(string='CCs')
    count_an = fields.Integer(string='Anz. AN')
    count_cc = fields.Integer(string='Anz. CCs')    
    date_start = fields.Date(string='GAV Unterstellt seit')
    date_end = fields.Date(string='GAV Unterstellt bis')
    partner_id = fields.Integer(string='Kontakt im Betrieb')
    lang = fields.Char(string='Sprache')
    count_mailings = fields.Integer(string='Anz. Auffoderungen')
    date_deadline = fields.Date(string='Frist')
    declaration_id = fields.Integer(string='Deklarations ID')
    

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):

        stage_id = self.env['syndicom.vollzug.declaration.stage'].search([('process_step','=',1)],limit=1)
        stage_id_waiting = str(stage_id.id) if stage_id else '0'

        return """

            SELECT 
                        p.id,
                        c.id partner_id,
                        p.name,
                        c.name gav,
                        p.zip,
                        p.city,
                        
                        (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True) count_an,
                        (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration_cc' and can.active = True) count_cc,
                        
                        case 
                            when (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True and can.email != '') = 0 then p.email
                            else (select email from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True and can.email != '' limit 1) end as email,
                            
                        case 
                            when (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True  and can.email != '') = 0 then ''
                            else (select name from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True  and can.email != '' limit 1) end as name_an,

                        case 
                            when (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True  and can.email != '') = 0 then p.lang
                            else (select lang from res_partner can where can.parent_id = p.id and can.type = 'declaration' and can.active = True  and can.email != '' limit 1) end as lang,
                            
                        case 
                            when (select count(*) from res_partner can where can.parent_id = p.id and can.type = 'declaration_cc' and can.active =  True  and can.email != '') = 0 then ''
                            else (select string_agg(email::text, ',') from res_partner can where can.parent_id = p.id and can.type = 'declaration_cc' and can.active = True  and can.email != '' limit 1) end as email_cc,

                        con.date_start,
                        con.date_end,
                        d.count_mailings,
                        d.date_deadline,
                        d.id declaration_id
                            
            FROM 
                        res_partner p
                        inner join  syndicom_vollzug_declaration d on d.enterprise_id = p.id and d.date_deadline < current_date  and d.stage_id = """ + stage_id_waiting + """
                        inner join 	res_partner_relation_all con on con.is_inverse = False and con.this_partner_id = p.id
                        inner join  res_partner_relation_type rel_type on rel_type.id = con.type_id and rel_type.cla_imputed_ok = True
                        inner join 	res_partner c on c.id = con.other_partner_id
           
            WHERE
                    p.active = True
                and p.is_company = True
                
            """
            #and d.is_closed = 0