#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-auth.py
#  Author      : Feather.et.ELF <andelf@gmail.com>
#  Created     : Fri Apr 08 15:35:36 2011 by Feather.et.ELF
#  Copyright   : andelf <andelf@gmail.com> (c) 2011
#  Description : example to show how to do authentication
#  Time-stamp: <2011-06-04 11:37:50 andelf>


from __future__ import unicode_literals
import sys
sys.path.insert(0, '..')
import webbrowser
from qqweibo import OAuthHandler, API, JSONParser


# for py3k
try:
    input = raw_input
except:
    pass


API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print ('You must fill API_KEY and API_SECRET!')
    webbrowser.open("http://open.t.qq.com/apps_index.php")
    raise RuntimeError('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)
# or you can use callback url
# auth = OAuthHandler(API_KEY, API_SECRET,
#     callback="http://localhost:5000/callback")
# will be callbackurl?oauth_token=[OAUTH_TOKEN]&oauth_verifier=[VERIFIER]

## use get_authorization_url if you haven't got a token
url = auth.get_authorization_url()
print ('Opening {:s} in your browser...'.format(url))
webbrowser.open_new(url)
verifier = input('Your PIN: ').strip()

access_token = auth.get_access_token(verifier)

# = Save Token =
token = access_token.key
tokenSecret = access_token.secret
print (("Access token key:    {:s}\n"
        "Access token secret: {:s}").format(token, tokenSecret))
## or if you already have token
# token = 'your token'
# tokenSecret = 'yourr tokenSecret'
# auth.setToken(token, tokenSecret)


# now you have a workable api
api = API(auth, parser=JSONParser())
# or use `api = API(auth)`
print ("User Infomation:")
I = api.user.info()                     # or api.me()
data = I['data']
print (("Name: {name}\nNick: {nick}\nLocation {location}\n"
        "Email: {email}\n").format(**data))
