#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-auth.py 
#  Author      : Feather.et.ELF <andelf@gmail.com> 
#  Created     : Fri Apr 08 15:35:36 2011 by Feather.et.ELF 
#  Copyright   : andelf <andelf@gmail.com> (c) 2011 
#  Description : example to show how to do authentication
#  Time-stamp: <2011-04-08 16:51:44 andelf> 

import sys
sys.path.insert(0, "..")

from qqweibo.auth import OAuthHandler
from qqweibo.api import API
from qqweibo.parsers import JSONParser
import webbrowser


API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print u'必须正确填写 API_KEY 和 API_SECRET'
    raise SystemExit('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)

## use get_authorization_url if you haven't got a token
url = auth.get_authorization_url()
print 'Open', url, 'in your browser'
webbrowser.open_new(url)
verifier = raw_input('Your PIN: ').strip()
auth.get_access_token(verifier)

## or if you already have token
#token = 'your token'
#tokenSecret = 'yourr tokenSecret'
#auth.setToken(token, tokenSecret)


# now you have a workable api
api = API(auth, parser=JSONParser())
# or use `api = API(auth)`

I = api.me()
print I
data = I['data']
print data['name'], data['nick'], data['location']
