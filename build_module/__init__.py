#!/usr/bin/env python3
import sys
import os
from . import consts
from . import setup
from . import tools
from . import module

c = consts.Consts()
s = setup.Setup()
t = tools.Tools()
m = module.Module()

command = sys.argv[1] if len(sys.argv) > 1 else None
arg1 = sys.argv[2] if len(sys.argv) > 2 else None
arg2 = sys.argv[3] if len(sys.argv) > 3 else None

lang = t.get_language_file()

# Differents commands:
# setup, update [arg], remove, create, help

# If package is already set up
if t.check_setup():
    if command == 'setup':
        print(lang['init_package_already_setup'])
    elif command == 'update':
        s.update(arg=arg1)
    elif command == 'remove':
        s.remove()
    elif command == 'create':
        m.create(arg1=arg1, arg2=arg2)
    elif command == 'help':
        t.read_help()
    else:
        print(lang['tools_bad_argument'])

# If the package is not set up
else:
    if command == 'setup':
        s.setup()
    else:
        print(lang['init_package_not_setup'])
