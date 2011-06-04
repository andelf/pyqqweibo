#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2010 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-03 13:30:10 andelf>

class QWeiboError(Exception):
    """basic weibo error class"""
    pass


def assertion(condition, msg):
    try:
        assert condition, msg
    except AssertionError as e:
        raise QWeiboError(e.message)
