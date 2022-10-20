from odoo import fields,models

class EventAttachment(models.Model):
   _name = 'event.syndicom.interpreter'
   event_id = fields.Many2one('event.event', 'Event')
   partner_id = fields.Many2one('res.partner', 'Dolmetscher')
   
