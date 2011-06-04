#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-timeline.py
#  Author      : Feather.et.ELF <fledna@qq.com>
#  Created     : Fri Apr 08 15:37:46 2011 by Feather.et.ELF
#  Copyright   : andelf <andelf@gmail.com> (c) 2011
#  Description : example file to show how to get timeline
#  Time-stamp: <2011-06-04 11:38:17 andelf>


from __future__ import unicode_literals
import sys
sys.path.insert(0, "..")
import webbrowser

from qqweibo import OAuthHandler, API


API_KEY = 'your key'
API_SECRET = 'your secret'

if API_KEY.startswith('your'):
    print ('You must fill API_KEY and API_SECRET!')
    webbrowser.open("http://open.t.qq.com/apps_index.php")
    raise RuntimeError('You must set API_KEY and API_SECRET')

auth = OAuthHandler(API_KEY, API_SECRET)

token = YOUR TOKEN HERE (so called consumer)
tokenSecret = YOUR TOKEN_SECRET HERE (so called token)

auth.setToken(token, tokenSecret)

api = API(auth)

"""
Avaliable API:
Do to refer api.doc.rst
api.timeline.broadcast
api.timeline.home
api.timeline.mentions
api.timeline.public
api.timeline.special
api.timeline.topic
api.timeline.user
"""

def dumpTweet(t):
    try:
        print ("{0.nick}({0.name}) => {0.origtext} [{0.from_}]".format(t))
        if t.source:
            print ("!Orig: {0.source.origtext}".format(t))
    except UnicodeEncodeError:
        # NOTE: this is a very common error under win32
        print ("Error: Some tweets or usernames may be outside "
               "your system encoding")


for t in api.timeline.home():
    dumpTweet(t)

for retid in api.timeline.homeids():
    t = api.tweet.show(retid.id)
    # or the magic t = retid.as_tweet()
    dumpTweet(t)
    print ("Warning: it may use up your request quota.")
    break

for t in api.timeline.users(names=['andelf', 'karenmo']):
    dumpTweet(t)
