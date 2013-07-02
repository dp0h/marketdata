#!/usr/bin/env python
from distutils.core import setup

setup(
	name = 'marketdata',
	version = '0.1',
	description = 'Library for working with Market Data',
	packages = ['marketdata'],
	install_requires = ['numpy', 'pandas', 'sqlalchemy', 'pysqlite'],
	author='Andrei Visnakovs',
	author_email='andrei@visnakovs.com'
)
