# -*- coding: utf-8 -*-
{
    'name': "External Sale Invoice",
    'author': "Erik Firmansyah",
    'category': 'Sale',
    'summary': """
        External Sale & Invoice
    """,
    'description': """
        Showing Sale and Invoice For External
    """,
    'license': 'LGPL-3',
    'version': '1.0.0',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/server_actions.xml',
        'views/res_partner_views.xml',
        'views/external_sale_invoice_views.xml',
        'views/invoice_request_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'external_sale_invoice/static/src/xml/external_sale_order_list.xml',
            'external_sale_invoice/static/src/xml/button_invoice.xml',
            'external_sale_invoice/static/src/js/external_sale_order_list.js',
            'external_sale_invoice/static/src/js/button_invoice.js',
        ],
    },
    'application': True,
}
