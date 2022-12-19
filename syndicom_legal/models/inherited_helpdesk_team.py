from odoo import fields,models

class HelpdeskTeam(models.Model):
   _inherit = "helpdesk.team"
   is_legal = fields.Boolean(string='Rechtsdienst', default=False)
   is_firstlevel = fields.Boolean(string='Firstlevel', default=False)
   