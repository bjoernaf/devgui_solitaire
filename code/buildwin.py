# -*- coding: utf-8 -*-

# Creates a windows executable for a PyQT5 program.
#
# Run the build process by running the command 'python buildwin.py build'
# Python has to be set in your PATH variable.
#
# If everything works well you should find a subdirectory in the build
# subdirectory (code/build/) that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(name='Solitaire',
      version='0.1',
      description='Solitaire game',
      options=options,
      executables=executables
      )