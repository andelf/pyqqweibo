#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-tweet.py
#  Author      : Feather.et.ELF <andelf@gmail.com>
#  Created     : Fri Apr 08 15:44:25 2011 by Feather.et.ELF
#  Copyright   : andelf <andelf@gmail.com> (c) 2011
#  Description : example to show how to post or del
#  Time-stamp: <2011-06-04 11:38:34 andelf>


from __future__ import unicode_literals
import sys
sys.path.insert(0, "..")
import webbrowser

from qqweibo import OAuthHandler, API, ModelParser


API_KEY = 'your key'
API_SECRET = 'your secret'


if API_KEY.startswith('your'):
    print ('You must fill API_KEY and API_SECRET!')
    webbrowser.open("http://open.t.qq.com/apps_index.php")
    raise RuntimeError('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)

token = 'your token'
tokenSecret = 'yourr tokenSecret'

auth.setToken(token, tokenSecret)

# this time we use ModelParser()
api = API(auth, parser=ModelParser())


"""
Avaliable API:
Do to refer api.doc.rst
api.tweet.add
api.tweet.addmusic
api.tweet.addpic
api.tweet.addvideo
api.tweet.comment
api.tweet.delete
api.tweet.getvideoinfo
api.tweet.reply
"""

# you must use unicode object here
sent = []
ret = api.tweet.add('测试发帖....本帖来自 #pyqqweibo#.', clientip='127.0.0.1')
print (ret)
sent.append(ret.id)

tw = api.tweet.show(ret.id)
print ('id={0.id} nick={0.nick} text={0.text}'.format(tw))

ret = tw.reply('测试自回复')           # 作为对话显示
sent.append(ret.id)

ret = tw.retweet('测试自转发')
sent.append(ret.id)

ret = tw.comment('测试评论')
sent.append(ret.id)

for id in sent:
    print ("Uncomment to delete")
    #api.tweet.delete(id)
    # or api.tweet.show(id).delete()
