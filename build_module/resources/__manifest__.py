# -*- coding: utf-8 -*-
{
    'name': '@@name@@',
    'version': '@@version@@',
    'category': '@@category@@',
    'summary': "@@summary@@",
    'description': "@@description@@",
    'author': '@@author@@ (@@email@@)',
    'website': '@@website@@',
    'depends': @@depends@@,
    'data': [
        'security/@@dir_name@@_security.xml',

        'datas/datas.xml',

        # _models_views (do not change or remove)

        # _wizards_views (do not change or remove)

        # _controllers_templates (do not change or remove)

        'security/ir.model.access.csv',
        '@@dir_name@@_menu.xml',
    ],
    'installable': True,
}