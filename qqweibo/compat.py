#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2010 andelf <andelf@gmail.com>
# See LICENSE for details.

try:
    from urllib2 import Request, urlopen
    import urlparse
    from urllib import quote, unquote, urlencode
    import htmlentitydefs
except ImportError:
    from urllib.request import Request, urlopen
    import urllib.parse as urlparse
    from urllib.parse import quote, unquote, urlencode
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
