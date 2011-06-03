#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup, find_packages


setup(name = "pyqqweibo",
      version = "0.3.1",
      author = "andelf",
      author_email = "andelf@gmail.com",
      description = ("QQ weibo API SDK for python"),
      license = "MIT",
      keywords= "qq weibo library tencent microblog",
      url="http://github.com/andelf/pyqqweibo",
      packages = find_packages(),
      long_description = """
      QQ weibo API SDK, python version.
      QQ weibo is a microblog service that is popular among Chinese.

      * fix the bad offical api names and arangement.
      * With model parser support, cache support.
      * Under active development.
      * Py2.x and Py3.x support

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

