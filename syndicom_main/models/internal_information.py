# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools import html_escape


class SyndicomInternalInformation(models.Model):
    _name = 'syndicom.internal.information'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Interne Informationen'
    
    name = fields.Char(string='Titel',  translate=True )
    teaser = fields.Html(string='Teaser', help='Dieser Text erscheint ebenfalls in einer allfälligen Ankündigung',  translate=True )    
    body = fields.Html(string='Inhalt',  translate=True , sanitize=False,   sanitize_tags=False,   sanitize_attributes=False)

    announcement_id = fields.Many2one(comodel_name='announcement', string='Verbundene Ankündigung') 
    category_id = fields.Many2one(comodel_name='syndicom.internal.category', string='Kategorie')
    

    image = fields.Binary(related='category_id.image', string='Bild')
    
    publish_date = fields.Date(string='Veröffentlichen ab')
    

    notify = fields.Boolean(string='Ankündigung?', help='Wenn diese Box ausgewählt wird, erscheint zum eigentlichen Newseintrag ebenfalls eine entsprechende Ankündigungsmeldung')        
    notify_from = fields.Datetime(string='Ankündigung ab')
    notify_till = fields.Datetime(string='Ankündigung bis')


    def create_announcement(self):
        for record in self:
            
            body = record.body

            button = "<a href='web#id=" + str(record.id) + "&model=syndicom.internal.information&view_type=form'>Info Intern öffnen</a><hr/>"

            announcement = self.env['announcement'].create({
                'active' : True,
                'name' : record.name,
                'is_general_announcement' : True,
                'notification_date' : record.notify_from,
                'notification_expiry_date' : record.notify_till,
                'content' : body,
            })

            record.announcement_id = announcement
   
