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
    'depends': ['base','syndicom_member_data_history','product','account','membership','helpdesk','syndicom_member_administration','hr_expense','announcement','event', 'website_event','website_event_social'],

    # always loaded
    'data': [
        'security/binding_officer.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_ticket.xml',
        'views/res_partner.xml',
        'views/hr_leave_type.xml',
        'views/suisse_streets.xml',
        'views/binding_operators.xml',
        'views/binding_conversations.xml',
        'views/retirement_consulting.xml',
        'views/work_employee.xml',
        'views/work_locations.xml',
        'views/mysyndicom_users.xml',
        'views/internal_category.xml',
        'views/internal_informations.xml',
        'views/menu.xml',
    ],
    
}
