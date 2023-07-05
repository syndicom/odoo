from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'member.service'

    course_id = fields.Many2one(comodel_name='syndicom.course', string='Kurs')
    