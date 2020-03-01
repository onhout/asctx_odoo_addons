# -*- coding: utf-8 -*-
{
    'name': "RD/TD",

    'summary': """
        This is the ASC Therapeutics RD/TD Database application
    """,

    'description': """
        To store ASC Therapeutics RD/TD information
    """,

    'author': "ASC Therapeutics",
    'website': "https://www.asctherapeutics.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ASC Therapeutics',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/plasmids.xml',
        'views/viruses.xml',
        'views/analysis_runs.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'application': True
}