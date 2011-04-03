#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf<andelf@gmail.com>
# See LICENSE for details.

import os
import mimetypes

from binder import bind_api
from error import WeibopError
from parsers import ModelParser


class API(object):
    """Weibo API"""

    def __init__(self, auth_handler=None,
            host='open.t.qq.com', search_host='open.t.qq.com',
            cache=None, secure=False, api_root='', search_root='',
            retry_count=0, retry_delay=0, retry_errors=None,source=None,
            parser=None, log = None):
        self.auth = auth_handler
        self.host = host
        #if source == None:
        #    if auth_handler != None:
        #        self.source = self.auth._consumer.key
        #else:
        #    self.source = source
        self.search_host = search_host
        self.api_root = api_root
        self.search_root = search_root
        self.cache = cache
        self.secure = secure
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or ModelParser()
        self.log = log

    ## 时间线 ##
    """ 1.Statuses/home_timeline 主页时间线 """
    home_timeline = bind_api(
        path = '/api/statuses/home_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    """ 2.Statuses/public_timeline 广播大厅时间线"""
    public_timeline = bind_api(
        path = '/api/statuses/public_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pos', 'reqnum'],
        require_auth = True
    )

    """ 3.Statuses/user_timeline 其他用户发表时间线"""
    user_timeline = bind_api(
        path = '/api/statuses/user_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pageflag', 'pagetime', 'reqnum',
                         'lastid', 'name'],
        require_auth = True
    )

    """ 4.Statuses/mentions_timeline @提到我的时间线 """
    mentions_timeline = bind_api(
        path = '/api/statuses/mentions_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    """ 5.Statuses/ht_timeline 话题时间线 """
    ht_timeline = bind_api(
        path = '/api/statuses/ht_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'httext', 'pageflag', 'pageinfo',
                         'reqnum'],
        require_auth = True
    )
    # 个人很鄙视 ht_....
    topic_timeline = ht_timeline

    """ 6.Statuses/broadcast_timeline 我发表时间线 """
    broadcast_timeline = bind_api(
        path = '/api/statuses/broadcast_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    """ 7.Statuses/special_timeline 特别收听的人发表时间线 """
    special_timeline = bind_api(
        path = '/api/statuses/special_timeline',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    ## 微博相关 ##
    """ 1.t/show 获取一条微博数据 """
    show = bind_api(
        path = '/api/t/show',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'id'],
        require_auth = True
    )

    """ 2.t/add 发表一条微博 """
    add = bind_api(
        path = '/api/t/add',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip',
                         'jing', 'wei'],
        require_auth = True
    )

    """ 3.t/del 删除一条微博 """
    delete = bind_api(                  # del cofilicts with del in python
        path = '/api/t/del',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'id'],
        require_auth = True
    )

    """ 4.t/re_add 转播一条微博 """
    re_add = bind_api(
        path = '/api/t/re_add',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 5.t/reply 回复一条微博 """
    reply = bind_api(
        path = '/api/t/reply',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 6.t/add_pic 发表一条带图片的微博 """
    # add_pic = bind_api(
    #     path = '/api/t/add_pic',
    #     method = 'POST',
    #     payload_type = 'status', payload_list = True,
    #     allowed_param = ['format', 'content', 'clientip',
    #                      'jing', 'wei', 'pic'],
    #     require_auth = True
    # )
    def add_pic(self, filename, content, clientip, jing=None, wei=None):
        headers, post_data = API._pack_image(filename, 1024, content=content, clientip=clientip, jing=jing, wei=wei, contentname="pic")
        args = [content, clientip]
        allowed_param = ['content', 'clientip']
        
        if jing is not None:
            args.append(jing)
            allowed_param.append('jing')
        
        if wei is not None:
            args.append(wei)
            allowed_param.append('wei')
        
        return bind_api(
            path = '/api/t/add_pic',
            method = 'POST',
            payload_type = 'status',
            require_auth = True,
            allowed_param = allowed_param            
            )(self, *args, post_data=post_data, headers=headers)


    """ 7.t/re_count 转播数或点评数 """ # FIXME
    re_count = bind_api(
        path = '/api/t/re_count',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'ids', 'flag'],
        require_auth = True
    )

    """ 8.t/re_list 获取单条微博的转发或点评列表 """ # TODO: test
    re_list = bind_api(
        path = '/api/t/re_list',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'flag', 'rootid', 'pageflag', 'pagetime',
                         'reqnum', 'twitterid',],
        require_auth = True
    )

    """ 9.t/comment 点评一条微博 """
    comment = bind_api(
        path = '/api/t/comment',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip', 'jing', 'wei',
                         'reid'],
        require_auth = True
    )

    """ 10.t/add_music发表音乐微博 """
    add_music = bind_api(
        path = '/api/t/add_music',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip', 'jing', 'wei',
                         'url', 'title', 'author'],
        require_auth = True
    )

    """ 11.t/add_video发表视频微博 """
    add_video = bind_api(
        path = '/api/t/add_video',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'content', 'clientip', 'jing', 'wei',
                         'url'], # supports: youku,tudou,ku6
        require_auth = True
    )
    
    """ 12.t/getvideoinfo 获取视频信息 """
    getvideoinfo = bind_api(
        path = '/api/t/getvideoinfo',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'url'], # supports: youku,tudou,ku6
        require_auth = True
    )


    ## 帐户相关 ##
    """ 1.User/info获取自己的详细资料 """
    info = bind_api(
        path = '/api/user/info',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format',],
        require_auth = True
    )

    """ 2.user/update 更新用户信息 """
    update = bind_api(
        path = '/api/user/update',
        method = 'POST',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'nick', 'sex', 'year', 'month',
                         'day', 'countrycode', 'provincecode',
                         'citycode', 'introduction'],
        require_auth = True
    )

    """ 3.user/update_head 更新用户头像信息 """
    def update_head(self, filename):
        headers, post_data = API._pack_image(filename, 1024, contentname="pic")
        args = []
        allowed_param = []
        
        return bind_api(
            path = '/api/user/update_head',
            method = 'POST',
            payload_type = 'status',
            require_auth = True,
            allowed_param = allowed_param            
            )(self, *args, post_data=post_data, headers=headers)

    """ 4.user/other_info 获取其他人资料 """
    other_info = bind_api(
        path = '/api/user/other_info',
        payload_type = 'status', payload_list = True,
        allowed_param = ['format', 'name'],
        require_auth = True
    )



    ####################
    
    """ status """
    comment_destroy  = bind_api(
        path = '/statuses/comment_destroy/{id}.json',
        method = 'POST',
        payload_type = 'comments',
        allowed_param = ['id'],
        require_auth = True
    )
    
    """ statuses/comments_timeline """
    comments = bind_api(
        path = '/statuses/comments.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/comments_timeline """
    comments_timeline = bind_api(
        path = '/statuses/comments_timeline.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/comments_by_me """
    comments_by_me = bind_api(
        path = '/statuses/comments_by_me.json',
        payload_type = 'comments', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    
    """ statuses/user_timeline """
    user_timeline = bind_api(
        path = '/statuses/user_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'since_id',
                          'max_id', 'count', 'page']
    )


    """ statuses/counts """
    counts = bind_api(
        path = '/statuses/counts.json',
        payload_type = 'counts', payload_list = True,
        allowed_param = ['ids'],
        require_auth = True
    )
    
    """ statuses/unread """
    unread = bind_api(
        path = '/statuses/unread.json',
        payload_type = 'counts'
    )
    
    """ statuses/retweeted_by_me """
    retweeted_by_me = bind_api(
        path = '/statuses/retweeted_by_me.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/retweeted_to_me """
    retweeted_to_me = bind_api(
        path = '/statuses/retweeted_to_me.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/retweets_of_me """
    retweets_of_me = bind_api(
        path = '/statuses/retweets_of_me.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ statuses/show """
    get_status = bind_api(
        path = '/statuses/show.json',
        payload_type = 'status',
        allowed_param = ['id']
    )

    """ statuses/update """
    update_status = bind_api(
        path = '/statuses/update.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['status', 'lat', 'long', 'source'],
        require_auth = True
    )
    """ statuses/upload """
    def upload(self, filename, status, lat=None, long=None, source=None):
        if source is None:
            source=self.source
        headers, post_data = API._pack_image(filename, 1024, source=source, status=status, lat=lat, long=long, contentname="pic")
        args = [status]
        allowed_param = ['status']
        
        if lat is not None:
            args.append(lat)
            allowed_param.append('lat')
        
        if long is not None:
            args.append(long)
            allowed_param.append('long')
        
        if source is not None:
            args.append(source)
            allowed_param.append('source')
        return bind_api(
            path = '/statuses/upload.json',            
            method = 'POST',
            payload_type = 'status',
            require_auth = True,
            allowed_param = allowed_param            
        )(self, *args, post_data=post_data, headers=headers)
        
    """ statuses/reply """
    reply = bind_api(
        path = '/statuses/reply.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id', 'cid','comment'],
        require_auth = True
    )
    
    """ statuses/repost """
    repost = bind_api(
        path = '/statuses/repost.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id', 'status'],
        require_auth = True
    )
    
    """ statuses/destroy """
    destroy_status = bind_api(
        path = '/statuses/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ statuses/retweet """
    retweet = bind_api(
        path = '/statuses/retweet/{id}.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ statuses/retweets """
    retweets = bind_api(
        path = '/statuses/retweets/{id}.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'count'],
        require_auth = True
    )

    """ users/show """
    get_user = bind_api(
        path = '/users/show.json',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name']
    )
    
    """ Get the authenticated user """
    def me(self):
        return self.get_user(screen_name=self.auth.get_username())

    """ users/search """
    search_users = bind_api(
        path = '/users/search.json',
        payload_type = 'user', payload_list = True,
        require_auth = True,
        allowed_param = ['q', 'per_page', 'page']
    )

    """ statuses/friends """
    friends = bind_api(
        path = '/statuses/friends.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'page', 'cursor']
    )

    """ statuses/followers """
    followers = bind_api(
        path = '/statuses/followers.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'page', 'cursor']
    )

    """ direct_messages """
    direct_messages = bind_api(
        path = '/direct_messages.json',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )

    """ direct_messages/sent """
    sent_direct_messages = bind_api(
        path = '/direct_messages/sent.json',
        payload_type = 'direct_message', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page'],
        require_auth = True
    )
    """ direct_messages/new """
    new_direct_message = bind_api(
        path = '/direct_messages/new.json',
        method = 'POST',
        payload_type = 'direct_message',
        allowed_param = ['id', 'screen_name', 'user_id', 'text'],
        require_auth = True
    )
    
    """ direct_messages/destroy """
    destroy_direct_message = bind_api(
        path = '/direct_messages/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'direct_message',
        allowed_param = ['id'],
        require_auth = True
    )

    """ friendships/create """
    create_friendship = bind_api(
        path = '/friendships/create.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name', 'follow'],
        require_auth = True
    )

    """ friendships/destroy """
    destroy_friendship = bind_api(
        path = '/friendships/destroy.json',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ friendships/exists """
    exists_friendship = bind_api(
        path = '/friendships/exists.json',
        payload_type = 'json',
        allowed_param = ['user_a', 'user_b']
    )

    """ friendships/show """
    show_friendship = bind_api(
        path = '/friendships/show.json',
        payload_type = 'friendship',
        allowed_param = ['source_id', 'source_screen_name',
                          'target_id', 'target_screen_name']
    )

    """ friends/ids """
    friends_ids = bind_api(
        path = '/friends/ids.json',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name', 'cursor', 'count'],
        require_auth = True
    )

    """ followers/ids """
    followers_ids = bind_api(        
        path = '/followers/ids.json',
        payload_type = 'json',
        allowed_param = ['id', 'page'],
    )

    """ account/verify_credentials """
    def verify_credentials(self):
        try:
            return bind_api(
                path = '/account/verify_credentials.json',
                payload_type = 'user',
                require_auth = True
            )(self)
        except WeibopError:
            return False

    """ account/rate_limit_status """
    rate_limit_status = bind_api(
        path = '/account/rate_limit_status.json',
        payload_type = 'json'
    )

    """ account/update_delivery_device """
    set_delivery_device = bind_api(
        path = '/account/update_delivery_device.json',
        method = 'POST',
        allowed_param = ['device'],
        payload_type = 'user',
        require_auth = True
    )

    """ account/update_profile_colors """
    update_profile_colors = bind_api(
        path = '/account/update_profile_colors.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['profile_background_color', 'profile_text_color',
                          'profile_link_color', 'profile_sidebar_fill_color',
                          'profile_sidebar_border_color'],
        require_auth = True
    )
        
    """ account/update_profile_image """
    def update_profile_image(self, filename):
        headers, post_data = API._pack_image(filename=filename, max_size=700, source=self.source)
        return bind_api(
            path = '/account/update_profile_image.json',
            method = 'POST',
            payload_type = 'user',
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile_background_image """
    def update_profile_background_image(self, filename, *args, **kargs):
        headers, post_data = API._pack_image(filename, 800)
        bind_api(
            path = '/account/update_profile_background_image.json',
            method = 'POST',
            payload_type = 'user',
            allowed_param = ['tile'],
            require_auth = True
        )(self, post_data=post_data, headers=headers)

    """ account/update_profile """
    update_profile = bind_api(
        path = '/account/update_profile.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['name', 'url', 'location', 'description'],
        require_auth = True
    )

    """ favorites """
    favorites = bind_api(
        path = '/favorites/{id}.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['id', 'page']
    )

    """ favorites/create """
    create_favorite = bind_api(
        path = '/favorites/create/{id}.json',
        method = 'POST',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ favorites/destroy """
    destroy_favorite = bind_api(
        path = '/favorites/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'status',
        allowed_param = ['id'],
        require_auth = True
    )

    """ notifications/follow """
    enable_notifications = bind_api(
        path = '/notifications/follow.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ notifications/leave """
    disable_notifications = bind_api(
        path = '/notifications/leave.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/create """
    create_block = bind_api(
        path = '/blocks/create.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/destroy """
    destroy_block = bind_api(
        path = '/blocks/destroy.json',
        method = 'DELETE',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ blocks/exists """
    def exists_block(self, *args, **kargs):
        try:
            bind_api(
                path = '/blocks/exists.json',
                allowed_param = ['id', 'user_id', 'screen_name'],
                require_auth = True
            )(self, *args, **kargs)
        except WeibopError:
            return False
        return True

    """ blocks/blocking """
    blocks = bind_api(
        path = '/blocks/blocking.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['page'],
        require_auth = True
    )

    """ blocks/blocking/ids """
    blocks_ids = bind_api(
        path = '/blocks/blocking/ids.json',
        payload_type = 'json',
        require_auth = True
    )

    """ statuses/repost """
    report_spam = bind_api(
        path = '/report_spam.json',
        method = 'POST',
        payload_type = 'user',
        allowed_param = ['id', 'user_id', 'screen_name'],
        require_auth = True
    )

    """ saved_searches """
    saved_searches = bind_api(
        path = '/saved_searches.json',
        payload_type = 'saved_search', payload_list = True,
        require_auth = True
    )

    """ saved_searches/show """
    get_saved_search = bind_api(
        path = '/saved_searches/show/{id}.json',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ saved_searches/create """
    create_saved_search = bind_api(
        path = '/saved_searches/create.json',
        method = 'POST',
        payload_type = 'saved_search',
        allowed_param = ['query'],
        require_auth = True
    )

    """ saved_searches/destroy """
    destroy_saved_search = bind_api(
        path = '/saved_searches/destroy/{id}.json',
        method = 'DELETE',
        payload_type = 'saved_search',
        allowed_param = ['id'],
        require_auth = True
    )

    """ help/test """
    def test(self):
        try:
            bind_api(
                path = '/help/test.json',
            )(self)
        except WeibopError:
            return False
        return True

    def create_list(self, *args, **kargs):
        return bind_api(
            path = '/%s/lists.json' % self.auth.get_username(),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    def destroy_list(self, slug):
        return bind_api(
            path = '/%s/lists/%s.json' % (self.auth.get_username(), slug),
            method = 'DELETE',
            payload_type = 'list',
            require_auth = True
        )(self)

    def update_list(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/lists/%s.json' % (self.auth.get_username(), slug),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['name', 'mode', 'description'],
            require_auth = True
        )(self, *args, **kargs)

    lists = bind_api(
        path = '/{user}/lists.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_memberships = bind_api(
        path = '/{user}/lists/memberships.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    lists_subscriptions = bind_api(
        path = '/{user}/lists/subscriptions.json',
        payload_type = 'list', payload_list = True,
        allowed_param = ['user', 'cursor'],
        require_auth = True
    )

    list_timeline = bind_api(
        path = '/{owner}/lists/{slug}/statuses.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['owner', 'slug', 'since_id', 'max_id', 'count', 'page']
    )

    get_list = bind_api(
        path = '/{owner}/lists/{slug}.json',
        payload_type = 'list',
        allowed_param = ['owner', 'slug']
    )

    def add_list_member(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/%s/members.json' % (self.auth.get_username(), slug),
            method = 'POST',
            payload_type = 'list',
            allowed_param = ['id'],
            require_auth = True
        )(self, *args, **kargs)

    def remove_list_member(self, slug, *args, **kargs):
        return bind_api(
            path = '/%s/%s/members.json' % (self.auth.get_username(), slug),
            method = 'DELETE',
            payload_type = 'list',
            allowed_param = ['id'],
            require_auth = True
        )(self, *args, **kargs)

    list_members = bind_api(
        path = '/{owner}/{slug}/members.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_list_member(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '/%s/%s/members/%s.json' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except WeibopError:
            return False

    subscribe_list = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        method = 'POST',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    unsubscribe_list = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        method = 'DELETE',
        payload_type = 'list',
        allowed_param = ['owner', 'slug'],
        require_auth = True
    )

    list_subscribers = bind_api(
        path = '/{owner}/{slug}/subscribers.json',
        payload_type = 'user', payload_list = True,
        allowed_param = ['owner', 'slug', 'cursor']
    )

    def is_subscribed_list(self, owner, slug, user_id):
        try:
            return bind_api(
                path = '/%s/%s/subscribers/%s.json' % (owner, slug, user_id),
                payload_type = 'user'
            )(self)
        except WeibopError:
            return False

    """ trends/available """
    trends_available = bind_api(
        path = '/trends/available.json',
        payload_type = 'json',
        allowed_param = ['lat', 'long']
    )

    """ trends/location """
    trends_location = bind_api(
        path = '/trends/{woeid}.json',
        payload_type = 'json',
        allowed_param = ['woeid']
    )

    """ search """
    search = bind_api(
        search_api = True,
        path = '/search.json',
        payload_type = 'search_result', payload_list = True,
        allowed_param = ['q', 'lang', 'locale', 'rpp', 'page', 'since_id', 'geocode', 'show_user']
    )
    search.pagination_mode = 'page'

    """ trends """
    trends = bind_api(
        search_api = True,
        path = '/trends.json',
        payload_type = 'json'
    )

    """ trends/current """
    trends_current = bind_api(
        search_api = True,
        path = '/trends/current.json',
        payload_type = 'json',
        allowed_param = ['exclude']
    )

    """ trends/daily """
    trends_daily = bind_api(
        search_api = True,
        path = '/trends/daily.json',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )

    """ trends/weekly """
    trends_weekly = bind_api(
        search_api = True,
        path = '/trends/weekly.json',
        payload_type = 'json',
        allowed_param = ['date', 'exclude']
    )
    """ Internal use only """
    # TODO: more general method
    @staticmethod
    def _pack_image(filename, max_size, content=None, clientip=None, jing=None, wei=None, contentname="image"):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise WeibopError('File is too big, must be less than 700kb.')
        #except os.error, e:
        except os.error:
            raise WeibopError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise WeibopError('Could not determine file type')
        file_type = file_type[0]
        if file_type.split('/')[0] != 'image': # dummy
            raise WeibopError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        fp = open(filename, 'rb')
        BOUNDARY = 'Tw3ePyANDELF'
        body = []
        if content is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="content"')
            body.append('Content-Type: text/plain; charset=UTF-8')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            if isinstance(content, unicode):
                content = content.encode('utf-8')
            body.append(content)
        if clientip is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="clientip"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(clientip)
        if jing is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="jing"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(jing)
        if wei is not None:            
            body.append('--' + BOUNDARY)
            body.append('Content-Disposition: form-data; name="wei"')
            body.append('Content-Type: text/plain; charset=US-ASCII')
            body.append('Content-Transfer-Encoding: 8bit')
            body.append('')
            body.append(wei)
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="'+ contentname +'"; filename="%s"' % filename.encode('utf-8'))
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(fp.read())
        body.append('--' + BOUNDARY + '--')
        body.append('')
        fp.close()        
        body.append('--' + BOUNDARY + '--')
        body.append('')
        body = '\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY,
            'Content-Length': len(body)
        }

        return headers, body


