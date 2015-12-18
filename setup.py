# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='lechuga',
    version='0.1',
    author=u'Teofilo Sibileau',
    author_email='teo.sibileau@gmail.com',
    license='MIT license, see LICENSE',
    description='retrieves AR$ <-> USD exchange rate',
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