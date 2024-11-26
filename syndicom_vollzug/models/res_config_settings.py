# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    syn_declaration_association_imputed = fields.Many2one(comodel_name='res.partner.relation.type',string='Beziehung für Verbandsmitgliedschaft',
        config_parameter='syndicom_vollzug.association_imputed',
        default="", 
        )
    syn_declaration_ev_imputed = fields.Many2one(comodel_name='res.partner',string='Partner der als Einzelvertragsfirma gilt',
        config_parameter='syndicom_vollzug.ev_imputed',
        default="", 
        )

    syn_partner_cc = fields.Many2one(comodel_name='res.partner',string='Partner CC Berechnung',
        config_parameter='syndicom_vollzug.cla_logic_cc',
        default=55247)

    syn_company_cc = fields.Many2one(comodel_name='res.company',string='Company CC',
        config_parameter='syndicom_vollzug.syn_company_cc',
        default=0)

    syn_partner_nz = fields.Many2one(comodel_name='res.partner',string='Partner NZ Berechnung',
        config_parameter='syndicom_vollzug.cla_logic_nz',
        default=55250)

    syn_company_nz = fields.Many2one(comodel_name='res.company',string='Company nz',
        config_parameter='syndicom_vollzug.syn_company_nz',
        default=0)
    # CC Products
    syn_prod_cc_tz = fields.Many2one(comodel_name='product.product',string='Produkt TZ CC',
        config_parameter='syndicom_vollzug.syn_prod_cc_tz',
        default=0)
        
    syn_prod_cc_vz = fields.Many2one(comodel_name='product.product',string='Produkt VZ CC',
        config_parameter='syndicom_vollzug.syn_prod_cc_vz',
        default=0)

    syn_prod_cc_ag = fields.Many2one(comodel_name='product.product',string='Produkt AG CC',
        config_parameter='syndicom_vollzug.syn_prod_cc_ag',
        default=0)

    syn_prod_cc_discount = fields.Many2one(comodel_name='product.product',string='Produkt Rabatt CC',
        config_parameter='syndicom_vollzug.syn_prod_cc_discount',
        default=0)

    syn_account_cc_ertrag_ver = fields.Many2one(comodel_name='account.account',string="Ertragskonto CC Verbandsfirmen",default=0,     config_parameter='syndicom_vollzug.syn_account_cc_ertrag_ver')
    syn_account_cc_ertrag_ave = fields.Many2one(comodel_name='account.account',string="Ertragskonto CC AVE Firmen",default=0,         config_parameter='syndicom_vollzug.syn_account_cc_ertrag_ave')
    syn_account_cc_ertrag_org = fields.Many2one(comodel_name='account.account',string="Ertragskonto CC AN Organisiert",default=0,     config_parameter='syndicom_vollzug.syn_account_cc_ertrag_org')
    syn_account_cc_ertrag_n_org = fields.Many2one(comodel_name='account.account',string="Ertragskonto CC AN nicht-Organ.",default=0,  config_parameter='syndicom_vollzug.syn_account_cc_ertrag_n_org')
    syn_account_cc_deb_ver = fields.Many2one(comodel_name='account.account',string="Debitorenkonto CC Verbandsfirmen",default=0,      config_parameter='syndicom_vollzug.syn_account_cc_deb_ver')
    syn_account_cc_deb_ave = fields.Many2one(comodel_name='account.account',string="Debitorenkonto CC AVE Firmen",default=0,          config_parameter='syndicom_vollzug.syn_account_cc_deb_ave')
    syn_account_cc_deb_org = fields.Many2one(comodel_name='account.account',string="Debitorenkonto CC AN Organisiert",default=0,      config_parameter='syndicom_vollzug.syn_account_cc_deb_org')
    syn_account_cc_deb_n_org = fields.Many2one(comodel_name='account.account',string="Debitorenkonto CC AN nicht-Organ.",default=0,   config_parameter='syndicom_vollzug.syn_account_cc_deb_n_org')
        
    # NZ Products
    syn_prod_nz_tz = fields.Many2one(comodel_name='product.product',string='Produkt TZ nz',
        config_parameter='syndicom_vollzug.syn_prod_nz_tz',
        default=0)
        
    syn_prod_nz_vz = fields.Many2one(comodel_name='product.product',string='Produkt VZ nz',
        config_parameter='syndicom_vollzug.syn_prod_nz_vz',
        default=0)

    syn_prod_nz_ag = fields.Many2one(comodel_name='product.product',string='Produkt AG nz',
        config_parameter='syndicom_vollzug.syn_prod_nz_ag',
        default=0)

    syn_prod_nz_discount = fields.Many2one(comodel_name='product.product',string='Produkt Rabatt nz',
        config_parameter='syndicom_vollzug.syn_prod_nz_discount',
        default=0)

    syn_account_nz_ertrag_ver = fields.Many2one(comodel_name='account.account',string="Ertragskonto nz Verbandsfirmen",default=0,     config_parameter='syndicom_vollzug.syn_account_nz_ertrag_ver')
    syn_account_nz_ertrag_ave = fields.Many2one(comodel_name='account.account',string="Ertragskonto NZ AVE Firmen",default=0,         config_parameter='syndicom_vollzug.syn_account_nz_ertrag_ave')
    syn_account_nz_ertrag_org = fields.Many2one(comodel_name='account.account',string="Ertragskonto NZ AN Organisiert",default=0,     config_parameter='syndicom_vollzug.syn_account_nz_ertrag_org')
    syn_account_nz_ertrag_n_org = fields.Many2one(comodel_name='account.account',string="Ertragskonto NZ AN nicht-Organ.",default=0,  config_parameter='syndicom_vollzug.syn_account_nz_ertrag_n_org')
    syn_account_nz_deb_ver = fields.Many2one(comodel_name='account.account',string="Debitorenkonto NZ Verbandsfirmen",default=0,      config_parameter='syndicom_vollzug.syn_account_nz_deb_ver')
    syn_account_nz_deb_ave = fields.Many2one(comodel_name='account.account',string="Debitorenkonto NZ AVE Firmen",default=0,          config_parameter='syndicom_vollzug.syn_account_nz_deb_ave')
    syn_account_nz_deb_org = fields.Many2one(comodel_name='account.account',string="Debitorenkonto NZ AN Organisiert",default=0,      config_parameter='syndicom_vollzug.syn_account_nz_deb_org')
    syn_account_nz_deb_n_org = fields.Many2one(comodel_name='account.account',string="Debitorenkonto NZ AN nicht-Organ.",default=0,   config_parameter='syndicom_vollzug.syn_account_nz_deb_n_org')