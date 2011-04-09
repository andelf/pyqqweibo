#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
#  Description : description 
#  Time-stamp: <2011-04-09 19:37:14 andelf> 


from qqweibo.models import ModelFactory
from qqweibo.utils import import_simplejson
from qqweibo.error import QWeiboError

class Parser(object):

    def parse(self, method, payload):
        """
        Parse the response payload and return the result.
        Returns a tuple that contains the result data and the cursors
        (or None if not present).
        """
        raise NotImplementedError

    def parse_error(self, method, payload):
        """
        Parse the error message from payload.
        If unable to parse the message, throw an exception
        and default error message will be used.
        """
        raise NotImplementedError


class JSONParser(Parser):

    payload_format = 'json'

    def __init__(self):
        self.json_lib = import_simplejson()

    def parse(self, method, payload):
        try:
            json = self.json_lib.loads(payload)
        except Exception, e:
            print "Failed to parse JSON payload:"+ str(payload)
            raise QWeiboError('Failed to parse JSON payload: %s' % e)

        #if isinstance(json, dict) and 'previous_cursor' in json and 'next_cursor' in json:
        #    cursors = json['previous_cursor'], json['next_cursor']
        #    return json, cursors
        #else:
        return json

    def parse_error(self, method, payload):
        return self.json_lib.loads(payload)


class ModelParser(JSONParser):

    def __init__(self, model_factory=None):
        JSONParser.__init__(self)
        self.model_factory = model_factory or ModelFactory

    def parse(self, method, payload):
        try:
            if method.payload_type is None: return
            model = getattr(self.model_factory, method.payload_type)
        except AttributeError:
            raise QWeiboError('No model for this payload type: %s' % method.payload_type)

        json = JSONParser.parse(self, method, payload)
        json = json['data']             # got data
        hasnext = False
        if isinstance(json, dict):      # has data, not None
            if 'info' in json:
                hasnext = json.get('hasnext', 1) == 0
                json = json['info']         # got data list or data

        if method.payload_list:
            result = model.parse_list(method.api, json)
        else:
            result = model.parse(method.api, json)
        if hasnext:                     # 0 表示还有微博可拉取 1 已拉取完毕
            #print 'hasnext', hasnext
            pass
        return result

