#!/usr/bin/env python3
from setuptools import setup

setup(
    name = "odoo-build-module",
    packages = ['build_module'],

    version = "1.0.0",

    description = "To help you build your Odoo modules.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    author = "Flavien CHENE (Zelwak)",
    author_email = "me@flavienchene.fr",

    url = "https://github.com/Zelwak/build-odoo-module",

    license = "Creative Commons BY-NC-SA",

    keywords = "odoo module create openerp help build model controllers wizards",
    scripts = ['bin/build_module'],
    install_requires=[],
    classifiers = [
        'Framework :: Odoo',
        'Natural Language :: English',
        'Natural Language :: French',
        'Programming Language :: Python',
    ],

    include_package_data=True,
)
