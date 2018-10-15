#!/usr/bin/env python3

import os
import shutil

from . import consts
from . import tools

c = consts.Consts()
t = tools.Tools()


class Module:

    def __init__(self):
        self.config_text = t.get_config_file()
        self.lang = t.get_language_file()

    def create(self, arg1=None, arg2=None):
        lang = self.lang
        if not arg1 or arg1 == 'module':
            self.create_module()
        else:
            if arg2:
                module_name = arg2
                if not t.check_module_exist(module_name):
                    print(self.lang['module_not_found'].format(module_name))
                    return False
            else:
                print(lang['module_no_name'])

                module_name = input(lang['module_name'])
                if not t.check_module_exist(module_name):
                    print(self.lang['module_not_found'].format(module_name))
                    return False

            if arg1 == 'model':
                self.create_model(module_name)
            elif arg1 == 'model_inherited':
                self.create_model_inherited(module_name)
            elif arg1 == 'wizard':
                self.create_wizard(module_name)
            else:
                print(lang['create_bad_argument'].format(arg1))

    def create_module(self):
        lang = self.lang
        if not t.yes_no(lang['create_are_you_sure'] + ' "' + self.config_text['addons_path'] + '"'):
            print(lang['module_canceld'])
            return False

        content = {}
        content['modules'] = {}

        dir_name_done = None
        dir_name = None
        if not 'addons_path' in self.config_text:
            print(lang['module_no_addon_path'])
            return False

        addons_path = self.config_text['addons_path']

        content_module = {}

        name = None
        while not name:
            name = input(lang['module_name'])
            if not name:
                print(lang['module_no_name'])

        content_module['name'] = name

        while not dir_name_done:
            dir_name = input(lang['module_dir_name'])
            if dir_name:
                module_path = addons_path + ('/' if addons_path[-1] != '/' else '') + dir_name + '/'
                if not os.path.isdir(module_path):
                    content_module['dir_name'] = dir_name
                    content_module['path'] = module_path
                    dir_name_done = True
                else:
                    print(lang['module_already_exists'].format(dir_name))
            else:
                print(lang['module_specify_dir_name'])

        prefix_class = None
        while not prefix_class:
            prefix_class = input(lang['module_prefix_class'])
            if not prefix_class:
                print(lang['module_specify_prefix_class'])
        content_module['prefix_class'] = prefix_class

        prefix_name = None
        while not prefix_name:
            prefix_name = input(lang['module_prefix_name'])
            if not prefix_name:
                print(lang['module_specify_prefix_name'])
        content_module['prefix_name'] = prefix_name


        summary = input(lang['module_summary'])
        content_module['summary'] = summary

        description = input(lang['module_description'])
        content_module['description'] = description

        version = input(lang['module_version'])
        content_module['version'] = version

        category = input(lang['module_category'])
        content_module['category'] = category

        author = input(lang['module_author'])
        content_module['author'] = author

        email = input(lang['module_email'])
        content_module['email'] = email

        website = input(lang['module_website'])
        content_module['website'] = website

        depends = input(lang['module_depends'])
        content_module['depends'] = depends or '["base"]'

        content['modules'][dir_name] = content_module
        t.update_config_file(c.full_path_config, content)

        shutil.copytree(c.cur_dir + '/resources/', module_path)

        module_elements = os.listdir(module_path)

        for element in module_elements: # Check chaque éléments du dossier
            if os.path.isdir(module_path + element): # Si dossier
                for element2 in os.listdir(module_path + element): # Check chaque éléments du sous-dossier
                    self.make_element('{}{}/{}'.format(module_path, element, element2), content['modules'][dir_name])
            else: # Si fichier
                self.make_element('{}{}'.format(module_path, element), content['modules'][dir_name])

    def create_model(self, module_name):
        lang = self.lang
        content = {}

        addons_path = self.config_text['addons_path']
        module_path = addons_path + ('/' if addons_path[-1] != '/' else '') + module_name + '/'

        model_name = input(lang['model_name'])
        content['model_name'] = model_name

        content['model_prefix_view'] = content['model_name'].replace('.', '_')

        if os.path.exists('{}models/{}.py'.format(module_path, content['model_prefix_view'])):
            print(lang['model_already_exist'].format(content['model_prefix_view']))
            return False

        model_class = input(lang['model_class'])
        content['model_class'] = model_class

        model_name_view = input(lang['model_name_view'])
        content['model_name_view'] = model_name_view

        model_description = input(lang['model_description'])
        content['model_description'] = model_description

        content = t.merge_two_dicts(content, t.get_module_params(module_name))

        shutil.copyfile('{}/resources2/model.py'.format(c.cur_dir), '{}models/{}.py'.format(module_path, content['model_prefix_view']))
        shutil.copyfile('{}/resources2/view.xml'.format(c.cur_dir), '{}models/views/{}.xml'.format(module_path, content['model_prefix_view']))

        self.make_element('{}models/{}.py'.format(module_path, content['model_prefix_view']), content)
        self.make_element('{}models/views/{}.xml'.format(module_path, content['model_prefix_view']), content)

        t.insert_into_file('{}models/__init__.py'.format(module_path), 'from . import {}'.format(content['model_prefix_view']))
        t.insert_into_file('{}__manifest__.py'.format(module_path), "\t\t'models/views/{}.xml',".format(content['model_prefix_view']), '# _models_views')
        t.insert_into_file('{}security/ir.model.access.csv'.format(module_path), 'access_{}_{}_guest,access.{}.{}.guest,model_{}_{},group_{}_guest,1,0,0,0'.format(content['dir_name'], content['model_prefix_view'], content['prefix_name'], content['model_name'], content['dir_name'], content['model_prefix_view'], content['dir_name']))
        t.insert_into_file('{}security/ir.model.access.csv'.format(module_path), 'access_{}_{}_admin,access.{}.{}.admin,model_{}_{},group_{}_admin,1,1,1,1'.format(content['dir_name'], content['model_prefix_view'], content['prefix_name'], content['model_name'], content['dir_name'], content['model_prefix_view'], content['dir_name']))

    def create_model_inherited(self, module_name):
        lang = self.lang
        content = {}

        addons_path = self.config_text['addons_path']
        module_path = addons_path + ('/' if addons_path[-1] != '/' else '') + module_name + '/'

        model_inherited_name = input(lang['model_inherited_name'])
        content['model_inherited_name'] = model_inherited_name

        content['model_inherited_prefix_view'] = content['model_inherited_name'].replace('.', '_')

        if os.path.exists('{}models/{}.py'.format(module_path, content['model_inherited_prefix_view'])):
            print(lang['model_inherited_already_exist'].format(content['model_inherited_prefix_view']))
            return False

        model_inherited_class = input(lang['model_inherited_class'])
        content['model_inherited_class'] = model_inherited_class

        print(lang['model_inherited_info_view'])

        model_inherited_view_search = input(lang['model_inherited_view_search'])
        content['model_inherited_view_search'] = model_inherited_view_search

        model_inherited_view_tree = input(lang['model_inherited_view_tree'])
        content['model_inherited_view_tree'] = model_inherited_view_tree

        model_inherited_view_form = input(lang['model_inherited_view_form'])
        content['model_inherited_view_form'] = model_inherited_view_form

        content = t.merge_two_dicts(content, t.get_module_params(module_name))

        shutil.copyfile('{}/resources2/model_inherited.py'.format(c.cur_dir), '{}models/{}.py'.format(module_path, content['model_inherited_prefix_view']))

        view_content = '<odoo>\n\t<data>\n'

        if content['model_inherited_view_search']:
            with open('{}/resources2/inherited_view_search.xml'.format(c.cur_dir), 'r') as file:
                view_content += file.read() + '\n'

        if content['model_inherited_view_tree']:
            with open('{}/resources2/inherited_view_tree.xml'.format(c.cur_dir), 'r') as file:
                view_content += file.read() + '\n'

        if content['model_inherited_view_form']:
            with open('{}/resources2/inherited_view_form.xml'.format(c.cur_dir), 'r') as file:
                view_content += file.read() + '\n'

        view_content += '\t</data>\n</odoo>\n'

        with open('{}models/views/{}.xml'.format(module_path, content['model_inherited_prefix_view']), 'w') as file:
            file.write(view_content)

        self.make_element('{}models/{}.py'.format(module_path, content['model_inherited_prefix_view']), content)
        self.make_element('{}models/views/{}.xml'.format(module_path, content['model_inherited_prefix_view']), content)

        t.insert_into_file('{}models/__init__.py'.format(module_path), 'from . import {}'.format(content['model_inherited_prefix_view']))
        t.insert_into_file('{}__manifest__.py'.format(module_path), "\t\t'models/views/{}.xml',".format(content['model_inherited_prefix_view']), '# _models_views')
        t.insert_into_file('{}security/ir.model.access.csv'.format(module_path), 'access_{}_guest,access.{}.guest,model_{},group_{}_guest,1,0,0,0'.format(content['model_inherited_prefix_view'], content['model_inherited_name'], content['model_inherited_prefix_view'], content['dir_name']))
        t.insert_into_file('{}security/ir.model.access.csv'.format(module_path), 'access_{}_admin,access.{}.admin,model_{},group_{}_admin,1,1,1,1'.format(content['model_inherited_prefix_view'], content['model_inherited_name'], content['model_inherited_prefix_view'], content['dir_name']))

    def create_wizard(self, module_name):
        print('Wizard not available yet.')
        pass

    def make_element(self, path_element_init, content):
        if os.path.isfile(path_element_init):
            self.make_file(path_element_init, content)  # Remplacement variables
        path_element_new = path_element_init
        for key, value in c.custom_variables_list.items():
            try: path_element_new = path_element_new.replace(key, content[value])
            except: pass
        os.rename(path_element_init, path_element_new)

    def make_file(self, file_path, content):
        with open(file_path, 'r') as file:
            filedata = file.read()

        for key, value in c.custom_variables_list.items():
            try: filedata = filedata.replace(key, content[value])
            except: pass

        with open(file_path, 'w') as file:
            file.write(filedata)