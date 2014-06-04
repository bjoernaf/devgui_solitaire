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
        'includes': 'atexit',
        'include_files': ['images/']
    }
}

executables = [
    Executable('main.py', base=base)
]

setup(name='Solitaire',
      version='1.0',
      description='Solitaire game',
      author='Group 13',
      options=options,
      executables=executables
      )