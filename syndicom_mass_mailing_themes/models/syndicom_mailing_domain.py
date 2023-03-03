##############################################################################
# Copyright (c) 2022 brain-tec AG (https://bt-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, fields, api


class MailingDomain(models.Model):
    _name = 'syndicom.mailing.domain'
    _description = "Domains for Mailing"

    name = fields.Char('Name', required=True)
    mailing_model_id = fields.Many2one(
        'ir.model', string='Recipients Model', ondelete='cascade', required=True,
        domain=[('is_mailing_enabled', '=', True)],
        default=lambda self: self.env.ref('mass_mailing.model_mailing_list').id)

    mailing_model_real = fields.Char(string='Recipients Real Model', compute='_compute_mailing_model_real',
                                     store=True)

    domain = fields.Char(default='[]')

    domain_usage = fields.Selection(
        [('mailing', 'Mailing'), ('print', 'Print')], default='mailing')

    @api.depends('mailing_model_id.model')
    def _compute_mailing_model_real(self):
        for record in self:
            if record.mailing_model_id.model != 'mailing.list':
                record.mailing_model_real = record.mailing_model_id.model
            else:
                record.mailing_model_real = 'mailing.contact'
