# -*- coding: utf-8 -*-
{
    'name': "syndicom_events",

    'summary': """
       Erweiterungen am Eventtool für syndicom""",

    'description': """
       Erweiterungen am Eventtool für syndicom
    """,

    'author': "Pascal Arnold, syndicom",
    'website': "https://syndicom.ch",
    'category': 'Uncategorized',
    'version': '15.0.1.0.2',
    'license': 'LGPL-3',
    'depends': ['website_event'],
    'data': [
        'security/ir.model.access.csv',
        'views/inherited_event_event_view.xml',
    ],
   
    
}
