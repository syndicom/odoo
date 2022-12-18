from odoo import api, fields, models


class SyndicomTicketCostType(models.Model):
    _name = 'syndicom_ticket.costs.type'
    _description = 'Configuration of Cost Types'
    name = fields.Char(string='Name')
    helpdesk_ids = fields.Many2many(
       "helpdesk.team",
       string="Helpdesk Teams"  )