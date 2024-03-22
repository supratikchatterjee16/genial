from setuptools import setup, Extension, find_packages

with open('README.md') as f:
	extd_desc = f.read()

with open('LICENSE') as f:
    license = f.read()


with open('requirements.txt', 'r') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
	# Meta information
	name				= 'genial',
	version				= '0.1.0',
	author				= 'Supratik Chatterjee',
	author_email			= 'supratikdevm96@gmail.com',
	url				= 'https://github.com/supratikchatterjee16/genial',
	description			= '',
	keywords			= ["integration", "genial", "api", "loading"],
	install_requires		= requirements,
	# build information
	py_modules			= ['genial'],
	packages			= find_packages(),
	package_dir			= {'genial' : 'genial'},
	include_package_data		= True,
	long_description		= extd_desc,
	long_description_content_type	= 'text/markdown',
	package_data			= {'genial' : [
						'data/*',
						]},
    entry_points		= {'console_scripts' : ['genial = genial:run'],},
	zip_safe			= True,
	# https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py
	classifiers			= [
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
	license 			= license
)