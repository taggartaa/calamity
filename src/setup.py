#!/usr/bin/env python

"""
@file setup.py
@date 8/23/2010
@version 0.1
@author Aaron Taggart

@brief Setup call for Distutils
"""

from distutils.core import setup

setup(name='Calamity',
      version='0.1',
      description='IM client writen in Python',
      author='Aaron Taggart',
      url='none',
      author_email='ajtaggs@gmail.com',
      packages=['calamity', 'gui', 'network']
     )
