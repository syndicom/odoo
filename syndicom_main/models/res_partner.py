from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    syndicom_account_report_ids = fields.One2many('syndicom.account.report', 'partner_id', string='Kontoauszüge')
    mobile = fields.Char(track_visibility='onchange')
    phone = fields.Char(track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street2 = fields.Char(track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    country_id = fields.Char(track_visibility='onchange')
    mediator_id = fields.Char(track_visibility='onchange')
    operating_unit_id = fields.Char(track_visibility='onchange')
    first_union_entry = fields.Char(track_visibility='onchange')
    anniversary_date = fields.Char(track_visibility='onchange')
