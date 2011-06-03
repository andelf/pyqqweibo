#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.


from datetime import datetime
import time
import re

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
    """Created by Fredrik Lundh (http://effbot.org/zone/re-sub.htm#unescape-html)"""
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


def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    # modified by andelf ^_^
    if type(arg) == str:
        return arg
    elif hasattr(arg, 'decode'):
        arg = arg.decode('utf-8')
    elif hasattr(arg, '__iter__'):      # FIX list param
        arg = ','.join(map(convert_to_utf8_str, arg))
    elif not isinstance(arg, str):
        arg = str(arg)
    return arg


def convert_to_utf8_bytes(arg):
    if type(arg) == bytes:
        return arg
    ret = convert_to_utf8_str(arg)
    return ret.encode('utf-8')


def timestamp_to_str(tm):
    return time.ctime(tm)

