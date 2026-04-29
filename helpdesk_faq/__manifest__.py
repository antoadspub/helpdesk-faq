# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk FAQ',
    'version': '19.0.1.0.0',
    'category': 'Helpdesk',
    'summary': 'Manage Frequently Asked Questions with categories and tags',
    'description': """
        Helpdesk FAQ Module for Odoo 19 CE
        =================================
        - Manage FAQ questions grouped by categories
        - Rich HTML answers
        - Tag-based organization
        - Draft / Published workflow
        - Role-based access (FAQ Manager / FAQ User)
        - File attachments with 2 MB size limit
    """,
    'author': 'Anto Vincent',
    'depends': ['base', 'website'],
    'data': [
        'security/faq_security.xml',
        'security/ir.model.access.csv',
        'views/faq_category_views.xml',
        'views/faq_tag_views.xml',
        'views/faq_question_views.xml',
        'views/menu_views.xml',
        'views/website_faq_templates.xml',
        'data/faq_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
