#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-08 19:22:59 andelf>

from datetime import datetime
import time
import re
import sys

from qqweibo.compat import htmlentitydefs


def parse_datetime(str):
    # We must parse datetime this way to work in python 2.4
    return datetime(*(time.strptime(str, '%a %b %d %H:%M:%S +0800 %Y')[0:6]))


def parse_html_value(html):
    return html[html.find('>') + 1:html.rfind('<')]


def parse_a_href(atag):
    start = atag.find('"') + 1
    end = atag.find('"', start)
    return atag[start:end]


def parse_search_datetime(str):
    # python 2.4
    return datetime(*(time.strptime(str, '%a, %d %b %Y %H:%M:%S +0000')[0:6]))


def unescape_html(text):
    """Created by Fredrik Lundh
    (http://effbot.org/zone/re-sub.htm#unescape-html)"""
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def convert_to_utf8_unicode(arg):
    """TODO: currently useless"""
    pass


def convert_to_utf8_str(arg):
    # written by andelf ^_^
    # return py2str py3str
    # fix py26
    MAJOR_VERSION = sys.version_info[0]
    if MAJOR_VERSION == 3:
        unicodeType = str
        if type(arg) == unicodeType:
            return arg
        elif type(arg) == bytes:
            return arg.decode('utf-8')
    else:
        unicodeType = __builtins__['unicode']
        if type(arg) == unicodeType:
            return arg.encode('utf-8')
        elif type(arg) == str:
            return arg
    # assume list
    if hasattr(arg, '__iter__'):
        arg = ','.join(map(convert_to_utf8_str, arg))
    return str(arg)


def convert_to_utf8_bytes(arg):
    # return py2str py3bytes
    if type(arg) == bytes:
        return arg
    ret = convert_to_utf8_str(arg)
    return ret.encode('utf-8')


def timestamp_to_str(tm):
    return time.ctime(tm)
