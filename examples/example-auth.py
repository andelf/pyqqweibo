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
from qqweibo import API, JSONParser
from qqweibo import OAuth2_0_Handler as AuthHandler
import secret

# for py3k
try:
    input = raw_input
except:
    pass


API_KEY = secret.apiKey
API_SECRET = secret.apiSecret
CALLBACK_URL = secret.callbackUrl

auth = AuthHandler(API_KEY, API_SECRET, CALLBACK_URL)


## use get_authorization_url if you haven't got a token
url = auth.get_authorization_url()
print ('Opening {:s} in your browser...'.format(url))
webbrowser.open_new(url)
verifier = input('Your CODE: ').strip()

token = auth.get_access_token(verifier)

print token
# = Save Token =


# now you have a workable api
api = API(auth, parser=JSONParser())
# or use `api = API(auth)`
print ("User Infomation:")
I = api.user.info()                     # or api.me()
data = I['data']
print (("Name: {name}\nNick: {nick}\nLocation {location}\n"
        "Email: {email}\n").format(**data))
