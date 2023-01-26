from odoo import fields,models,api

class EventAttachment(models.Model):
   _name = 'event.syndicom.event2interpreter'
   #event_id = fields.Many2one('event.event', 'Event')
   interpreter_id = fields.Many2one('event.syndicom.interpreter', 'Dolmetscher')
   event_id = fields.Many2one('event.event', 'Event')
   amount_expenses = fields.Float(string='Spesen')
   amount_transport = fields.Selection(string='Transport', selection=[('0', 'Kein Transport'), ('20', '1 Weg'),('40','2 Wege')], default='0')
   amount_fee = fields.Float(string='Entschädigung')
   is_done = fields.Boolean(string='Verrechnet')

   @api.onchange('interpreter_id')
   def _onchange_interpreter_id(self):
      amount = 0
      default = self.env['event.syndicom.interpreter'].search([('id','=',self.interpreter_id.id)], limit = 1)
      amount = default.amount_fee
      self.amount_fee = amount

   
   

   

   
   
   