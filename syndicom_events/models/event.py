from odoo import fields,models

class Event(models.Model):
   _inherit = "event.event"
   syn_teamslink = fields.Char( string="MS Teams Link"  )
   syn_interactio = fields.Char( string="Interactio Code"  )
   syn_domain = fields.Char (string="Zielgruppe")
   syn_attachment_ids = fields.One2many('event.syndicom.attachment','event_id', string='Dokuemnte')
   syn_event_interpreter_ids = fields.One2many("event.syndicom.event2interpreter", 'event_id', string="Dolmetscher"  )
   syn_is_public = fields.Boolean(string='Öffentlich')
   
