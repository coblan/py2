# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes':  ["openpyxl", "os", "re", "sys",'atexit'],
        "include_files":[(r"D:\coblan\py2\work\attend_excel\.constants.json",r"openpyxl/.constants.json")]
    }
}

executables = [
    Executable('selwin.py', base=base)
]

setup(name='metaupload',
      version='0.1',
      description='metainfo upload tool',
      options=options,
      executables=executables
      )
