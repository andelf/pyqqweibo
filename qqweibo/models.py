#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf<andelf@gmail.com>
# See LICENSE for details.

from utils import parse_datetime, parse_html_value, parse_a_href, \
     parse_search_datetime, unescape_html

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

    @classmethod
    def parse(cls, api, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        """Parse a list of JSON objects into a result set of model instances."""
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
        tweet = cls(api)  # ; __import__('pprint').pprint(json)
        for k, v in json.items():
            if k == 'source':
                source = Source.parse(api, v)
                setattr(tweet, 'source', source)
                #user = User.parse(api, v)
                #setattr(tweet, 'author', user)
                #setattr(tweet, 'user', user)  # DEPRECIATED
            elif k in ('isvip', 'self'):
                setattr(tweet, k, bool(v))
            elif k == 'from':
                setattr(tweet, 'from_', v) # avoid use py keyword
            else:
                setattr(tweet, k, v)
        return tweet

    def delete(self):
        if self.self:
            return self._api.delete(self.id)
        else:
            raise WeibopError("You can't delete others tweet")

    def retweet(self, content, clientip='127.0.0.1', jing=None, wei=None):
        # TODO: add jing, wei
        return self._api.re_add(content, clientip, reid=self.id)

    def reply(self, content, clientip='127.0.0.1', jing=None, wei=None):
        # TODO: add jing, wei
        return self._api.reply(content, clientip, reid=self.id)

    def comment(self, content, clientip='127.0.0.1', jing=None, wei=None):
        return self._api.comment(content, clientip, reid=self.id)
        
    #def retweets(self):
    #    return self._api.retweets(self.id)

    def favorite(self):
        return self._api.create_favorite(self.id)

class Geo(Model):

    @classmethod
    def parse(cls, api, json):
        geo = cls(api)
        if json:                        # may be 0
            for k, v in json.items():
                setattr(geo, k, v)
        return geo

class Source(Model):
    def __repr__(self):
        return '<Source object #%s>' % hex(self)

    @classmethod
    def parse(cls, api, json):
        source = cls(api)
        if json:
            for k, v in json.items():
                if k in ('isvip', 'self'):
                    setattr(source, k, bool(v))
                elif k == 'from':
                    setattr(source, 'from_', v)
                #elif k == 'geo':
                else:
                    setattr(source, k, v)
            return source
        else:
            return None
    
class User(Model):

    def __repr__(self):
        return '<User object #%s>' % self.name # no uid

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
            elif k == 'tweet':
                tweet = Tweet.parse_list(api, v) # only 1 item
                setattr(user, k, tweet[0] if tweet else tweet)
            else:
                setattr(user, k, v)

        # FIXME, need better way
        if hasattr(user, 'ismyidol'):
            setattr(user, 'self', False) # is this myself?
        else:
            setattr(user, 'self', True)
        
        return user

    def update(self, **kwargs):
        assert bool(self.self), "you can only update youself's profile"
        nick = self.nick =  kwargs.get('nick', self.nick)
        sex = self.sex = kwargs.get('sex', self.sex)
        year = self.birth_year = kwargs.get('year', self.birth_year)
        month = self.birth_month = kwargs.get('month', self.birth_month)
        day = self.birth_day = kwargs.get('day', self.birth_day)
        countrycode = self.country_code = kwargs.get('countrycode', self.country_code)
        provincecode = self.province_code = kwargs.get('provincecode', self.province_code)
        citycode = self.city_code = kwargs.get('citycode', self.city_code)
        introduction = self.introduction = kwargs.get('introduction', self.introduction)
        self._api.update(nick, sex, year, month, day,
                         countrycode, provincecode, citycode, introduction)

    def timeline(self, **kargs):
        return self._api.user_timeline(name=self.name, **kargs)

#    def friends(self, **kargs):
#        return self._api.friends(user_id=self.id, **kargs)

 #   def followers(self, **kargs):
 #       return self._api.followers(user_id=self.id, **kargs)

    def follow(self):
        assert not bool(self.self), "you can't follow your self"
        if self.ismyidol:
            return                      # already flollowed
        else:
            self._api.add(name=self.name)

    add = flollow
    def unfollow(self):
        assert not bool(self.self), "you can't unfollow your self"
        if self.ismyidol:
            self._api.del_(name=self.name)
        else:
            pass
    del_ = unfollow

        
        
    def lists_subscriptions(self, *args, **kargs):
        return self._api.lists_subscriptions(user=self.screen_name, *args, **kargs)

    def lists(self, *args, **kargs):
        return self._api.lists(user=self.screen_name, *args, **kargs)

    def followers_ids(self, *args, **kargs):
        return self._api.followers_ids(user_id=self.id, *args, **kargs)

class DirectMessage(Model):
    @classmethod
    def parse(cls, api, json):
        dm = cls(api)
        for k, v in json.items():
            if k == 'sender' or k == 'recipient':
                setattr(dm, k, User.parse(api, v))
            elif k == 'created_at':
                setattr(dm, k, parse_datetime(v))
            else:
                setattr(dm, k, v)
        return dm

class Friendship(Model):

    @classmethod
    def parse(cls, api, json):
       
        source = cls(api)
        for k, v in json['source'].items():
            setattr(source, k, v)

        # parse target
        target = cls(api)
        for k, v in json['target'].items():
            setattr(target, k, v)

        return source, target


class SavedSearch(Model):

    @classmethod
    def parse(cls, api, json):
        ss = cls(api)
        for k, v in json.items():
            if k == 'created_at':
                setattr(ss, k, parse_datetime(v))
            else:
                setattr(ss, k, v)
        return ss

    def destroy(self):
        return self._api.destroy_saved_search(self.id)


class SearchResult(Model):

    @classmethod
    def parse(cls, api, json):
        result = cls()
        for k, v in json.items():
            if k == 'created_at':
                setattr(result, k, parse_search_datetime(v))
            elif k == 'source':
                setattr(result, k, parse_html_value(unescape_html(v)))
            else:
                setattr(result, k, v)
        return result

    @classmethod
    def parse_list(cls, api, json_list, result_set=None):
        results = ResultSet()
        results.max_id = json_list.get('max_id')
        results.since_id = json_list.get('since_id')
        results.refresh_url = json_list.get('refresh_url')
        results.next_page = json_list.get('next_page')
        results.results_per_page = json_list.get('results_per_page')
        results.page = json_list.get('page')
        results.completed_in = json_list.get('completed_in')
        results.query = json_list.get('query')

        for obj in json_list['results']:
            results.append(cls.parse(api, obj))
        return results

class List(Model):

    @classmethod
    def parse(cls, api, json):
        lst = List(api)
        for k,v in json.items():
            if k == 'user':
                setattr(lst, k, User.parse(api, v))
            else:
                setattr(lst, k, v)
        return lst

    @classmethod
    def parse_list(cls, api, json_list, result_set=None):
        results = ResultSet()
        for obj in json_list['lists']:
            results.append(cls.parse(api, obj))
        return results

    def update(self, **kargs):
        return self._api.update_list(self.slug, **kargs)

    def destroy(self):
        return self._api.destroy_list(self.slug)

    def timeline(self, **kargs):
        return self._api.list_timeline(self.user.screen_name, self.slug, **kargs)

    def add_member(self, id):
        return self._api.add_list_member(self.slug, id)

    def remove_member(self, id):
        return self._api.remove_list_member(self.slug, id)

    def members(self, **kargs):
        return self._api.list_members(self.user.screen_name, self.slug, **kargs)

    def is_member(self, id):
        return self._api.is_list_member(self.user.screen_name, self.slug, id)

    def subscribe(self):
        return self._api.subscribe_list(self.user.screen_name, self.slug)

    def unsubscribe(self):
        return self._api.unsubscribe_list(self.user.screen_name, self.slug)

    def subscribers(self, **kargs):
        return self._api.list_subscribers(self.user.screen_name, self.slug, **kargs)

    def is_subscribed(self, id):
        return self._api.is_subscribed_list(self.user.screen_name, self.slug, id)

class JSONModel(Model):

    def __repr__(self):
        return "<%s object #%s>" % (type(self).__name__, self.id)

    @classmethod
    def parse(cls, api, json):
        lst = JSONModel(api)
        for k,v in json.items():
            setattr(lst, k, v)
        return lst

class VideoModel(Model):
    def __repr__(self):
        return "<VideoModel object #%s>" % self.real

    @classmethod
    def parse(cls, api, json):
        lst = VideoModel(api)
        for k,v in json.items():
            setattr(lst, k, v)
        return lst

class TagModel(JSONModel):
    def __repr__(self):
        return '<Tag object #%s>' % self.id

class IDSModel(Model):
    @classmethod
    def parse(cls, api, json):
        ids = IDSModel(api)
        for k, v in json.items():            
            setattr(ids, k, v)
        return ids
    
class Counts(Model):
    @classmethod
    def parse(cls, api, json):
        ids = Counts(api)
        for k, v in json.items():            
            setattr(ids, k, v)
        return ids
    
class ModelFactory(object):
    """
    Used by parsers for creating instances
    of models. You may subclass this factory
    to add your own extended models.
    """

    tweet = Tweet
    user = User
    direct_message = DirectMessage
    friendship = Friendship
    saved_search = SavedSearch
    search_result = SearchResult
    list = List
    video = VideoModel
    json = JSONModel
    ids_list = IDSModel
    counts = Counts
