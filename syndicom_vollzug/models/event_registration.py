from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    partner_id = fields.Many2one(index=True)
