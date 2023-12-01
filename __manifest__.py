# -*- coding: utf-8 -*-
{
    'name': "gse_field_service",

    'summary': """
        Customizations pour Goshop Energy""",

    'description': """
    """,

    'author': "Benjamin Kisenge",
    'website': "https://dev--glowing-faun-e9789d.netlify.app/",

    'category': 'Customizations',
    'version': '0.1.8.7',
    'license': 'LGPL-3',

    'depends': [  
        'base',
        'sale',
        'sale_management',
        'project',
        'sales_team',
        'account_payment',  # -> account, payment, portal
        'utm',
        'delivery'
    ],

    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/project_task_views.xml',
        'reports/project_report_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            
        ]
    },
}
