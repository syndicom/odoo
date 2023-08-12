from odoo import fields,models,api

class Event(models.Model):
   _inherit = "event.registration"

   # Compute a Many2One field, wich return False if the registration
   # is either Canceld of Unconfirmed
   # so one can select easyle all confirmed registration via odoo domain fields
   booked_event_id = fields.Many2one(comodel_name='event.event', string='Teilnahme am Event',compute='_compute_booked_event_id',store=True)

   @api.depends('partner_id','event_id','state')
   def _compute_booked_event_id(self):
      for record in self:
        if record.state in ['open','done','draft']:
            record.booked_event_id = record.event_id.id
        else:
            record.booked_event_id = False

   