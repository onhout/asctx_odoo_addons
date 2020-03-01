# -*- coding: utf-8 -*-
{
    'name': "tawkto_chat",

    'summary': """
        Tawk.To chat widget""",

    'description': """
        Just a chat widget that scripted online.
    """,

    'author': "Peter Liu",
    'website': "https://www.asctherapeutics.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Chat Bot',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}