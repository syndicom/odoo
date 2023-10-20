from odoo import models, fields, api


class Announcement(models.Model):
    _inherit = 'announcement'

    name = fields.Char(string="Title", required=True, translate=True)
    content = fields.Html(translate=True)