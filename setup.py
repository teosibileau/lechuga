# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

required = [
    '-i https://pypi.org/simple',
    'certifi==2018.11.29',
    'chardet==3.0.4',
    'click==7.0',
    'colorama==0.4.1',
    'idna==2.7',
    'requests-cache==0.4.13',
    'requests==2.20.1',
    'simplejson==3.16.0',
    'tabulate==0.8.2',
    'urllib3==1.24.1; python_version < \'4\'',
]

setup(
    name='lechuga',
    version='0.2',
    author=u'Teofilo Sibileau',
    author_email='teo.sibileau@gmail.com',
    license='MIT license, see LICENSE',
    description='retrieves AR$ rates from fixer.io API',
    packages=['lechuga'],
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'lechuga = lechuga.lechuga:run',
        ],
    },
    install_requires=required,
)
