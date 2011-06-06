#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-06 00:46:10 andelf>

import xml.dom.minidom as dom
import xml.etree.ElementTree as ET

from qqweibo.compat import json
from qqweibo.models import ModelFactory
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


class XMLRawParser(Parser):
    """return string of xml"""
    payload_format = 'xml'

    def parse(self, method, payload):
        return payload

    def parse_error(self, method, payload):
        return payload


class XMLDomParser(XMLRawParser):
    """return xml.dom.minidom object"""
    def parse(self, method, payload):
        return dom.parseString(payload)


class XMLETreeParser(XMLRawParser):
    """return elementtree object"""
    def parse(self, method, payload):
        return ET.fromstring(payload)


class JSONParser(Parser):

    payload_format = 'json'

    def __init__(self):
        self.json_lib = json

    def parse(self, method, payload):
        try:
            json = self.json_lib.loads(payload, encoding='utf-8')
        except Exception as e:
            print ("Failed to parse JSON payload:" + str(payload))
            raise QWeiboError('Failed to parse JSON payload: %s' % e)

        return json

    def parse_error(self, method, payload):
        return self.json_lib.loads(payload, encoding='utf-8')


class ModelParser(JSONParser):

    def __init__(self, model_factory=None):
        JSONParser.__init__(self)
        self.model_factory = model_factory or ModelFactory

    def parse(self, method, payload):
        try:
            if method.payload_type is None:
                return
            model = getattr(self.model_factory, method.payload_type)
        except AttributeError:
            raise QWeiboError('No model for this payload type: %s' % method.payload_type)

        json = JSONParser.parse(self, method, payload)
        data = json['data']

        print (dir(method))
        print (method.parameters)
        print (method.method)
        # pager support
        if 'pagetime' in method.allowed_param:
            pass

        #        hasnext = False
        #        if isinstance(json, dict):      # has data, not None
        #            if 'info' in json:
        #                hasnext = json.get('hasnext', 1) == 0
        #                json = json['info']         # got data list or data
        if 'info' in data:
            data = data['info']

        if method.payload_list:
            result = model.parse_list(method.api, data)
        else:
            result = model.parse(method.api, data)
        return result

