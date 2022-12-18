from odoo import api, fields, models


class SyndicomLegalCosts(models.Model):
    _name = 'syndicom_ticket.costs'
    _description = 'Costs to syndicom Tickets case'

    name = fields.Char(string='Name')
    description = fields.Text(string='Beschreibung')
    amount = fields.Float(string='Betrag')
    cost_id = fields.Many2one(comodel_name='syndicom_ticket.costs.type',string='Art')
    date = fields.Date(string='Datum')    
    ticket_id = fields.Many2one('helpdesk.ticket', 'Ticket')


    
    