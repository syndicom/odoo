# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    syn_declaration_cla_imputed = fields.Many2one(comodel_name='res.partner.relation.type',string='Beziehung für GAV Unterstellung',
        config_parameter='syndicom_vollzug.cla_imputed',
        default="")
    
    
