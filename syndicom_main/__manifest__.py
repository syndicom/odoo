##############################################################################
# Copyright (c) 2022 brain-tec AG (https://bt-group.com)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    'name': 'Syndicom member administration',
    'author': 'brain-tec AG',
    'website': 'https://bt-group.com',
    'category': 'Sales/CRM',
    'version': '15.0.1.0.7',
    'license': 'AGPL-3',
    'summary': 'Extensions for the contacts requested by Syndicom',
    'depends': [
        'base',
        'contacts',
        'membership',
        'helpdesk_timesheet',
        'partner_firstname',
        'sale_subscription',
        'syndicom_contacts',
        'syndicom_gender',
        'bt_advanced_sale_subscription',
        'bt_advanced_sale_subscription_termination',
        'syndicom_partner_multi_relation',
        'helpdesk_plausibility_check',
        'bt_invoice_tier_payer',
        'bt_subscription_payment_method'
    ],
    'data': [
        'security/membership_administration_security.xml',
        'security/ir.model.access.csv',
        'data/helpdesk_team.xml',
        'views/helpdesk_stage.xml',
        'views/helpdesk_team.xml',
        'views/helpdesk_ticket.xml',
        'views/syndicom_member_search.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'views/res_partner.xml',
        'views/res_partner_bank.xml',
        'views/menu_items.xml',
        'wizards/start_process_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'post_load': 'post_load',
    'uninstall_hook': 'uninstall_hook',
}
