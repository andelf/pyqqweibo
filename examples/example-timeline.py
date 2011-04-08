#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-timeline.py 
#  Author      : Feather.et.ELF <fledna@qq.com> 
#  Created     : Fri Apr 08 15:37:46 2011 by Feather.et.ELF 
#  Copyright   : andelf <andelf@gmail.com> (c) 2011 
#  Description : example file to show how to get timeline 
#  Time-stamp: <2011-04-08 15:51:09 andelf> 


from qqweibo.auth import OAuthHandler
from qqweibo.api import API
from qqweibo.parsers import JSONParser

API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print u'必须正确填写 API_KEY 和 API_SECRET'
    raise SystemExit('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)

token = 'your token'
tokenSecret = 'yourr tokenSecret'
auth.setToken(token, tokenSecret)

api = API(auth, parser=JSONParser())

"""
Avaliable API:
api.timeline.broadcast
api.timeline.home
api.timeline.mentions
api.timeline.public
api.timeline.special
api.timeline.topic
api.timeline.user
"""
def dumpMsg(msgs):
    for t in msgs['data']['info']:
        print t['nick'].encode('gbk', 'ignore'), \
              t['text'].encode('gbk', 'ignore')

dumpMsg( api.timeline.home() )
