#!/usr/bin/python
# -*- coding: utf-8 -*-


class QWeiboError(Exception):
    """basic weibo error class"""
    pass


def assertion(condition, msg):
    try:
        assert condition, msg
    except AssertionError as e:
        raise QWeiboError(e.message)
