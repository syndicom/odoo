from odoo import api, fields, models


class SyndicomTicketComsultingType(models.Model):
    _name = 'syndicom_ticket.consulting.type'
    _description = 'Configuration of Consulting Types'
    name = fields.Char(string='Name')
    helpdesk_ids = fields.Many2many(
       "helpdesk.team",
       string="Helpdesk Teams"  )