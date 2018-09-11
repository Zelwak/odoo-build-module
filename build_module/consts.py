#!/usr/bin/env python3
from pathlib import Path
import os

class Consts:
    home = str(Path.home())
    path_config = home + "/.odoo-build-module/"
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = "config.yml"
    full_path_config = path_config + config_file
    language = 'en'
    available_update_args = ['language', 'addons_path']
    custom_variables_list = {'@@name@@': 'name',
                             '@@dir_name@@': 'dir_name',
                             '@@prefix_name@@': 'prefix_name',
                             '@@prefix_class@@': 'prefix_class',
                             '@@version@@': 'version',
                             '@@category@@': 'category',
                             '@@summary@@': 'summary',
                             '@@description@@': 'description',
                             '@@author@@': 'author',
                             '@@email@@': 'email',
                             '@@website@@': 'website',
                             '@@depends@@': 'depends',
                             '@@model_name@@': 'model_name',
                             '@@model_class@@': 'model_class',
                             '@@model_description@@': 'model_description',
                             '@@model_prefix_view@@': 'model_prefix_view',
                             '@@model_name_view@@': 'model_name_view',
                             '@@model_inherited_class@@': 'model_inherited_class',
                             '@@model_inherited_name@@': 'model_inherited_name',
                             '@@model_inherited_prefix_view@@': 'model_inherited_prefix_view',
                             '@@model_inherited_view_search@@': 'model_inherited_view_search',
                             '@@model_inherited_view_tree@@': 'model_inherited_view_tree',
                             '@@model_inherited_view_form@@': 'model_inherited_view_form'}
