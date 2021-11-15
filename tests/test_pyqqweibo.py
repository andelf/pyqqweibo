#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : test_pyqqweibo.py
#  Author      : Feather.et.ELF <fledna@qq.com>
#  Created     : Wed Jun 08 10:20:57 2011 by Feather.et.ELF
#  Copyright   : Feather Workshop (c) 2011
#  Description : testcast
#  Time-stamp: <2011-06-09 22:18:47 andelf>

from __future__ import unicode_literals
from __future__ import print_function

import sys
import time
from random import randint
import unittest

sys.path.insert(0, '..')
from qqweibo import *
from qqweibo import models


def contenttype_tester(apifunc, reqnum, contenttype, **kwargs):
    # contenttype: content filter
    # FIXME: type1 | type2 not supported
    if contenttype not in [1, 2, 4, 8, 0x10]:
        return
    ret = apifunc(reqnum=reqnum, contenttype=contenttype, **kwargs)
    if not ret:
        print ('No test for contenttype 0x%x' % contenttype)
        return
    if contenttype & 1:
        # Text
        for t in ret:
            assert bool(t.text)
    if contenttype & 2:
        # LINK
        for t in ret:
            # typically works, because all url will be translated
            # to http://url.cn/somewhat
            assert ('http://' in t.origtext) or \
                   (t.source and ('http://' in t.source.origtext))
    if contenttype & 4:
        # IMAGE
        for t in ret:
            assert t.image or (t.source and t.source.image)
    if contenttype & 8:
        # VIDEO
        # BUG: .video sometimes is None
        for t in ret:
            assert t.video or (t.source and t.source.video) or \
                   (('视频' in t.origtext) or \
                    (t.source and ('视频' in t.source.origtext)))
    if contenttype & 0x10:
        # MUSIC
        for t in ret:
            assert t.music or (t.source and t.source.music)
    return True


def test():
    """This Must Pass"""
    pass


def test_get_access_token():
    """TODO: write later"""
    pass
    #assert access_token.key
    #assert access_token.secret
    #auth.get_authorization_url()
    #print (a.get_authorization_url())
#verifier = raw_input('PIN: ').strip()
#access_token = a.get_access_token(verifier)

#token = access_token.key
#tokenSecret = access_token.secret

#print (access_token.key)
#print (access_token.secret)
#auth.setToken(token, tokenSecret)


class QWeiboTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """generate OAuthHandler"""
        import secret
        #auth = OAuthHandler(secret.apiKey, secret.apiSecret)
        auth = OAuth2_0_Handler(secret.apiKey, secret.apiSecret, secret.callbackUrl)


        auth.access_token = secret.accessToken
        auth.openid = secret.openid
        cls.auth = auth


class MemoryCacheTestCase(QWeiboTestCase):
    def test_MemoryCache(self):
        """MemoryCache"""
        api = API(self.auth, cache=MemoryCache())
        ret = api.timeline.home(reqnum=100)
        startTime = time.time()
        ret2 = api.timeline.home(reqnum=100)
        endTime = time.time()
        self.assertEqual(ret[0].id, ret2[0].id)
        self.assertEqual(ret[-1].id, ret2[-1].id)
        self.assertLess(endTime - startTime, 0.01)


class FileCacheTestCase(QWeiboTestCase):
    def setUp(self):
        #super(FileCacheTestCase, self).setUp()
        import tempfile
        self.tmpdir = tempfile.mkdtemp()

    def test_FileCache(self):
        """FileCache"""
        api = API(self.auth, cache=FileCache(self.tmpdir), )
        ret = api.timeline.public(reqnum=100)
        startTime = time.time()
        ret2 = api.timeline.public(reqnum=100)
        endTime = time.time()
        self.assertEqual(ret[0].id, ret2[0].id)
        self.assertEqual(ret[-1].id, ret2[-1].id)
        self.assertLess(endTime - startTime, 0.1)

    def teardown():
        import shutil
        shutil.rmtree(self.tmpdir)


class ParserTestCase(QWeiboTestCase):
    def test_XMLRawParser(self):
        """XMLRawParser"""
        import xml.dom.minidom
        api = API(self.auth, parser=XMLRawParser())
        ret = api.info.update()
        assert len(ret) > 0
        xml.dom.minidom.parseString(ret)

    def test_XMLDomParser(self):
        """XMLDomParser"""
        api = API(self.auth, parser=XMLDomParser())
        ret = api.user.userinfo('andelf')
        assert hasattr(ret, 'getElementsByTagName')
        assert len(ret.getElementsByTagName('nick')) == 1

    def test_XMLETreeParser(self):
        """XMLETreeParser"""
        api = API(self.auth, parser=XMLETreeParser())
        ret = api.user.userinfo('andelf')
        assert hasattr(ret, 'findtext')
        assert ret.findtext('data/nick')

    def test_ModelParser(self):
        """ModelParser"""
        from qqweibo.models import User
        api = API(self.auth, parser=ModelParser())
        ret = api.user.userinfo('andelf')
        assert type(ret) == User
        assert hasattr(ret, 'name')
        api = API(self.auth)
        ret = api.user.userinfo('andelf')
        assert type(ret) == User

    def test_JSONParser(self):
        """JSONParser"""
        api = API(self.auth, parser=JSONParser())
        ret = api.user.userinfo('andelf')
        assert 'msg' in ret
        assert ret['msg'] == 'ok'
        assert 'data' in ret
        assert 'name' in ret['data']


# === API test ===

class APITestCase(QWeiboTestCase):
    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()
        cls.api = API(cls.auth)


class TimelineAPITestCase(APITestCase):
    def test_home(self):
        """api.timeline.home"""
        api = self.api
        ret = api.timeline.home()
        assert isinstance(ret, list)
        assert len(ret) <= 20
        if len(ret) > 1:
            assert isinstance(ret[0], models.Tweet)

        for ct in [1, 2, 4, 8, 0x10]:
            contenttype_tester(api.timeline.home,
                               reqnum=1,
                               contenttype=ct)

        ret = api.timeline.home(reqnum=100)
        assert len(ret) == 70
        assert ret.hasnext

        num = randint(1, 70)
        ret = api.timeline.home(reqnum=num)
        assert len(ret) == num
        assert ret.hasnext

    def test_public(self):
        """api.timeline.public"""
        api = self.api
        ret = api.timeline.public()
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet

        ret = api.timeline.public()
        assert len(ret) == 20

        ret = api.timeline.public(reqnum=130)
        assert len(ret) == 100

    def test_user(self):
        """api.timeline.user"""
        api = self.api
        ret = api.timeline.user('andelf')
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet
        assert ret[0].name == 'andelf'
        assert ret.hasnext

        for ct in [1, 2, 4, 8, 0x10]:
            contenttype_tester(api.timeline.user,
                                    reqnum=1,
                                    contenttype=ct,
                                    name='andelf')

        ret = api.timeline.user(name='andelf', reqnum=120)
        assert len(ret) == 70
        assert ret.hasnext

        num = randint(1, 70)
        ret = api.timeline.user(name='andelf', reqnum=num)
        assert len(ret) == num
        assert ret.hasnext

    def test_mentions(self):
        """api.timeline.mentions"""
        api = self.api
        ret = api.timeline.mentions()
        username = self.auth.get_username()
        assert 1 < len(ret) <= 20
        assert type(ret[0]) == models.Tweet
        # ugly but works
        # BUG: it also returns retweets of my tweet, no @myusername
        assert (username in ret[0].origtext + ret[0].name) or \
               (ret[0].source and (username in \
                ret[0].source.origtext + ret[0].source.name))

        for ct in [1, 2, 4, 8, 0x10]:
            contenttype_tester(api.timeline.mentions,
                                    reqnum=1,
                                    contenttype=ct)

        ret = api.timeline.mentions(reqnum=120)
        assert len(ret) == 70
        assert ret.hasnext

        ret = api.timeline.mentions(reqnum=64)
        assert len(ret) == 64
        assert ret.hasnext

    def test_topic(self):
        """api.timeline.topic"""
        api = self.api
        ret = api.timeline.topic(httext='这里是辽宁')
        # BUG: 默认为 20, 但大部分情况下即使热门话题, 返回都会少一些
        assert len(ret) <= 20
        assert type(ret[0]) == models.Tweet
        assert '这里是辽宁' in ret[0].origtext
        # BUG: hasnext = 2 not 0
        assert ret.hasnext

        for reqnum in [120, randint(1, 100), randint(1, 100)]:
            ret = api.timeline.topic(httext='毕业', reqnum=reqnum)
            # BUG: this will range from 90 or so to 100
            assert len(ret) <= 100
            # BUG: generally return count will be 0-10 less than reqnum
            assert len(ret) <= reqnum
            assert ret.hasnext
            # NOTE: I don't know why, ask tencent please

    def test_broadcast(self):
        """api.timeline.broadcast"""
        api = self.api
        username = api.user.info().username
        ret = api.timeline.broadcast()
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet
        assert username == ret[0].name

        for ct in [1, 2, 4, 8, 0x10]:
            contenttype_tester(api.timeline.broadcast,
                                    reqnum=1,
                                    contenttype=ct)

        ret = api.timeline.broadcast(reqnum=110)
        assert len(ret) == 70

        num = randint(1, 70)
        ret = api.timeline.broadcast(reqnum=num)
        assert len(ret) == num

    def test_special(self):
        """api.timeline.special"""
        api = self.api
        ret = api.timeline.special()
        assert 1 <= len(ret) <= 20, 'You should add special listen ' \
               'friends to pass this test'
        assert type(ret[0]) == models.Tweet

        ret = api.timeline.special(reqnum=110)
        assert len(ret) == 70

        num = randint(1, 70)
        ret = api.timeline.special(reqnum=num)
        assert len(ret) == num

    def test_area(self):
        """api.timeline.area"""
        api = self.api
        ret = api.timeline.area(country=1, province=44, city=3)
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet
        assert int(ret[0].countrycode) == 1
        assert int(ret[0].provincecode) == 44
        assert int(ret[0].citycode) == 3

        ret = api.timeline.area(country=1, province=44, city=3, reqnum=110)
        assert len(ret) == 100

        num = randint(1, 100)
        ret = api.timeline.area(country=1, province=44, city=3, reqnum=num)
        assert len(ret) == num

    def test_users(self):
        """api.timeline.users"""
        api = self.api
        ret = api.timeline.users(names=['andelf', 'NBA'])
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet
        assert ret[0].name in ['andelf', 'NBA']

        for ct in [1, 2, 4, 8, 0x10]:
            contenttype_tester(api.timeline.users,
                               reqnum=1,
                               contenttype=ct,
                               names=['andelf', 'yinyuetai'])

        # BUG: max reqnum is 40, or Exception raised
        # Update Wed Jun 08 14:35:33 2011:
        # seems fixed
        # Update Wed Jun 08 15:06:24 2011
        # bug again.... 囧rz..
        ret = api.timeline.users(names=['andelf', 'NBA'], reqnum=100)
        assert len(ret) == 70

        num = randint(1, 70)
        ret = api.timeline.users(names=['andelf', 'NBA'], reqnum=num)
        assert len(ret) == num

    def test_homeids(self):
        """api.timeline.homeids"""
        api = self.api
        ret = api.timeline.homeids()
        assert len(ret) == 20
        assert type(ret[0]) == models.RetId
        assert hasattr(ret[0], 'id')
        assert hasattr(ret[0], 'timestamp')

        ret = api.timeline.homeids(reqnum=310)
        assert len(ret) == 300

        num = randint(1, 300)
        ret = api.timeline.homeids(reqnum=num)
        assert len(ret) == num

    def test_userids(self):
        """api.timeline.userids"""
        api = self.api
        ret = api.timeline.userids('andelf')
        assert len(ret) == 20
        assert type(ret[0]) == models.RetId
        assert hasattr(ret[0], 'id')
        assert hasattr(ret[0], 'timestamp')

        # use 腾讯薇薇
        # BUG: return count is less than reqnum
        # and it is not a linear relation..... max 210
        # for e.g. :
        # 60 => 60, 70 => 70, 80 => 70, 90 => 70, 100 => 70
        # 110 => 80, 120 => 90, ... 260 => 200, 181 => 140
        # 141 => 111
        ret = api.timeline.userids(name='t', reqnum=300)
        assert len(ret) == 210

        num = randint(1, 210)
        ret = api.timeline.userids(name='t', reqnum=num)
        assert len(ret) <= num

    def test_broadcastids(self):
        """api.timeline.broadcastids"""
        api = self.api
        ret = api.timeline.broadcastids()
        assert len(ret) == 20
        assert type(ret[0]) == models.RetId
        assert hasattr(ret[0], 'id')
        assert hasattr(ret[0], 'timestamp')

        # BUG: same bug as api.timeline.userids
        ret = api.timeline.broadcastids(reqnum=310)
        assert len(ret) == 210

        num = randint(1, 300)
        ret = api.timeline.broadcastids(reqnum=num)
        assert len(ret) <= num

    def test_mentionsids(self):
        """api.timeline.mentionsids"""
        api = self.api
        ret = api.timeline.mentionsids()
        assert len(ret) == 20
        assert type(ret[0]) == models.RetId
        assert hasattr(ret[0], 'id')
        assert hasattr(ret[0], 'timestamp')

        # BUG: same bug as api.timestamp.userids
        ret = api.timeline.mentionsids(reqnum=300)
        assert len(ret) <= 210

        num = randint(1, 300)
        ret = api.timeline.mentionsids(reqnum=num)
        assert len(ret) <= num

    def test_usersids(self):
        """api.timeline.usersids"""
        api = self.api
        ret = api.timeline.usersids(['andelf', 't', 'NBA'])
        assert len(ret) == 20
        assert type(ret[0]) == models.RetId
        assert hasattr(ret[0], 'id')
        assert hasattr(ret[0], 'timestamp')

        ret = api.timeline.usersids(names=['andelf', 't', 'NBA'], reqnum=310)
        assert len(ret) == 300

        num = randint(1, 300)
        ret = api.timeline.usersids(names=['andelf', 't', 'NBA'], reqnum=num)
        assert len(ret) == num

# part 2
test_ids = []


class TweetAPITestCase(APITestCase):
    def test_show(self):
        """api.tweet.show"""
        api = self.api
        id = api.timeline.homeids(reqnum=1)[0].id
        ret = api.tweet.show(id)
        assert type(ret) == models.Tweet
        assert ret.id == id

    def test_add(self):
        """api.tweet.add"""
        api = self.api
        ret = api.tweet.add("#pyqqweibo# unittest auto post."
                            "will be delete later %d" % randint(0, 100),
                            clientip='127.0.0.1',
                            jing=123.422889,
                            wei=41.76627
                            )
        assert type(ret) == models.RetId
        assert hasattr(ret, 'id')
        assert hasattr(ret, 'timestamp')
        test_ids.append(ret.id)

        t = ret.as_tweet()              # also show
        assert t.id == ret.id
        assert 'pyqqweibo' in t.origtext
        assert t.type == 1
        # not implemented yet
        assert not bool(t.geo)

    def test_delete(self):
        """api.tweet.delete"""
        # delete in others
        pass

    def test_retweet(self):
        """api.tweet.retweet"""
        api = self.api
        target_id = test_ids[0]
        ret = api.tweet.retweet(reid=target_id,
                                content="test retweet %d" % randint(0, 100),
                                clientip='127.0.0.1'
                                )
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert t.id == ret.id
        assert t.source.id == target_id
        assert t.type == 2
        assert 'retweet' in t.origtext

    def test_reply(self):
        """api.tweet.reply"""
        api = self.api
        target_id = test_ids[0]
        ret = api.tweet.reply(reid=target_id,
                              content="测试回复 %d" % randint(0, 100),
                              clientip='127.0.0.1'
                              )
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert t.id == ret.id
        assert t.source.id == target_id
        assert t.type == 4
        assert '回复' in t.origtext

    def test_addpic(self):
        """api.tweet.addpic"""
        api = self.api
        ret = api.tweet.addpic("f:/tutu.jpg",
                               "TOO~~~",
                               '127.0.0.1')
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert hasattr(t, 'image')
        assert len(t.image) == 1
        assert 'TOO' in t.origtext

    def test_retweetcount(self):
        """apt.tweet.retweetcount"""
        api = self.api
        ret = api.tweet.retweetcount(ids=[79504073889068,
                                          36575045593232])
        assert type(ret) == models.JSON
        data = ret.as_dict()
        assert '79504073889068' in data
        count = data['79504073889068']
        assert count > 0

        ret0 = api.tweet.retweetcount(ids=79504073889068,
                                     flag=0)
        count0 = ret0.as_dict()['79504073889068']
        assert count0 > 0
        # in some seconds
        assert count0 - 10 <= count <= count0

        ret1 = api.tweet.retweetcount(ids=79504073889068,
                                     flag=1)
        count1 = ret1.as_dict()['79504073889068']
        assert count1 > 0

        ret2 = api.tweet.retweetcount(ids=79504073889068,
                                     flag=2)
        count2 = ret2.as_dict()['79504073889068']
        # {u'count': 16511, u'mcount': 294}
        assert 'count' in count2
        assert 'mcount' in count2

        assert count2['count'] - 5 <= count <= count2['count']
        assert count2['mcount'] - 5 <= count1 <= count2['mcount']

    def test_retweetlist(self):
        """api.tweet.retweetlist"""
        api = self.api
        ret = api.tweet.retweetlist(rootid='79504073889068')
        assert len(ret) == 20
        assert type(ret[0]) == models.Tweet
        assert ret[0].source.id == '79504073889068'
        assert ret.hasnext

        ret = api.tweet.retweetlist(rootid='79504073889068',
                                    reqnum=120)
        assert len(ret) == 100

        num = randint(1, 100)
        ret = api.tweet.retweetlist(rootid='79504073889068',
                                    reqnum=num)
        assert len(ret) == num

    def test_comment(self):
        """api.tweet.comment"""
        api = self.api
        target_id = test_ids[0]
        ret = api.tweet.comment(reid=target_id,
                                content="测试评论 %d" % randint(0, 100),
                                clientip='127.0.0.1'
                                )
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert t.id == ret.id
        assert t.source.id == target_id
        assert t.type == 7
        assert '评论' in t.origtext

    def test_addmusic(self):
        """api.tweet.addmusic"""
        return
        api = self.api
        ret = api.tweet.addmusic(url='',
                                 title='',
                                 author='',
                                 content='Song',
                                 clientip='127.0.0.1')
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert hasattr(t, 'music')
        assert bool(t.music)
        assert 'Song' in t.origtext

    def test_addvideo(self):
        """api.tweet.addvideo"""
        return
        api = self.api
        ret = api.tweet.addvideo(url='',
                                 content='Video',
                                 clientip='127.0.0.1')
        assert type(ret) == models.RetId
        test_ids.append(ret.id)

        t = ret.as_tweet()
        assert hasattr(t, 'video')
        assert bool(t.video)
        assert type(t.video) == models.Video
        assert 'Video' in t.origtext

    def test_list(self):
        """api.tweet.list"""
        api = self.api
        ret = api.tweet.list(ids=[79504073889068,
                                  36575045593232])
        assert len(ret) == 2
        assert type(ret[0]) == models.Tweet

        assert not ret.hasnext

        for t in ret:
            assert t.id in ['79504073889068', '36575045593232']


class UserAPITestCase(APITestCase):
    def test_info(self):
        """api.user.info"""
        api = self.api
        ret = api.user.info()
        assert type(ret) == models.User

    def test_update(self):
        """api.user.update"""
        api = self.api
        ret = api.user.info()
        old_intro = ret.introduction

        ret.introduction = '#pyqqweibo# powered!'
        ret.update()                    # use model interface
        ret = api.user.info()

        assert ret.introduction == '#pyqqweibo# powered!'
        ret.introduction = old_intro
        ret.update()

    def test_updatehead(self):
        """api.user.updatehead"""
        # TODO: implement this
        api = self.api

    def test_userinfo(self):
        """api.user.userinfo"""
        api = self.api
        ret = api.user.userinfo(name='t')
        assert type(ret) == models.User
        assert ret.name == 't'

class FriendsAPITestCase(APITestCase):
    def test_fanslist(self):
        """api.friends.fanslist"""
        api = self.api
        ret = api.friends.fanslist()
        assert len(ret) == 30
        assert type(ret[0]) == models.User
        assert ret.hasnext

        fansnum  = api.user.info().fansnum
        ret = api.friends.fanslist(startindex=fansnum-1)
        assert not ret.hasnext

        ret = api.friends.fanslist(reqnum=100)
        assert len(ret) == 30

        num = randint(1, 30)
        ret = api.friends.fanslist(reqnum=num)
        assert len(ret) == num

    def test_idollist(self):
        """api.friends.idollist"""
        api = self.api
        ret = api.friends.idollist()
        assert len(ret) == 30
        assert type(ret[0]) == models.User
        assert ret.hasnext

        idolnum  = api.user.info().idolnum
        ret = api.friends.idollist(startindex=idolnum-1)
        assert not ret.hasnext

        ret = api.friends.idollist(reqnum=100)
        assert len(ret) == 30

        num = randint(1, 30)
        ret = api.friends.idollist(reqnum=num)
        assert len(ret) == num

    def test_blacklist(self):
        """api.friends.blacklist"""
        api = self.api
        ret = api.friends.blacklist()
        assert len(ret) > 0, "add someone to blacklist to pass test"
        assert type(ret[0]) == models.User

    def test_speciallist(self):
        """api.friends.speciallist"""
        api = self.api
        ret = api.friends.speciallist()
        assert len(ret) > 0, "add someone to special list to pass test"
        assert type(ret[0]) == models.User

    def test_add(self):
        """api.friends.add"""
        api = self.api
        ret = api.friends.add(name='fledna')
        assert ret is None

        info = api.user.userinfo(name='fledna')
        assert info.ismyidol

    def test_delete(self):
        """api.friends.delete"""
        api = self.api
        ret = api.friends.delete(name='t')
        assert ret is None

        info = api.user.userinfo(name='t')
        assert not info.ismyidol

        try:
            # BUG: will cause errcode=65. reason unknown
            api.friends.add(name='t')
        except:
            pass

    def test_addspecial(self):
        """api.friends.addspecial"""
        api = self.api
        ret = api.friends.addspecial('t')
        assert ret is None

    def test_deletespecial(self):
        """api.friends.deletespecial"""
        api = self.api
        try:
            ret = api.friends.add('t')
            ret = api.friends.addspecial('t')
        except:
            pass
        ret = api.friends.deletespecial('t')
        assert ret is None

    def test_addblacklist(self):
        """api.friends.addblacklist"""
        api = self.api
        ret = api.friends.addblacklist(name='t')
        assert ret is None

        info = api.user.userinfo(name='t')
        assert info.ismyblack

    def test_deleteblacklist(self):
        """api.friends.deleteblacklist"""
        api = self.api
        ret = api.friends.deleteblacklist(name='t')
        assert ret is None

        info = api.user.userinfo(name='t')
        assert not info.ismyblack

    def test_check(self):
        """self.friends.check"""
        api = self.api
        ret = api.friends.check(names=['t', 'andelf', 'NBA'])
        assert type(ret) == models.JSON

        assert type(ret.t) == bool
        assert type(ret.as_dict()['andelf']) == bool

    def test_userfanslist(self):
        """api.friends.userfanslist"""
        api = self.api
        ret = api.friends.userfanslist('NBA')
        assert len(ret) == 30
        assert type(ret[0]) == models.User
        assert ret.hasnext

        # BUG: if too large, cause ret=4, errcode=0
        fansnum  = api.user.userinfo('NBA').fansnum
        ret = api.friends.userfanslist('NBA', startindex=fansnum-1)
        assert not ret.hasnext

        ret = api.friends.userfanslist('NBA', reqnum=100)
        assert len(ret) == 30

        num = randint(1, 30)
        ret = api.friends.userfanslist('NBA', reqnum=num)
        assert len(ret) == num

    def test_useridollist(self):
        """api.friends.useridollist"""
        api = self.api
        ret = api.friends.useridollist('andelf')
        assert len(ret) == 30
        assert type(ret[0]) == models.User
        assert ret.hasnext

        idolnum  = api.user.userinfo('andelf').idolnum
        ret = api.friends.useridollist('andelf', startindex=idolnum-1)
        assert not ret.hasnext

        ret = api.friends.useridollist('andelf', reqnum=100)
        assert len(ret) == 30

        num = randint(1, 30)
        ret = api.friends.useridollist('andelf', reqnum=num)
        assert len(ret) == num

    def test_userspeciallist(self):
        """api.friends.userspeciallist"""
        api = self.api

        ret = api.friends.useridollist('andelf')
        assert len(ret) > 0
        assert type(ret[0]) == models.User
        if len(ret)< 30:
            assert not ret.hasnext



if __name__ == '__main__':
    unittest.main(verbosity=2)
    #suite = unittest.TestLoader().loadTestsFromTestCase(FriendsAPITestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)

if 1:
    print ('\nbegin clean up...')
    APITestCase.setUpClass()
    for i in test_ids:
        ret = APITestCase.api.tweet.delete(i)
        print ('delete id={}'.format(i))
        assert ret.id == i
