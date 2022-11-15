# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syndicom Mass Mailing Themes',
    'summary': 'syndicom Design gorgeous mails',
    'description': """
Design gorgeous mails
    """,
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',
    'sequence': 10,
    'website': 'https://www.odoo.com/app/mailing',
    'category': 'Marketing/Email Marketing',
    'depends': [
        'mass_mailing',
    ],
    'data': [
        'views/mass_mailing_themes_templates.xml'
    ],
    'installable': True,
    'auto_install': True,
}
