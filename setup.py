#!/usr/bin/env python
from distutils.core import setup

setup(
    name = 'marketdata',
	version = '0.2',
	description = 'Library for working with Market Data',
	packages = ['marketdata'],
	install_requires = ['numpy', 'pymongo'],
	author='Andrei Visnakovs',
	author_email='andrei@visnakovs.com'
)
