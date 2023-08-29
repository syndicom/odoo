# -*- coding: utf-8 -*-
import hashlib
import hmac
from odoo import fields, models, api, tools
from odoo.osv import expression
from odoo.tools import consteq
import ast
import werkzeug.urls
from werkzeug.urls import url_join


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

    syndicom_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="mailing_mailing_syndicom_res_partner_rel",
        column1="mailing_id",
        column2="res_partner_id",
        string="Weitere Kontakte")

    reminder_event_id = fields.Many2one(comodel_name='event.event', string='Reminder für', help='Wenn in diesem Feld ein Event ausgewählt wird, so wird sichergestellt, dass keine Kontakte, die sich bereits an besagtem Event An- oder Abgemeldet haben, den neuen Newsletter erhalten')
    announcement_event_id = fields.Many2one(comodel_name='event.event', string='Info für', help='Wenn in diesem Feld ein Event ausgewählt wird, so werden standartmässig alle Teilnehmer des entsprechenden Event als Empfänger ausgewählt.',readonly=True)
    event_announcement = fields.Char(string='Event Info Domain')

    @api.model
    def default_get(self, fields_list):
        vals = super(MailingMailing, self).default_get(fields_list)
        vals.update({
            'mailing_model_id': self.env.ref('base.model_res_partner').id
        })
        return vals

    @api.depends('mailing_model_id', 'contact_list_ids',
                 'mailing_type', 'syndicom_mailing_domain_ids',
                 'syndicom_filter_ids', 'syndicom_mailing_topic_id',
                 'syndicom_partner_ids','reminder_event_id')
    def _compute_recipient_count(self):
        """
        # todo: add docstring
        """
        if self.mailing_model_id.model == 'res.partner':
            domain = ast.literal_eval(self.mailing_domain)
            #domain = repr(expression.AND(
            #        [[['email','!=',False]], domain]
            #    ))
            contacts = self.env['res.partner'].search(domain)
            self.syndicom_count = len(contacts)
        else:
            self.syndicom_count = 99999

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
                 'syndicom_filter_ids', 'syndicom_mailing_topic_id',
                 'syndicom_partner_ids','reminder_event_id',
                 'announcement_event_id')
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
            elif mailing.syndicom_partner_ids:
                compiled_domain = mailing._get_combined_mailing_domain()

                mailing.mailing_domain = repr(expression.AND(
                    [compiled_domain, self.domain_eval(mailing.mailing_domain)]
                ))
            elif mailing.announcement_event_id.id:
                compiled_domain = mailing._get_combined_mailing_domain()

                mailing.mailing_domain = repr(expression.AND(
                    [compiled_domain, self.domain_eval(mailing.mailing_domain)]
                ))


    def _get_combined_mailing_domain(self):
        for mailing in self:

            compiled_domain = False

            # "Verteiler"
            for mailing_domain in mailing.syndicom_mailing_domain_ids:
                if compiled_domain:
                    compiled_domain = expression.OR(
                        [self.domain_eval(mailing_domain.domain), compiled_domain]
                    )
                else:
                    compiled_domain = self.domain_eval(mailing_domain.domain)
            
            # "Kontakte"
            partner_ids = []
            for mailing_partner in mailing.syndicom_partner_ids:
                partner_ids.append(mailing_partner._origin.id)
            
            if len(partner_ids) > 0:
                compiled_domain = expression.OR(
                    [[['id','in',partner_ids]], compiled_domain]
                )
            #else:
            #    compiled_domain = self.domain_eval(mailing_domain.domain)  

            # "Event-Info"
            # Check if this Mail is supposed to be a Annoucement Mail for a Event
            # Then Add the needed Logic
            if mailing.announcement_event_id.id != False:
                if compiled_domain:
                    compiled_domain = expression.OR(
                        [[['registration_ids.booked_event_id', 'in', [mailing.announcement_event_id.id] ]], compiled_domain]
                    )
                else:
                    compiled_domain = [['registration_ids.booked_event_id', 'in', [mailing.announcement_event_id.id] ]]
               
            # "Filter"
            for mailing_domain in mailing.syndicom_filter_ids:
                if compiled_domain:
                    compiled_domain = expression.AND(
                        [self.domain_eval(mailing_domain.domain), compiled_domain]
                    )
                else:
                    compiled_domain = self.domain_eval(mailing_domain.domain)
            
            # "Event-Reminder"
            # If the Mass Mailing is supposed to be a reminder Message for a Event
            # Add the needed Logic to the Domain Field
            if mailing.reminder_event_id.id != False:
                if compiled_domain:
                    compiled_domain = expression.AND(
                        [[    '|',  ['event_ids', '=', False],['event_ids','not in',[mailing.reminder_event_id.id]]        ], compiled_domain]
                    )
                else:
                    compiled_domain = self.domain_eval(mailing_domain.domain)
            
            return compiled_domain

        return False

    @api.model
    def domain_eval(self, domain):
        return ast.literal_eval(domain)

    def clear_partner_ids(self):
        for mailing in self:
            mailing.syndicom_partner_ids = False

    def custom_unsubscribe_token(self, res_id, email, mailing):
        """
        Custom Method to access from API
        """
        secret = self.env["ir.config_parameter"].sudo().get_param("database.secret")
        token = (self.env.cr.dbname, int(mailing), int(res_id), tools.ustr(email))
        return hmac.new(secret.encode('utf-8'), repr(token).encode('utf-8'), hashlib.sha512).hexdigest()

    @api.model
    def _get_unsubscribe_url(self, email_to, res_id):

        url = werkzeug.urls.url_join(
            'https://my.syndicom.ch/',
                'mail/mailing/%(mailing_id)s/unsubscribe?%(params)s' % {
                'mailing_id': self.id,
                'params': werkzeug.urls.url_encode({
                    'res_id': res_id,
                    'email': email_to,
                    'token': self._unsubscribe_token(res_id, email_to),
                }),
            }
        )
        
        return url

    @api.model
    def _get_view_url(self, email_to, res_id):
        
        url = werkzeug.urls.url_join(
            'https://my.syndicom.ch/',
            'mailing/%(mailing_id)s/view?%(params)s' % {
                'mailing_id': self.id,
                'params': werkzeug.urls.url_encode({
                    'res_id': res_id,
                    'email': email_to,
                    'token': self._unsubscribe_token(res_id, email_to),
                }),
            }
        )

        return url

 