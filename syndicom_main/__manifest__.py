# -*- coding: utf-8 -*-
{
    'name': "syndicom_main",

    'summary': """
        odoo Module for syndicom - Covers different modifications on other Apps""",

    'description': """
        
    """,

    'author': "syndicom, Pascal Arnold",
    'website': "https://syndicom.ch",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1.0.2',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': ['base','syndicom_member_data_history','product','account','membership'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/work_employee.xml',
        'views/work_locations.xml',
        'views/menu.xml',
    ],
    
}
