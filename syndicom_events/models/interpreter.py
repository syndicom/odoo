from odoo import fields,models,api

class EventAttachment(models.Model):
   _name = 'event.syndicom.interpreter'
   #event_id = fields.Many2one('event.event', 'Event')
   name = fields.Char('Name')
   partner_id = fields.Many2one('res.partner', 'Dolmetscher')
   amount_fee = fields.Float(string='Entschädigung')
   is_salary = fields.Boolean(string='Lohnempfänger')

   @api.onchange('partner_id')
   def _onchange_interpreter_id(self):
      name = 'Interpret'
      default = self.env['res.partner'].search([('id','=',self.partner_id.id)], limit = 1)
      name = default.name
      self.name = name
   
   
   
