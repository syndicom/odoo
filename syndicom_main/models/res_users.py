from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_syndicom_guest = fields.Boolean(string='Ist ein Gästeaccount')
    is_syndicom_section = fields.Boolean(string='Ist ein Sektionsuser')
    is_syndicom_gl = fields.Boolean(string='Ist ein Geschäftsleitungsuser')
    is_syndicom_bl = fields.Boolean(string='Ist ein Bereichsleiter')
    