# -*- coding: utf-8 -*-
{
    'name': "asc_therapeutics_customize",

    'summary': """
        Customize ASC Therapeutics Odoo""",

    'description': """
        Customzation for the ASC Therapeutics Odoo modules, extending the use for all ASC Therapeutics models
    """,

    'author': "ASC Therapeutics",
    'website': "http://www.asctherapeutics.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customize',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'calendar'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}