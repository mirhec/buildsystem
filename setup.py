#!/usr/bin/env python

from distutils.core import setup

setup(name='buildsystem',
      version='1.0',
      description='A very simple, python-based and extendable buildsystem.',
      author='Mirko Hecky',
      url='https://github.com/mirhec/buildsystem',
      packages=['buildsystem', 'buildsystem.examples'],
      install_requires=['futures;python_version<"3.4"'],
)