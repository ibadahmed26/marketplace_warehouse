# -*- coding: utf-8 -*-
{
    'name': "marketplace_warehouse",

    'summary': """
        Multi Warehousing in Odoo for Marketplace Sellers 
        """,

    'description': """
        This module is proposed to featuring the multi warehousing for seller.
        So, they can maintain their stocks to different warehouses.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','odoo_marketplace', 'sale','product', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sale_order.xml',
        'views/warehouse.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
