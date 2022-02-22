#!/usr/bin/env python3

import re
import sys
import os
from setuptools import setup


SRC = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(SRC, 'ig2wp/__init__.py')) as f:
        for line in f:
            m = re.match("__version__ = '(.*)'", line)
            if m:
                return m.group(1)
    raise SystemExit("Could not find version string.")


requirements = ['requests>=2.4']

keywords = (['instagram', 'wordpress', 'wordpress-uploader', 'instagram-post', 'instagram-wordpress', 'videos', 'photos',
             'pictures', 'instagram-user-photos', 'instagram-photos', 'instagram-metadata', 'instagram-downloader',
            ])

# NOTE that many of the values defined in this file are duplicated on other places, such as the
# documentation.

setup(
    name='ig2wp',
    version=get_version(),
    packages=['ig2wp'],
    package_data={'ig2wp': ['py.typed']},
    url='https://github.com/aderbique/ig2wp',
    license='MIT',
    author='Austin Derbique',
    author_email='austin@derbique.us',
    description='Upload posts from Instagram to Wordpress using Instaloader Tool',
    long_description=open(os.path.join(SRC, 'README.md')).read(),
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={'console_scripts': ['ig2wp=ig2wp.__main__:main']},
    zip_safe=False,
    keywords=keywords,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics'
    ]
)
