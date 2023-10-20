# -*- coding: utf-8 -*-
{
    'name': "syndicom Kursverwaltung",

    'summary': """
        Verwaltung der Movendo Kurse als syndicom Dienstleistungen""",

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
    'depends': ['base','syndicom_contacts'],

    # always loaded
    'data': [
        'security/course_manager.xml',
        'security/ir.model.access.csv',
        'views/course.xml',
        'views/member_service.xml',
        'views/settings_institute.xml',
        'views/settings_speaker.xml',
        'views/settings_level.xml',
        'views/menu.xml',
    ],
    
}
