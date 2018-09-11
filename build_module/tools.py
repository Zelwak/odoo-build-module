#!/usr/bin/env python3
import yaml
import os

from . import consts

c = consts.Consts()

class Tools:

    def __init__(self):
        self.config_text = self.get_config_file()
        self.lang = self.get_language_file()

    def get_config_file(self):
        if os.path.exists(c.full_path_config):
            return yaml.load(open(c.full_path_config))
        return {}

    def set_config_file(self, file_path, content):
        file = open(file_path, "w")
        yaml.dump(content, file, default_flow_style=False)
        file.close()
        return True

    def update_config_file(self, file, content):
        if os.path.exists(file):
            with open(file, 'r') as f:
                yamlfile = yaml.load(f)
            if content.get('modules') and yamlfile.get('modules'):
                yamlfile['modules'].update(content['modules'])
            else:
                yamlfile.update(content)
            with open(file, 'w') as f:
                yaml.dump(yamlfile, f, default_flow_style=False)
            return True
        return False


    def get_language_file(self):
        config_text = self.config_text
        global language
        if config_text and 'language' in config_text:
            language = config_text['language']

        try:
            return yaml.load(open(c.cur_dir+"/languages/"+language+".yml"))
        except:
            return yaml.load(open(c.cur_dir + "/languages/en.yml"))


    def get_language_list(self):
        language_list = os.listdir(c.cur_dir+"/languages/")
        language_list = [file.replace('.yml', '') for file in language_list]
        return language_list


    def yes_no(self, question):
        action = ''
        while action.lower() not in ['yes', 'y', 'no', 'n']:
            action = input(question + ' ' + self.lang['tools_yes_no'] + '\n> ')
        if action.lower() in ['yes', 'y']:
            return True
        else:
            return False

    def check_setup(self):
        if not os.path.isdir(c.path_config) or not os.path.exists(c.full_path_config):
            return False
        return True

    def check_module_exist(self, module_name):
        module_list = self.get_modules_list()
        if module_list:
            if module_name in module_list:
                return True
            else:
                return False
        else:
            return False

    def get_modules_list(self):
        if self.config_text.get('modules'):
            module_list = []
            for key in self.config_text.get('modules').keys():
                module_list.append(key)
            return module_list
        else:
            return False

    def get_module_params(self, module_name):
        lang = self.lang
        if self.config_text.get('modules'):
            modules = self.config_text.get('modules')
            if modules.get(module_name):
                return modules[module_name]
            else:
                print(lang['module_not_found'].format(module_name))
                return False

    def merge_two_dicts(self, x, y):
        if isinstance(x, dict) and isinstance(y,dict):
            z = x.copy()
            z.update(y)
            return z
        else:
            return {}

    def insert_into_file(self, file_path, content, delimiter='_append'):
        if delimiter == '_append':
            with open(file_path, 'a') as file:
                file = file.write(content + '\n')
        else:
            with open(file_path, 'r') as file:
                filelines = file.readlines()

            filedata = ''
            for line in filelines:
                if delimiter in line:
                    filedata += line + content + '\n'
                else:
                    filedata += line

            with open(file_path, 'w') as file:
                file.write(filedata)

    def read_help(self):
        file_path = c.cur_dir + '/resources2/help'
        with open(file_path, 'r') as file:
            print(file.read())