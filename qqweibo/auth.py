#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-04 08:14:39 andelf>

from compat import Request, urlopen
import oauth
import oauth2
from error import QWeiboError
from api import API
from utils import convert_to_utf8_bytes


class AuthHandler(object):

    def authorize_request(self, url, method, headers, parameters):
        raise NotImplementedError



class OAuth1_0_Handler(AuthHandler):
    """OAuth authentication handler"""

    OAUTH_HOST = 'open.t.qq.com'
    OAUTH_ROOT = '/cgi-bin/'
    AUTH_TYPE = "OAuth1.0"

    def __init__(self, consumer_key, consumer_secret, callback=None):
        self._consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self._sigmethod = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.request_token = None
        self.access_token = None
        self.callback = callback or 'null'  # fixed
        self.username = None

    def _get_oauth_url(self, endpoint):
        if endpoint in ('request_token', 'access_token'):
            prefix = 'https://'
        else:
            prefix = 'http://'
        return prefix + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    def authorize_request(self, url, method, headers, parameters):
        request = oauth.OAuthRequest(http_method=method, http_url=url, parameters=parameters)
        request.sign_request(self._sigmethod, self._consumer, self.access_token)
        return request.to_url()

    def _get_request_token(self):
        try:
            url = self._get_oauth_url('request_token')
            request = oauth.OAuthRequest.from_consumer_and_token(
                self._consumer, http_url=url, callback=self.callback
            )
            request.sign_request(self._sigmethod, self._consumer, None)
            resp = urlopen(Request(request.to_url()))  # must
            return oauth.OAuthToken.from_string(resp.read().decode('ascii'))
        except RuntimeError as e:
            raise QWeiboError(e)

    def set_request_token(self, key, secret):
        self.request_token = oauth.OAuthToken(key, secret)

    def set_access_token(self, key, secret):
        self.access_token = oauth.OAuthToken(key, secret)

    def get_authorization_url(self, signin_with_weibo=False):
        """Get the authorization URL to redirect the user"""
        try:
            # get the request token
            self.request_token = self._get_request_token()

            # build auth request and return as url
            if signin_with_weibo:
                url = self._get_oauth_url('authenticate')
            else:
                url = self._get_oauth_url('authorize')
            request = oauth.OAuthRequest.from_token_and_callback(
                token=self.request_token, http_url=url, callback=self.callback
            )

            return request.to_url()
        except RuntimeError as e:
            raise QWeiboError(e)

    def get_access_token(self, verifier=None):
        """
        After user has authorized the request token, get access token
        with user supplied verifier.
        """
        try:
            url = self._get_oauth_url('access_token')
            # build request
            request = oauth.OAuthRequest.from_consumer_and_token(
                self._consumer,
                token=self.request_token, http_url=url,
                verifier=str(verifier)
            )
            request.sign_request(self._sigmethod, self._consumer, self.request_token)

            # send request
            resp = urlopen(Request(request.to_url()))  # must
            self.access_token = oauth.OAuthToken.from_string(resp.read().decode('ascii'))

            #print ('Access token key: ' + str(self.access_token.key))
            #print ('Access token secret: ' + str(self.access_token.secret))

            return self.access_token
        except Exception as e:
            raise QWeiboError(e)

    def setToken(self, token, tokenSecret):
        self.access_token = oauth.OAuthToken(token, tokenSecret)




class OAuth2_0_Handler(AuthHandler):
    BASE_URL = "https://open.t.qq.com/cgi-bin/oauth2/"
    AUTH_TYPE = "OAuth2.0"

    def __init__(self, API_Key, API_Secret, callback=None, wap=None, state=None, forcelogin=None):

        self.callback = callback
        self._oauth = oauth2.Client2(API_Key, API_Secret, self.BASE_URL,
                                   redirect_uri=callback)
        self.http = self._oauth.http

        self.secret = API_Secret

        self.apiKey = API_Key

        self.openid = None
        self.accessToken = None
        self.refreshToken = None

        self.params = {}
        if wap is not None:
            self.params['wap'] = wap
        if state is not None:
            self.params['state'] = scope
        if forcelogin is not None:
            self.params['forcelogin'] = forcelogin

    def get_authorization_url(self):
        redirect_uri = self.callback
        params = self.params
        return self._oauth.authorization_url(redirect_uri, params)

    def get_access_token(self, code):
        redirect_uri = self.callback
        params = {}
        if 'state' in self.params:
            params['state'] = self.params['state']
        token = self._oauth.access_token(code, redirect_uri, params)
        self.set_token(token)
        return token

    def set_token(self, token):
        self.openid = token['openid']
        self.accessToken = token['access_token']
        self.refreshToken = token['refresh_token']

    def authorize_request(self, url, method, headers, parameters):
        query = dict(parameters)
        if "oauth_consumer_key" not in query:
            query["oauth_consumer_key"] = self.apiKey
        if "access_token" not in query:
            query["access_token"] = self.accessToken
        if "openid" not in query:
            query["openid"] = self.openid
        if "scope" not in query:
            query["scope"] = "all"
        if "clientip" not in query:
            query["clientip"] = "127.0.0.1"
        query["oauth_version"] = "2.a"

        query = query.items()
        query = [(str(k), convert_to_utf8_bytes(v)) for k,v in query]
        query.sort()
        if method == 'POST':
            return url, query
        elif method == 'GET':
            print query
            params = '&'.join(("%s=%s" % kv) for kv in query)
            if '?' in url:
                return "%s&%s" % (url, params), query
            else:
                return "%s?%s" % (url, params), query


class OpenId_OpenKey_Handler(AuthHandler):
    BASE_URL = "https://open.t.qq.com/cgi-bin/oauth2/"
    AUTH_TYPE = "OpenId&OpenKey"

    def __init__(self, API_Key, API_Secret, callback=None, wap=None, state=None, forcelogin=None):

        self.callback = callback
        self._oauth = oauth.Client2(API_Key, API_Secret, self.BASE_URL,
                                   redirect_uri=callback)
        self.http = self._oauth.http

        self.secret = API_Secret
        self.apiKey = API_Key

        self.openid = None
        self.openkey = None

        self.params = {}
        if wap is not None:
            self.params['wap'] = wap
        if state is not None:
            self.params['state'] = scope
        if forcelogin is not None:
            self.params['forcelogin'] = forcelogin

    def get_authorization_url(self):
        redirect_uri = self.callback
        params = self.params
        return self._oauth.authorization_url(redirect_uri, params)

    def set_token(self, openid, openkey):
        self.openid = openid
        self.openkey = openkey

    def authorize_request(self, url, method, headers, parameters):
        query = dict(parameters)
        if "appid" not in query:
            query["appid"] = self.apiKey
        if "openid" not in query:
            query["openid"] = self.openid
        if "openkey" not in query:
            query["openkey"] = self.openkey
        if "clientip" not in query:
            query["clientip"] = "127.0.0.1"
        if "reqtime" not in query:
            query["reqtime"] = utils.timestamp()
        query["wbversion"] = "1"

        query = query.items()
        query = [(str(k), to_utf8(v)) for k,v in query]
        query.sort()
        uri = urlparse.urlparse(url)[2] # url path
        raw = '&'.join(method, urlencode(uri), urlencode('&'.join(("%s=%s" % kv) for kv in query)))
        hashed = hmac.new(self.openKey, raw, hashlib.sha1)
        # Calculate the digest base 64.
        #return binascii.b2a_base64(hashed.digest())[:-1]
        # fix py3k, str() on a bytes obj will be a "b'...'"
        sig = binascii.b2a_base64(hashed.digest())[:-1]
        print ret
        return ret.decode('ascii')

        if method == 'POST':
            return url, query
        elif method == 'GET':
            print query
            params = '&'.join(("%s=%s" % kv) for kv in query)
            if '?' in url:
                return "%s&%s" % (url, params), query
            else:
                return "%s?%s" % (url, params), query
