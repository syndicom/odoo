# -*- coding: utf-8 -*-
{
    'name': "Syndicom Petitionen",

    'summary': """
        Petitionsverwaltung für odoo""",

    'description': """
        Petitionsverwaltung für odoo
    """,

    'author': "syndicom, Pascal Arnold",
    'website': "https://syndicom.ch",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_res_partner.xml',
        'views/syndicom_petition.xml',
        'views/syndicom_petition_participation.xml',
        'views/menu.xml',
    ],

}
