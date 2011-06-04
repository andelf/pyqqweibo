#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-04 01:55:58 andelf>

try:
    from urllib2 import Request, urlopen
    import urlparse
    from urllib import quote, unquote, urlencode
    import htmlentitydefs
    from cgi import parse_qs
except ImportError:
    from urllib.request import Request, urlopen
    import urllib.parse as urlparse
    from urllib.parse import quote, unquote, urlencode, parse_qs
    import html.entities as htmlentitydefs

try:
    import cPickle as pickle
except ImportError:
    import pickle


def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise ImportError("Can't load a json library")

    return json

json = import_simplejson()

