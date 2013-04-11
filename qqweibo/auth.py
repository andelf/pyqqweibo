#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-06-04 08:14:39 andelf>

from compat import Request, urlopen, urlencode, urlparse, parse_qsl, quote
import oauth
from error import QWeiboError
from api import API
from utils import convert_to_utf8_bytes
import utils


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

    def __init__(self, API_Key, API_Secret, callback, wap=None, state=None, forcelogin=None):

        if callback is None:
            raise ValueError("Redirect_uri must be set.")

        self.callback = callback

        self._api_secret = API_Secret

        self._api_key = API_Key

        self.openid = None
        self.access_token = None
        self.refresh_token = None

        self.params = {}
        if wap is not None:
            self.params['wap'] = wap
        if state is not None:
            self.params['state'] = scope
        if forcelogin is not None:
            self.params['forcelogin'] = forcelogin

    def get_authorization_url(self):
        """return a url for user to open
        Get the URL to redirect the user for client authorization
        https://svn.tools.ietf.org/html/draft-hammer-oauth2-00#section-3.5.2.1
        """
        endpoint = 'authorize'
        redirect_uri = self.callback
        params = self.params

        args = {
            'response_type': 'code',
            'client_id': self._api_key
        }

        args['redirect_uri'] = self.callback
        args.update(params or {})

        return '%s?%s' % (urlparse.urljoin(self.BASE_URL, endpoint),
                          urlencode(args))


    def get_access_token(self, code):
        """user code to access token
        Get an access token from the supplied code
        https://svn.tools.ietf.org/html/draft-hammer-oauth2-00#section-3.5.2.2
        """
        if code is None:
            raise ValueError("Code must be set.")

        endpoint='access_token'

        params = {}
        if 'state' in self.params:
            params['state'] = self.params['state']

        args = {
            'grant_type': 'authorization_code',
            'client_id': self._api_key,
            'client_secret': self._api_secret,
            'code': code,
            'redirect_uri': self.callback,
        }

        args.update(params or {})

        uri = urlparse.urljoin(self.BASE_URL, endpoint)
        body = urlencode(args)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        req = Request(uri, body, headers)
        resp = urlopen(req)
        content = resp.read()

        if not resp.code == 200:
            print (resp, resp.code, content)
            raise Error(content)

        response_args = dict(parse_qsl(content))

        error = response_args.get('error', None)
        if error is not None:
            msg = "%s:%s" % (error,
                             response_args.get('error_description', ''))
            raise Error(msg)

        refresh_token = response_args.get('refresh_token', None)
        access_token = response_args.get('access_token', None)
        openid = response_args.get('openid', None)

        if refresh_token is not None:
            response_args = self.refresh(refresh_token)

        self.refresh_token = refresh_token
        self.access_token = access_token
        self.openid = openid

        return response_args

    def set_token(self, openid, access_token, refresh_token):
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.openid = openid

    def refresh(self, refresh_token=None):
        """Get a new access token from the supplied refresh token
        https://svn.tools.ietf.org/html/draft-hammer-oauth2-00#section-4
        """
        endpoint = 'access_token'
        refresh_token = refresh_token or self.refresh_token
        if not refresh_token:
            raise ValueError("refresh_token can't be empty")

        args = {
            'grant_type': 'refresh_token',
            'client_id': self._api_key,
            'refresh_token': refresh_token,
        }

        uri = urlparse.urljoin(self.oauth_base_url, endpoint)
        body = urlencode(args)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        resp = urlopen(uri, body, headers)
        content = resp.read()

        if not resp.code == 200:
            raise Error(content)

        response_args = dict(parse_qsl(content))
        self.access_token = response_args.get("access_token", None)
        self.refresh_token = response_args.get("refresh_token", None)
        return response_args



    def authorize_request(self, url, method, headers, parameters):
        query = dict(parameters)
        if "oauth_consumer_key" not in query:
            query["oauth_consumer_key"] = self.api_key
        if "access_token" not in query:
            query["access_token"] = self.access_token
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
