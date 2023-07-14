from odoo import fields,models

class Event(models.Model):
   _inherit = "event.event"
   
   date_registration_end = fields.Date(string='Anmeldeschluss')
   
   syn_teamslink = fields.Char( string="MS Teams Link"  )
   syn_interactio = fields.Char( string="Interactio Code"  )
   syn_domain = fields.Char (string="Zielgruppe")
   syn_attachment_ids = fields.One2many('event.syndicom.attachment','event_id', string='Dokuemnte')
   syn_event_interpreter_ids = fields.One2many("event.syndicom.event2interpreter", 'event_id', string="Dolmetscher"  )
   syn_is_public = fields.Boolean(string='Öffentlich')
   syn_annoucement = fields.Boolean(string='Vorankündigung / ohne Anmeldung')
   syn_publish_website_de = fields.Boolean(string='Auf deutsche Website')
   syn_publish_website_fr = fields.Boolean(string='Auf französische Website')
   syn_publish_website_it = fields.Boolean(string='Auf italienische Website')
   syn_publish_website_en = fields.Boolean(string='Auf englische Website')
   