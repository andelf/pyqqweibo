#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-user.py
#  Author      : Feather.et.ELF <andelf@gmail.com>
#  Created     : Fri Apr 08 16:53:09 2011 by Feather.et.ELF
#  Copyright   : andelf <andelf@gmail.com> (c) 2011
#  Description : example to show how to use user api
#  Time-stamp: <2011-06-04 11:39:06 andelf>


import sys
sys.path.insert(0, "..")
import webbrowser

from qqweibo import API
from qqweibo import OAuth2_0_Handler as AuthHandler

API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print ('You must fill API_KEY and API_SECRET!')
    webbrowser.open("http://open.t.qq.com/apps_index.php")
    raise RuntimeError('You must set API_KEY and API_SECRET')

CALLBACK_URL = 'http://fledna.duapp.com/query'

auth = AuthHandler(API_KEY, API_SECRET, CALLBACK_URL)


token = YOUR TOKEN HERE
tokenSecret = YOUR TOKEN_SECRET HERE

auth.setToken(token, tokenSecret)

# this time we use ModelParser()
api = API(auth)  # ModelParser is the default option


"""
Avaliable API:
Do to refer api.doc.rst
api.user.info
api.user.otherinfo
api.user.update
api.user.updatehead
api.user.userinfo
"""

me = api.user.info()

print (("Name: {0.name}\nNick: {0.nick}\nLocation {0.location}\n"
        "Email: {0.email}\nIntro: {0.introduction}").format(me))

print (me.self)                           # is this user myself?

me.introduction = 'modify from pyqqweibo!!!'
me.update()                             # update infomation

me = api.user.info()
print (me.introduction)

api.user.updatehead('/path/to/your/head/img.fmt')

ret = api.user.otherinfo('NBA')

print (ret.verifyinfo)

for t in ret.timeline(reqnum=3):
    print (t.text)
