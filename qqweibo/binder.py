#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-09-05 19:40:35 wangshuyu>

import time
import re

from qqweibo.compat import Request, urlopen, quote, urlencode
from qqweibo.error import QWeiboError
from qqweibo.utils import convert_to_utf8_str


re_path_template = re.compile('{\w+}')


def bind_api(**config):

    class APIMethod(object):

        path = config['path']
        payload_type = config.get('payload_type', None)
        payload_list = config.get('payload_list', False)
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', False)

        def __init__(self, api, args, kargs):
            # If authentication is required and no credentials
            # are provided, throw an error.
            if self.require_auth and not api.auth:
                raise QWeiboError('Authentication required!')

            self.api = api
            self.payload_format = api.parser.payload_format
            self.post_data = kargs.pop('post_data', None)
            self.retry_count = kargs.pop('retry_count', api.retry_count)
            self.retry_delay = kargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kargs.pop('retry_errors', api.retry_errors)
            self.headers = kargs.pop('headers', {})
            self.build_parameters(args, kargs)
            self.api_root = api.api_root

            # Perform any path variable substitution
            self.build_path()

            self.scheme = 'http://'

            self.host = api.host

            # Manually set Host header to fix an issue in python 2.5
            # or older where Host is set including the 443 port.
            # This causes Twitter to issue 301 redirect.
            # See Issue http://github.com/joshthecoder/tweepy/issues/#issue/12
            self.headers['Host'] = self.host

        def build_parameters(self, args, kargs):
            # bind here, as default
            self.parameters = {'format': self.payload_format}
            for idx, arg in enumerate(args):
                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise QWeiboError('Too many parameters supplied!')

            for k, arg in kargs.items():
                if bool(arg) == False:
                    continue
                if k in self.parameters:
                    raise QWeiboError('Multiple values for parameter `%s` supplied!' % k)
                #if k not in self.allowed_param:
                #    raise QWeiboError('`%s` is not allowd in this API function.' % k)
                self.parameters[k] = convert_to_utf8_str(arg)

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                if name == 'user' and self.api.auth:
                    value = self.api.auth.get_username()
                else:
                    try:
                        value = quote(self.parameters[name])
                    except KeyError:
                        raise QWeiboError('No parameter value found for path variable: %s' % name)
                    del self.parameters[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build the request URL
            url = self.api_root + self.path
            #if self.api.source is not None:
            #    self.parameters.setdefault('source',self.api.source)

            if len(self.parameters):
                if self.method == 'GET':
                    url = '%s?%s' % (url, urlencode(self.parameters))
                else:
                    self.headers.setdefault("User-Agent", "pyqqweibo")
                    if self.post_data is None:
                        self.headers.setdefault("Accept", "text/html")
                        self.headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
                        # asure in bytes format
                        self.post_data = urlencode(self.parameters).encode('ascii')
            # Query the cache if one is available
            # and this request uses a GET method.
            if self.api.cache and self.method == 'GET':
                cache_result = self.api.cache.get(url)
                # if cache result found and not expired, return it
                if cache_result:
                    # must restore api reference
                    if isinstance(cache_result, list):
                        for result in cache_result:
                            result._api = self.api
                    else:
                        cache_result._api = self.api
                    return cache_result
                #urllib.urlencode(self.parameters)
            # Continue attempting request until successful
            # or maximum number of retries is reached.
            sTime = time.time()
            retries_performed = 0
            while retries_performed < self.retry_count + 1:
                # Open connection
                # FIXME: add timeout
                # Apply authentication
                if self.require_auth and self.api.auth:
                    url_full = self.api.auth.get_authed_url(
                        self.scheme + self.host + url,
                        self.method, self.headers, self.parameters
                    )
                else:                   # this brunch is never accoured
                    url_full = self.api.auth.get_signed_url(
                        self.scheme + self.host + url,
                        self.method, self.headers, self.parameters
                    )
                try:
                    if self.method == 'POST':
                        req = Request(url_full, data=self.post_data, headers=self.headers)
                    else:
                        req = Request(url_full)
                    resp = urlopen(req)
                except Exception as e:
                    raise QWeiboError("Failed to request %s headers=%s %s" % \
                                      (url, self.headers, e))

                # Exit request loop if non-retry error code
                if self.retry_errors:
                    if resp.code not in self.retry_errors:
                        break
                else:
                    if resp.code == 200:
                        break

                # Sleep before retrying request again
                time.sleep(self.retry_delay)
                retries_performed += 1

            # If an error was returned, throw an exception
            body = resp.read()
            self.api.last_response = resp
            if self.api.log is not None:
                requestUrl = "URL:http://" + self.host + url
                eTime = '%.0f' % ((time.time() - sTime) * 1000)
                postData = ""
                if self.post_data is not None:
                    postData = ",post:" + self.post_data[:500]
                self.api.log.debug("%s, time: %s, %s result: %s" % (requestUrl, eTime, postData, body))

            retcode = 0
            errcode = 0
            # for py3k, ^_^
            if not hasattr(body, 'encode'):
                body = str(body, 'utf-8')
            if self.api.parser.payload_format == 'json':
                try:
                    # BUG: API BUG, refer api.doc.rst
                    if body.endswith('out of memery'):
                        body = body[:body.rfind('}')+1]
                    json = self.api.parser.parse_error(self, body)
                    retcode = json.get('ret', 0)
                    msg = json.get('msg', '')
                    # only in some post request
                    errcode = json.get('errcode', 0)
                except ValueError as e:
                    retcode = -1
                    msg = "Bad json format (%s)" % e
                finally:
                    if retcode + errcode != 0:
                        raise QWeiboError("Response error: %s. (ret=%s, errcode=%s)" % \
                                          (msg, retcode, errcode))

            # Parse the response payload
            result = self.api.parser.parse(self, body)

            # Store result into cache if one is available.
            if self.api.cache and self.method == 'GET' and result:
                self.api.cache.store(url, result)
            return result

    def _call(api, *args, **kargs):
        method = APIMethod(api, args, kargs)
        return method.execute()

    # make doc string
    if config.get('payload_list', False):
        rettype = '[%s]' % config.get('payload_type', None)
    else:
        rettype = str(config.get('payload_type', None))
    doc_string = """ \
    Call API Method %s
    (%s) => %s""" % (config['path'],
                     ', '.join(config.get('allowed_param', [])),
                     rettype)
    _call.__doc__ = doc_string

    return _call
