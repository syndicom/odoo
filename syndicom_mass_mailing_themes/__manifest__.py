# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syndicom Mass Mailing Themes',
    'summary': 'syndicom Design gorgeous mails',
    'description': """
Design gorgeous mails
    """,
    'version': '15.0.1.0.2',
    'author': 'syndicom, Pascal Arnold',
    'license': 'LGPL-3',
    'website': 'https://syndicom.ch',
    'category': 'Marketing/Email Marketing',
    'depends': [

        'mass_mailing',
        'syndicom_mailing_topic',
        'base_user_role',
    ],
    'data': [
        'security/ir.model.access.csv', 
        'views/snippets/syndicom_buttons.xml',
        'views/snippets_themes.xml',
        'views/mass_mailing_themes_templates.xml',
        'views/inherited_mailing_mailing_form.xml',
        'views/inherited_res_users_role.xml',
        'views/syndicom_mailing_domain_view.xml',
        'views/sender.xml',
        'views/filter.xml',
        'views/menu.xml',
    ],
    
    'installable': True,
    'auto_install': True,
    'application': True,
}
