from odoo import fields,models

class HelpdeskAnalyticLine(models.Model):
   _inherit = "account.analytic.line"
   syn_consulting_id = fields.Many2one(comodel_name='syndicom_ticket.consulting.type', string='Beratungsart')
   
   
   



