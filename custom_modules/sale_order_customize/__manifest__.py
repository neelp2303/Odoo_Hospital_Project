# -*- coding: utf-8 -*-
{
    "name": "sale_order_customize",
    "summary": "Practical Assignment",
    "description": """
    Practical
    """,
    "author": "Neel Patel",
    "website": "https://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "0.1",
    "sequence": "0",
    # any module necessary for this one to work correctly
    "depends": ["base", "sale"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "wizards/sale_order_line_wizard_views.xml",
    ],
    # only loaded in demonstration mode
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
