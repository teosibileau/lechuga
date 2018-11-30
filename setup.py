# -*- coding: utf-8 -*-
import os
from distutils.core import setup

setup(
    name='lechuga',
    version='0.2',
    author=u'Teofilo Sibileau',
    author_email='teo.sibileau@gmail.com',
    license='MIT license, see LICENSE',
    description='retrieves AR$ exchange rates',
    packages=['lechuga'],
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'lechuga = lechuga.lechuga:run',
        ],
    },
)