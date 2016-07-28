#!/usr/bin/python

from distutils.core import setup

setup(
	# Basic package information.
	name = 'twitter',
	version = '0.0.0',
	packages = ['twitter'],
	include_package_data = True,
	install_requires = ['httplib2', 'simplejson'],
	license='LICENSE.txt',
	url = 'https://github.com/alexcchan/twitter/tree/master',
	keywords = 'twitter api',
	description = 'Twitter API Wrapper for Python',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Internet'
	],
)


