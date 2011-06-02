#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "qqweibo",
      version = "0.2.1",
      author = "andelf",
      author_email = "andelf@gmail.com",
      description = ("QQ weibo API SDK in python"),
      license = "MIT",
      keywords= "qq weibo library tencent microblog",
      url="http://github.com/andelf/pyqqweibo",
      packages = find_packages(),
      long_description = """
      QQ weibo API SDK, python version.
      With model parser support, cache support.
      And is under active development.
      NOTE: this is a thrid party SDK.
      """,
      classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Natural Language :: Chinese (Simplified)",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
          "Topic :: Utilities"
          ],
      zip_safe = True)

