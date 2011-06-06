#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 andelf <andelf@gmail.com>
# Time-stamp: <2011-06-05 01:54:24 andelf>

#from distutils.core import setup
from setuptools import setup, find_packages
import os, sys

lib_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, lib_path)

from qqweibo import version


setup(name = "pyqqweibo",
      version = version,
      author = "andelf",
      author_email = "andelf@gmail.com",
      description = ("QQ weibo API SDK for python"),
      license = "MIT",
      keywords= "qq weibo library tencent microblog",
      url="http://github.com/andelf/pyqqweibo",
      packages = ['qqweibo'],
      long_description = """
      QQ weibo is a microblog service that is popular among Chinese.

      This is the SDK tools for QQ weibo, written by @andelf.

      * fix the bad offical api names and arangement.
      * With model parser support, cache support.
      * Under active development.
      * Py2.x and Py3.x support
      * document & samples included
      * MIT license

      NOTE: this is a thrid party SDK, use at your risk.
      """,
      classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Natural Language :: Chinese (Simplified)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.0",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities"
          ],
      zip_safe = True)

