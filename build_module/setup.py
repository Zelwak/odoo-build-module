#!/usr/bin/env python3
import os
import shutil
import yaml

from . import consts
from . import tools

c = consts.Consts()
t = tools.Tools()

class Setup:

    def __init__(self):
        self.lang = t.get_language_file()
        self.language_list = t.get_language_list()
        self.config_text = t.get_config_file()

    def setup(self):
        print(c.path_config)
        if os.path.isdir(c.path_config):
            shutil.rmtree(c.path_config)
        os.makedirs(c.path_config)

        self.update(True)


    def update(self, setup=False, arg=None):
        new_config_text = {}
        if not arg or arg == 'language':
            self.config_text['language'] = self.config_text['language'] if 'language' in self.config_text else ''
            new_config_text['language'] = ''
            if not setup:
                print(self.lang['update_cur_language']+self.config_text['language'])
            while new_config_text['language'] not in self.language_list:
                new_config_text['language'] = input(self.lang['update_get_language'] + str(self.language_list) + '\n> ')

        if not arg or arg == 'addons_path':
            self.config_text['addons_path'] = self.config_text['addons_path'] if 'addons_path' in self.config_text else ''
            new_config_text['addons_path'] = ''
            if not setup:
                print(self.lang['update_cur_addons_path'] + self.config_text['addons_path'])
            while not os.path.isdir(new_config_text['addons_path']):
                new_config_text['addons_path'] = input(self.lang['update_get_addons_path'] + '\n> ')

        if arg and arg not in c.available_update_args:
            print(self.lang['update_no_arg']+str(c.available_update_args))

        for text in self.config_text:
            if text not in new_config_text:
                new_config_text[text] = self.config_text[text]
        t.set_config_file(c.full_path_config, new_config_text)

    def remove(self):
        print(self.lang['remove_config'])
        if t.yes_no(self.lang['remove_are_you_sure']):
            shutil.rmtree(c.path_config)
            print(self.lang['remove_config_file_removed'])