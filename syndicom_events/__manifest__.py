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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_event'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
       
        'views/inherited_event_event_view.xml',
    ],
   
    
}
