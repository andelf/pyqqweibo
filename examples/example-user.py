#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-user.py 
#  Author      : Feather.et.ELF <andelf@gmail.com> 
#  Created     : Fri Apr 08 16:53:09 2011 by Feather.et.ELF 
#  Copyright   : andelf <andelf@gmail.com> (c) 2011 
#  Description : example to show how to use user api 
#  Time-stamp: <2011-04-21 14:19:37 andelf> 


import sys
sys.path.insert(0, "..")

from qqweibo.auth import OAuthHandler
from qqweibo.api import API
from qqweibo.parsers import ModelParser

API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print u'必须正确填写 API_KEY 和 API_SECRET'
    raise SystemExit('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)

token = 'your token'
tokenSecret = 'yourr tokenSecret'
auth.setToken(token, tokenSecret)

# this time we use ModelParser()
api = API(auth) # ModelParser is the default option


"""
Avaliable API:
api.user.info
api.user.otherinfo
api.user.update
api.user.updatehead
api.user.userinfo
NOTE:
api.me
api.info
api.user.info
功能相同
"""

me = api.info()

print me.name, me.nick, me.location, me.introduction

print me.self                           # is this user myself?

me.introduction = 'modify from pyqqweibo!!!'
me.update()                             # update infomation

me = api.info()
print me.introduction

api.user.updatehead('/path/to/your/head/img.fmt')

ret = api.user.otherinfo('NBA')

print ret.verifyinfo
for t in ret.timeline(reqnum=3):
    print t.text

