from odoo import fields,models

class EventAttachment(models.Model):
   _name = 'event.syndicom.attachment'
   _order = 'sequence,id'
   sequence = fields.Integer(string='Sequence')
   event_id = fields.Many2one('event.event', 'Event')
   document = fields.Binary( string="Dokument", attachment=True  )
   document_filename = fields.Char(string='Dateiname')
   language = fields.Selection([('de_CH','Deutsch'),('it_IT','Italienisch'),('fr_CH','Französisch'),('en_US','Englisch')])
   
