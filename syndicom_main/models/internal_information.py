# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import html_escape
from odoo.exceptions import UserError


class SyndicomInternalInformation(models.Model):
    _name = 'syndicom.internal.information'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Interne Informationen'
    
    name = fields.Char(string='Titel',  translate=True, readonly=True, compute='_compute_name' )
    teaser = fields.Html(string='Teaser', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',  translate=True, readonly=True, compute='_compute_teaser' )    
    body = fields.Html(string='Inhalt',  translate=True , sanitize=False,   sanitize_tags=False,   sanitize_attributes=False, readonly=True, compute='_compute_body')

    name_de = fields.Char(string='Titel Deutsch')
    teaser_de = fields.Html(string='Teaser Deutsch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',  sanitize=False,   sanitize_tags=False,   sanitize_attributes=False )    
    body_de = fields.Html(string='Inhalt Deutsch', sanitize=False,   sanitize_tags=False,   sanitize_attributes=False )
    name_fr = fields.Char(string='Titel Französisch')
    teaser_fr = fields.Html(string='Teaser Französisch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung' , sanitize=False,   sanitize_tags=False,   sanitize_attributes=False  )    
    body_fr = fields.Html(string='Inhalt Französisch', sanitize=False,   sanitize_tags=False,   sanitize_attributes=False  )
    name_it = fields.Char(string='Titel Italienisch')
    teaser_it = fields.Html(string='Teaser Italienisch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung', sanitize=False,   sanitize_tags=False,   sanitize_attributes=False  )    
    body_it = fields.Html(string='Inhalt Italienisch', sanitize=False,   sanitize_tags=False,   sanitize_attributes=False  )

    announcement_id = fields.Many2one(comodel_name='announcement', string='Verbundene Ankündigung') 
    category_id = fields.Many2one(comodel_name='syndicom.internal.category', string='Kategorie')
    

    image = fields.Binary(related='category_id.image', string='Bild')
    
    publish_date = fields.Date(string='Veröffentlichen ab')
    

    notify = fields.Boolean(string='Ankündigung?', help='Wenn diese Box ausgewählt wird, erscheint zum eigentlichen Newseintrag ebenfalls eine entsprechende Ankündigungsmeldung')        
    notify_from = fields.Datetime(string='Ankündigung ab')
    notify_till = fields.Datetime(string='Ankündigung bis')





    def create_announcement(self):
        for record in self:
            
            if record.name_de == False:
                raise UserError('Kein deutscher Titel eingetragen - dies muss zwingend erfüllt sein')
            if record.body_de == False:
                raise UserError('Kein deutscher Inhalt eingetragen - dies muss zwingend erfüllt sein')
            if record.notify_from == False:
                raise UserError('Die Ankündigung hat kein Start Datum - bitte eines eintragen und die Ankündigung erneut mit dem entsprechenden Button erstellen')
            if record.notify_till == False:
                raise UserError('Die Ankündigung hat kein Ende Datum - bitte eines eintragen und die Ankündigung erneut mit dem entsprechenden Button erstellen')

            user_deutsch = self.env['res.users'].sudo().search([('lang','in',['de_CH','en_US']),('is_syndicom_section','=',False),('is_syndicom_guest','=',False)])
            user_franz = self.env['res.users'].sudo().search([('lang','in',['fr_CH','it_IT']),('is_syndicom_section','=',False),('is_syndicom_guest','=',False)])
            user_all = self.env['res.users'].sudo().search([('is_syndicom_section','=',False),('is_syndicom_guest','=',False)])         

            html_before = record.category_id.html_before
            html_after = record.category_id.html_after
            
            if html_before:
                html_before = html_before.replace('{resid}',str(record.id))
            else:
                html_before = ''
            if html_after:
                html_after = html_after.replace('{resid}',str(record.id))
            else: 
                html_after = ''

            if record.name_fr and len(record.name_fr) > 1:
                deutsch = self.env['announcement'].sudo().create({
                        'active' : True,
                        'name' : record.name_de,
                        'content' : html_before + record.body_de + html_after,
                        'is_general_announcement' : False,
                        'notification_date' : record.notify_from,
                        'notification_expiry_date' : record.notify_till,
                        'announcement_type' : 'specific_users',
                        'specific_user_ids': user_deutsch.ids,
                    })                
                franz = self.env['announcement'].sudo().create({
                        'active' : True,
                        'name' : record.name_fr,
                        'content' : html_before + record.body_fr + html_after,
                        'is_general_announcement' : False,
                        'notification_date' : record.notify_from,
                        'notification_expiry_date' : record.notify_till,
                        'announcement_type' : 'specific_users',
                        'specific_user_ids': user_franz.ids,
                    })
            else:
                alle = self.env['announcement'].sudo().create({
                        'active' : True,
                        'name' : record.name_de,
                        'content' : html_before + record.body_de + html_after,
                        'is_general_announcement' : False,
                        'notification_date' : record.notify_from,
                        'notification_expiry_date' : record.notify_till,
                        'announcement_type' : 'specific_users',
                        'specific_user_ids': user_all.ids,
                    })        

    def _compute_name(self):
        for rec in self:

            fr = rec.with_context(lang='fr_CH')
            it = rec.with_context(lang='it_IT')
            de = rec.with_context(lang='de_CH')
            en = rec.with_context(lang='en_US')

            en.name = rec.name_de
            de.name = rec.name_de


            if rec.name_it:
                it.name = rec.name_it
            elif rec.name_fr:
                it.name = rec.name_fr
            else:
                it.name = rec.name_de

            if rec.name_fr:
                fr.name = rec.name_fr
            else:
                fr.name = rec.name_de
 

    def _compute_teaser(self):
        for rec in self:

            fr = rec.with_context(lang='fr_CH')
            it = rec.with_context(lang='it_IT')
            de = rec.with_context(lang='de_CH')
            en = rec.with_context(lang='en_US')

            en.teaser = rec.teaser_de
            de.teaser = rec.teaser_de


            if len(rec.teaser_it) > 13:
                it.teaser = rec.teaser_it
            elif len(rec.teaser_fr) > 13:
                it.teaser = rec.teaser_fr
            else:
                it.teaser = rec.teaser_de

            if len(rec.teaser_fr) > 13:
                fr.teaser = rec.teaser_fr
            else:
                fr.teaser = rec.teaser_de
 
        
    def _compute_body(self):
        for rec in self:
            
            fr = rec.with_context(lang='fr_CH')
            it = rec.with_context(lang='it_IT')
            de = rec.with_context(lang='de_CH')
            en = rec.with_context(lang='en_US')

            en.body = rec.body_de
            de.body = rec.body_de

            if len(rec.body_it) > 13:
                it.body = rec.body_it
            elif len(rec.body_fr) > 13:
                it.body = rec.body_fr
            else:
                it.body = rec.body_de

            if len(rec.body_fr) > 13:
                fr.body = rec.body_fr
            else:
                fr.body = rec.body_de


class ResAnnoucement(models.Model):
    _inherit = 'announcement'
    content = fields.Html(sanitize=False,   sanitize_tags=False,   sanitize_attributes=False )
