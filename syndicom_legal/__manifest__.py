# -*- coding: utf-8 -*-
{
    'name': "syndicom Rechtsdienstverwaltung",

    'summary': """
        Rechtsfall verwaltung für syndicom""",

    'description': """
        Rechtsfall verwaltung für syndicom
    """,

    'author': "syndicom, Pascal Arnold",
    'website': "https://syndicom.ch",
    'category': 'Uncategorized',
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',
    'depends': ['base','contacts','membership','helpdesk','helpdesk_timesheet',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/server_action.xml',
        'views/inherited_helpdesk.helpdesk_team_view_form.xml',
        'views/inherited_helpdesk.helpdesk_ticket_view_form.xml',
        'views/syndicom_ticket_cost_type.xml',
        'views/syndicom_ticket_consulting_type.xml',
        'views/menu.xml',
    ],
 
}
