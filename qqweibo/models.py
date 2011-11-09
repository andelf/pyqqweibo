#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-11-09 10:15:42 wangshuyu>

from qqweibo.utils import (parse_datetime, parse_html_value, parse_a_href,
                           parse_search_datetime, unescape_html)
from qqweibo.error import assertion, QWeiboError


class ResultSet(list):
    """A list like object that holds results from a Twitter API query."""


class Model(object):

    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        del pickle['_api']  # do not pickle the API reference
        return pickle

    def as_dict(self):
        ret = dict(self.__dict__)
        # py3k fixed, in py3k, .keys() will be a dict_keys obj
        for k in list(ret.keys()):
            if k.startswith('_'):
                del ret[k]
            elif k == 'as_dict':
                del ret[k]
        return ret

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """Parse a list of JSON objects into a result set of
        model instances."""
        results = ResultSet()
        if json_list:                   # or return empty ResultSet
            for obj in json_list:
                results.append(cls.parse(api, obj))
        return results


class Tweet(Model):

    def __repr__(self):
        return '<Tweet object #%s>' % (self.id or 'unkownID')

    @classmethod
    def parse(cls, api, json):
        if not json:
            return None
        tweet = cls(api)
        for k, v in json.items():
            if k == 'source':
                source = Tweet.parse(api, v)
                setattr(tweet, 'source', source)
            elif k == 'video':
                video = Video.parse(api, v) if v else None
                setattr(tweet, 'video', video)
            elif k in ('isvip', 'self'):
                setattr(tweet, k, bool(v))
            elif k == 'from':
                setattr(tweet, 'from_', v)  # avoid keyword
            elif k == 'tweetid':
                #setattr(tweet, k, v)
                setattr(tweet, 'id', v)
            elif '_' in k:
                # avoid xxxx_xxxx
                setattr(tweet, k.replace('_', ''), v)
            else:
                setattr(tweet, k, v)
        return tweet

    def delete(self):
        if self.self:
            return self._api.t.delete(self.id)
        else:
            raise QWeiboError("You can't delete others' tweet")

    def retweet(self, content, clientip='127.0.0.1', jing=None, wei=None):
        return self._api.t.retweet(content=content, clientip=clientip,
                                   jing=jing, wei=wei, reid=self.id)

    def reply(self, content, clientip='127.0.0.1', jing=None, wei=None):
        return self._api.t.reply(content=content, clientip=clientip, jing=jing,
                                 wei=wei, reid=self.id)

    def comment(self, content, clientip='127.0.0.1', jing=None, wei=None):
        return self._api.t.comment(content=content, clientip=clientip,
                                   jing=jing, wei=wei, reid=self.id)

    def retweetlist(self, *args, **kwargs):
        return self._api.t.retweetlist(self.id, *args, **kwargs)

    def retweetcount(self, *args, **kwargs):
        return self._api.t.retweetcount(self.id, *args, **kwargs)[str(self.id)]

    def favorite(self, fav=True):
        if fav:
            return self._api.fav.addtweet(self.id)
        else:
            return self.unfavorite()

    def unfavorite(self):
        return self._api.fav.deletetweet(self.id)


class Geo(Model):
    """ current useless"""
    @classmethod
    def parse(cls, api, json):
        geo = cls(api)
        if json:
            for k, v in json.items():
                setattr(geo, k, v)
        return geo


class User(Model):

    def __repr__(self):
        return '<User object #%s>' % self.name

    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        for k, v in json.items():
            if k in ('isvip', 'isent',):
                setattr(user, k, bool(v))
            elif k == 'tag':
                tags = TagModel.parse_list(api, v)
                setattr(user, k, tags)
            elif k in ('Ismyblack', 'Ismyfans', 'Ismyidol'):
                # fix name bug
                setattr(user, k.lower(), bool(v))
            elif k == 'isidol':
                setattr(user, 'ismyidol', bool(v))
            elif '_' in k:
                # avoid xxxx_xxxx
                setattr(user, k.replace('_', ''), v)
            elif k == 'tweet':
                tweet = Tweet.parse_list(api, v)  # only 1 item
                setattr(user, k, tweet[0] if tweet else tweet)
            else:
                setattr(user, k, v)

        # FIXME, need better way
        if hasattr(user, 'ismyidol'):
            setattr(user, 'self', False)  # is this myself?
        else:
            setattr(user, 'self', True)
        # fixture for trends/famouslist
        if hasattr(user, 'account') and not hasattr(user, 'name'):
            setattr(user, 'name', user.account)
        return user

    def update(self, **kwargs):
        assertion(self.self, "you can only update youself's profile")

        nick = self.nick = kwargs.get('nick', self.nick)
        sex = self.sex = kwargs.get('sex', self.sex)
        year = self.birthyear = kwargs.get('year', self.birthyear)
        month = self.birthmonth = kwargs.get('month', self.birthmonth)
        day = self.birthday = kwargs.get('day', self.birthday)
        countrycode = self.countrycode = kwargs.get('countrycode',
                                                    self.countrycode)
        provincecode = self.provincecode = kwargs.get('provincecode',
                                                      self.provincecode)
        citycode = self.citycode = kwargs.get('citycode', self.citycode)
        introduction = self.introduction = kwargs.get('introduction',
                                                      self.introduction)
        self._api.user.update(nick, sex, year, month, day, countrycode,
                              provincecode, citycode, introduction)

    def timeline(self, **kargs):
        return self._api.timeline.user(name=self.name, **kargs)

    def add(self):
        """收听某个用户"""
        assertion(not bool(self.self), "you can't follow your self")
        if self.ismyidol:
            return                      # already flollowed
        else:
            self._api.friends.add(name=self.name)
    follow = add

    def delete(self):
        """取消收听某个用户"""
        assertion(not bool(self.self), "you can't unfollow your self")
        if self.ismyidol:
            self._api.friends.delete(name=self.name)
        else:
            pass
    unfollow = delete

    def addspecial(self):
        """特别收听某个用户"""
        assertion(not bool(self.self), "you can't follow yourself")
        self._api.friends.addspecial(name=self.name)

    def deletespecial(self):
        """取消特别收听某个用户"""
        assertion(not bool(self.self), "you can't follow yourself")
        self._api.friends.deletespecial(name=self.name)

    def addblacklist(self):
        """添加某个用户到黑名单"""
        assertion(not bool(self.self), "you can't block yourself")
        self._api.friends.addblacklist(name=self.name)
    block = addblacklist

    def deleteblacklist(self):
        """从黑名单中删除某个用户"""
        assertion(not bool(self.self), "you can't block yourself")
        self._api.friends.deleteblacklist(name=self.name)
    unblock = deleteblacklist

    def fanslist(self, *args, **kwargs):
        """帐户听众列表, 自己或者别人"""
        if self.self:
            return self._api.friends.fanslist(*args, **kwargs)
        else:
            return self._api.friends.userfanslist(self.name, *args, **kwargs)
    followers = fanslist

    def idollist(self, *args, **kwargs):
        """帐户收听的人列表, 自己或者别人"""
        if self.self:
            return self._api.friends.idollist(*args, **kwargs)
        else:
            return self._api.friends.useridollist(self.name, *args, **kwargs)
    followees = idollist

    def speciallist(self, *args, **kwargs):
        """帐户特别收听的人列表, 自己或者别人"""
        if self.self:
            return self._api.friends.speciallist(*args, **kwargs)
        else:
            return self._api.friends.userspeciallist(self.name, *args, **kwargs)

    def pm(self, content, clientip='127.0.0.1', jing=None, wei=None):
        """发私信"""
        assertion(not bool(self.self), "you can't pm yourself")
        return self._api.private.add(self.name, content, clientip, jing, wei)

    def headimg(self, size=100):
        assertion(size in [20, 30, 40, 50, 100],
                  'size must be one of 20 30 40 50 100')
        return '%s/%s' % (self.head, size)


class JSON(Model):

    def __repr__(self):
        if 'id' in self.__dict__:
            return "<%s object #%s>" % (type(self).__name__, self.id)
        else:
            return object.__repr__(self)

    @classmethod
    def parse(cls, api, json):
        lst = JSON(api)
        for k, v in json.items():
            if k == 'tweetid':
                setattr(lst, k, v)
                setattr(lst, 'id', v)   # make `id` always useable
            else:
                setattr(lst, k, v)
        return lst


class RetId(Model):
    def __repr__(self):
        return "<RetId id:%s>" % self.id

    @classmethod
    def parse(cls, api, json):
        lst = RetId(api)
        for k, v in json.items():
            if k == 'tweetid':
                setattr(lst, k, v)
                setattr(lst, 'id', v)   # make `id` always useable
            elif k == 'time':
                setattr(lst, k, v)
                setattr(lst, 'timestamp', v)
            else:
                setattr(lst, k, v)
        return lst

    def as_tweet(self):
        return self._api.tweet.show(self.id)


class Video(Model):
    def __repr__(self):
        return "<Video object #%s>" % self.realurl

    @classmethod
    def parse(cls, api, json):
        lst = Video(api)
        for k, v in json.items():
            # FIX bug names
            if k == 'real':
                k = 'realurl'
            elif k == 'short':
                k = 'shorturl'
            elif k == 'minipic':
                k = 'picurl'
            setattr(lst, k, v)
        return lst


class TagModel(JSON):
    def __repr__(self):
        return '<Tag object #%s>' % self.id

    @classmethod
    def parse(cls, api, json):
        tag = TagModel(api)
        for k, v in json.items():
                setattr(tag, k, v)
        return tag

    def add(self):
        return self._api.tag.add(self.id)

    def delete(self):
        return self._api.tag.delete(self.id)


class Topic(JSON):
    def __repr__(self):
        return '<Topic object #%s>' % self.id

    @classmethod
    def parse(cls, api, json):
        tag = Topic(api)
        for k, v in json.items():
                setattr(tag, k, v)
        return tag


class ModelFactory(object):
    """
    Used by parsers for creating instances
    of models. You may subclass this factory
    to add your own extended models.
    """

    tweet = Tweet
    user = User
    video = Video
    json = JSON
    retid = RetId
