#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="qqweibo",
      version="0.2",
      description="QQ Weibo library for python",
      license="MIT",
      author="andelf",
      author_email="andelf@gmail.com",
      url="http://github.com/andelf/pyqqweibo",
      packages = find_packages(),
      keywords= "qq weibo library",
      zip_safe = True)

