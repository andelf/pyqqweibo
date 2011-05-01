#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-tweet.py 
#  Author      : Feather.et.ELF <andelf@gmail.com> 
#  Created     : Fri Apr 08 15:44:25 2011 by Feather.et.ELF 
#  Copyright   : andelf <andelf@gmail.com> (c) 2011 
#  Description : example to show how to post or del
#  Time-stamp: <2011-04-21 14:18:52 andelf> 


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
api = API(auth, parser=ModelParser())


"""
Avaliable API:
api.t.add
api.t.addmusic
api.t.addpic
api.t.addvideo
api.t.comment
api.t.delete
api.t.getvideoinfo
api.t.reply
api.t.retweet
api.t.retweets
api.t.show
"""

# you must use unicode object here
sent = []
ret = api.t.add(u'测试发帖....本帖来自 pyqqweibo.', clientip='127.0.0.1')
print ret.id
sent.append(ret.id)

tw = api.t.show(ret.id)
print tw.id, tw.nick, tw.text

ret = tw.reply(u'测试自回复')           # 作为对话显示
sent.append(ret.id)

ret = tw.retweet(u'测试自转发')
sent.append(ret.id)

ret = tw.comment(u'测试评论')
send.append(ret.id)

for id in send:
    api.t.delete(id)
    # or api.t.show(id).delete()
