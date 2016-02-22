from distutils.core import setup
import py2exe, sys, os
sys.argv.append('py2exe')

setup(windows=[{'script': "MainProgram.py"}])
time.sleep(2)
