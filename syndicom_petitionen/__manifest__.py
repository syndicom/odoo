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
    'depends': ['base','membership','crm'],
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_res_partner.xml',
        'views/inherited_crm_lead.xml',
        'views/syndicom_petition.xml',
        'views/syndicom_petition_participation.xml',
        'views/menu.xml',
        'views/filter_partners_wizard_views.xml',
    ],

}
