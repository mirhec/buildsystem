#!/usr/bin/env python

from distutils.core import setup

setup(name='buildsystem',
      version='1.6',
      description='A very simple, python-based and extendable buildsystem.',
      author='Mirko Hecky',
      url='https://github.com/mirhec/buildsystem',
      download_url='https://github.com/mirhec/buildsystem/archive/1.6.tar.gz',
      packages=['buildsystem', 'buildsystem.examples'],
      keywords=['buildsystem', 'build', 'automation']
)