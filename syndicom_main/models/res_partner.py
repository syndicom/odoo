from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    syndicom_account_report_ids = fields.One2many('syndicom.account.report', 'partner_id', string='Kontoauszüge')