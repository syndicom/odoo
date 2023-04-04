# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.osv import expression
import ast


class MailingMailing(models.Model):
    _inherit = "mailing.mailing"

    syndicom_count = fields.Integer(
        string='Anz. Empfänger', compute='_compute_recipient_count')

    syndicom_filter_ids = fields.Many2many(
       comodel_name='syndicom.recipient.filter', string='Weiter Filter')

    syndicom_role_ids = fields.Many2many(
        comodel_name='res.users.role',
        relation="mailing_mailing_syndicom_role_ids_rel",
        column1="mailing_id",
        column2="syndicom_role_id",
        string='Berechtigung')

    syndicom_mail_sender = fields.Many2one(
       comodel_name='syndicom.mail.sender', string='Absender')

    syndicom_mailing_domain_ids = fields.Many2many(
        comodel_name="syndicom.mailing.domain",
        relation="mailing_mailing_syndicom_mailing_domain_rel",
        column1="mailing_id",
        column2="syndicom_mailing_domain_id",
        string="Verteiler")

    @api.model
    def default_get(self, fields_list):
        vals = super(MailingMailing, self).default_get(fields_list)
        vals.update({
            'mailing_model_id': self.env.ref('base.model_res_partner').id
        })
        return vals

    @api.depends('mailing_model_id', 'contact_list_ids',
                 'mailing_type', 'syndicom_mailing_domain_ids',
                 'syndicom_filter_ids', 'syndicom_mailing_topic_id')
    def _compute_recipient_count(self):
        """
        # todo: add docstring
        """
        domain = ast.literal_eval(self.mailing_domain)
        contacts = self.env['res.partner'].search(domain)
        self.syndicom_count = len(contacts)

    @api.onchange('syndicom_mail_sender')
    def _onchange_syndicom_mail_sender(self):
        sender = self.env['syndicom.mail.sender'].search([
            ('id', '=', self.syndicom_mail_sender.id)
        ], limit=1)
        if len(sender) > 0:
            self.email_from = sender.mail_from
            self.reply_to = sender.reply_to

    @api.depends('mailing_model_id', 'contact_list_ids',
                 'mailing_type', 'syndicom_mailing_domain_ids',
                 'syndicom_filter_ids', 'syndicom_mailing_topic_id')
    def _compute_mailing_domain(self):
        """
            We let mailing_domain be computed forst from the standard
            odoo method _compute_mailing_domain, then we check if we
            have syndicom_mailing_domain_ids, and add them to the deomain
        """
        for mailing in self:

            super(MailingMailing, self)._compute_mailing_domain()

            if mailing.syndicom_mailing_domain_ids:
                compiled_domain = mailing._get_combined_mailing_domain()

                mailing.mailing_domain = repr(expression.AND(
                    [compiled_domain, self.domain_eval(mailing.mailing_domain)]
                ))

    def _get_combined_mailing_domain(self):
        for mailing in self:

            compiled_domain = False

            for mailing_domain in mailing.syndicom_mailing_domain_ids:
                if compiled_domain:
                    compiled_domain = expression.OR(
                        [self.domain_eval(mailing_domain.domain), compiled_domain]
                    )
                else:
                    compiled_domain = self.domain_eval(mailing_domain.domain)

            for mailing_domain in mailing.syndicom_filter_ids:
                if compiled_domain:
                    compiled_domain = expression.AND(
                        [self.domain_eval(mailing_domain.domain), compiled_domain]
                    )
                else:
                    compiled_domain = self.domain_eval(mailing_domain.domain)
            return compiled_domain

        return False

    @api.model
    def domain_eval(self, domain):
        return ast.literal_eval(domain)
