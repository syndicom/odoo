# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import html_escape


class SyndicomInternalInformation(models.Model):
    _name = 'syndicom.internal.information'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Interne Informationen'
    
    name = fields.Char(string='Titel',  translate=True, readonly=True, compute='_compute_name' )
    teaser = fields.Html(string='Teaser', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',  translate=True, readonly=True, compute='_compute_teaser' )    
    body = fields.Html(string='Inhalt',  translate=True , sanitize=False,   sanitize_tags=False,   sanitize_attributes=False, readonly=True, compute='_compute_body')

    name_de = fields.Char(string='Titel Deutsch')
    teaser_de = fields.Html(string='Teaser Deutsch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',   )    
    body_de = fields.Html(string='Inhalt Deutsch', )
    name_fr = fields.Char(string='Titel Französisch')
    teaser_fr = fields.Html(string='Teaser Französisch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',  )    
    body_fr = fields.Html(string='Inhalt Französisch',  )
    name_it = fields.Char(string='Titel Italienisch')
    teaser_it = fields.Html(string='Teaser Italienisch', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',   )    
    body_it = fields.Html(string='Inhalt Italienisch',  )



    announcement_id = fields.Many2one(comodel_name='announcement', string='Verbundene Ankündigung') 
    category_id = fields.Many2one(comodel_name='syndicom.internal.category', string='Kategorie')
    

    image = fields.Binary(related='category_id.image', string='Bild')
    
    publish_date = fields.Date(string='Veröffentlichen ab')
    

    notify = fields.Boolean(string='Ankündigung?', help='Wenn diese Box ausgewählt wird, erscheint zum eigentlichen Newseintrag ebenfalls eine entsprechende Ankündigungsmeldung')        
    notify_from = fields.Datetime(string='Ankündigung ab')
    notify_till = fields.Datetime(string='Ankündigung bis')


    def create_announcement(self):
        for record in self:
            
            rec_fr = record.with_context(lang='fr_CH')
            rec_it = record.with_context(lang='it_IT')
            rec_de = record.with_context(lang='de_CH')
            rec_en = record.with_context(lang='en_US')

            #button = "<a href='web#id=" + str(record.id) + "&model=syndicom.internal.information&view_type=form'>Info Intern öffnen</a><hr/>"

            announcement = self.env['announcement'].create({
                'active' : True,
                'name' : record.name,
                'is_general_announcement' : True,
                'notification_date' : record.notify_from,
                'notification_expiry_date' : record.notify_till,
            })

            fr = announcement.with_context(lang='fr_CH')
            it = announcement.with_context(lang='it_IT')
            de = announcement.with_context(lang='de_CH')
            en = announcement.with_context(lang='en_US')

            fr.write({'name':rec_fr.name, 'content': rec_fr.body})
            it.write({'name':rec_it.name, 'content': rec_it.body})
            en.write({'name':rec_en.name, 'content': rec_en.body})
            de.write({'name':rec_de.name, 'content': rec_de.body})

            record.announcement_id = announcement

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


