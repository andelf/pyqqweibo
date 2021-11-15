#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.
# Time-stamp: <2011-11-09 10:18:18 wangshuyu>

import os
import mimetypes

from qqweibo.binder import bind_api
from qqweibo.error import QWeiboError
from qqweibo.parsers import ModelParser
from qqweibo.utils import convert_to_utf8_bytes, mulitpart_urlencode


class API(object):
    """Weibo API"""
    # TODO: remove unsupported params
    def __init__(self, auth_handler=None, retry_count=0,
                 host='open.t.qq.com', api_root='/api', cache=None,
                 secure=False, retry_delay=0, retry_errors=None,
                 source=None, parser=None, log=None):
        self.auth = auth_handler
        self.host = host
        self.api_root = api_root
        self.cache = cache
        self.secure = secure
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or ModelParser()
        self.log = log

        self._build_api_path()
    ## 时间线 ##

    """ 1.Statuses/home_timeline 主页时间线 """
    # BUG: type, contenttype, accesslevel is useless
    _statuses_home_timeline = bind_api(
        path = '/statuses/home_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime',
                         'type', 'contenttype'],
    )

    """ 2.Statuses/public_timeline 广播大厅时间线"""
    _statuses_public_timeline = bind_api(
        path = '/statuses/public_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pos'],
    )

    """ 3.Statuses/user_timeline 其他用户发表时间线"""
    _statuses_user_timeline = bind_api(
        path = '/statuses/user_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['name', 'reqnum', 'pageflag', 'pagetime',
                         'lastid', 'type', 'contenttype'],
    )

    """ 4.Statuses/mentions_timeline @提到我的时间线 """
    _statuses_mentions_timeline = bind_api(
        path = '/statuses/mentions_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid',
                         'type', 'contenttype', 'accesslevel'],
    )

    """ 5.Statuses/ht_timeline 话题时间线 """
    _statuses_ht_timeline = bind_api(
        path = '/statuses/ht_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['httext', 'reqnum', 'pageflag', 'pageinfo'],
    )

    """ 6.Statuses/broadcast_timeline 我发表时间线 """
    _statuses_broadcast_timeline = bind_api(
        path = '/statuses/broadcast_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime',
                         'lastid', 'type', 'contenttype'],
    )

    """ 7.Statuses/special_timeline 特别收听的人发表时间线 """
    _statuses_special_timeline = bind_api(
        path = '/statuses/special_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime'],
    )

    """ 8.Statuses/area_timeline 地区发表时间线 """
    # required: country, province, city
    _statuses_area_timeline = bind_api(
        path = '/statuses/area_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['country', 'province', 'city', 'reqnum', 'pos'],
    )

    """ 9.Statuses/home_timeline_ids 主页时间线索引 """
    _statuses_home_timeline_ids = bind_api(
        path = '/statuses/home_timeline_ids',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'type',
                         'contenttype'],
    )

    """ 10.Statuses/user_timeline_ids 其他用户发表时间线索引 """
    # required: name
    _statuses_user_timeline_ids = bind_api(
        path = '/statuses/user_timeline_ids',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['name', 'reqnum', 'pageflag', 'pagetime', 'type',
                         'contenttype'],
    )

    """ 11.Statuses/broadcast_timeline_ids 我发表时间线索引 """
    _statuses_broadcast_timeline_ids = bind_api(
        path = '/statuses/broadcast_timeline_ids',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid', 'type',
                         'contenttype'],
    )

    """ 12.Statuses/mentions_timeline_ids 用户提及时间线索引 """
    _statuses_mentions_timeline_ids = bind_api(
        path = '/statuses/mentions_timeline_ids',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid', 'type',
                         'contenttype'],
    )

    """ 13.Statuses/users_timeline 多用户发表时间线 """
    _statuses_users_timeline = bind_api(
        path = '/statuses/users_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['names', 'reqnum', 'pageflag', 'pagetime',
                         'lastid', 'type', 'contenttype'],
    )

    """ 14.Statuses/users_timeline_ids 多用户发表时间线索引 """
    _statuses_users_timeline_ids = bind_api(
        path = '/statuses/users_timeline_ids',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['names', 'reqnum', 'pageflag', 'pagetime',
                         'lastid', 'type', 'contenttype'],
    )

    """ 15.statuses/ht_timeline_ext 话题时间线 """
    _statuses_ht_timeline_ext = bind_api(
        path = '/statuses/ht_timeline_ext',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['httext', 'reqnum', 'tweetid', 'time', 'pageflag',
                         'flag', 'accesslevel', 'type', 'contenttype'],
    )

    """ 16.statuses/home_timeline_vip 拉取vip用户发表微博消息接口 """
    _statuses_home_timeline_vip = bind_api(
        path = '/statuses/home_timeline_vip',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'lastid', 'pagetime', 'pageflag',],

    )

    _statuses_get_micro_album = bind_api(
        path = '/statuses/get_micro_album',
        payload_type = 'json', payload_list = True,
        allowed_param = ['reqnum', 'name'],
    )

    _statuses_sub_re_list = bind_api(
        path = '/statuses/sub_re_list',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['rootid', 'type', 'reqnum'],
    )

    """ 名单接口 """
    _list_add_to_list = bind_api(
        path = '/add_to_list',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['listid', 'names'],
    )
    ## TODO: finish list api

    ## 微博相关 ##
    """ 1.t/show 获取一条微博数据 """
    _t_show = bind_api(
        path = '/t/show',
        payload_type = 'tweet',
        allowed_param = ['id'],

    )

    """ 2.t/add 发表一条微博 """
    _t_add = bind_api(
        path = '/t/add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'longitude', 'latitude', 'clientip'],

    )

    """ 3.t/del 删除一条微博 """
    _t_del = bind_api(
        path = '/t/del',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 4.t/re_add 转播一条微博 """
    _t_re_add = bind_api(
        path = '/t/re_add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['reid', 'content', 'longitude', 'latitude', 'clientip'],

    )

    """ 5.t/reply 回复一条微博 """
    _t_reply = bind_api(
        path = '/t/reply',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['reid', 'content', 'longitude', 'latitude', 'clientip'],

    )

    """ 6.t/add_pic 发表一条带图片的微博 """
    def _t_add_pic(self, filename, content="", longitude=0, latitude=0, clientip='127.0.0.1'):
        _, query = self.auth.authorize_request(
            "dummy", "POST", {}, dict(content=content, clientip=clientip, longitude=longitude, latitude=latitude))
        headers, post_data = mulitpart_urlencode("pic", filename, **dict(query))

        allowed_param = ['content', 'longitude', 'latitude', 'clientip']
        args = [content, longitude, latitude, clientip]
        return bind_api(
            path = '/t/add_pic',
            method = 'POST',
            payload_type = 'retid',
            allowed_param = allowed_param
            )(self, *args, post_data=post_data, headers=headers)

    """ 7.t/re_count 转播数或点评数 """
    _t_re_count = bind_api(
        path = '/t/re_count',
        payload_type = 'json',
        allowed_param = ['ids', 'flag'],
    )

    """ 8.t/re_list 获取单条微博的转发或点评列表 """
    _t_re_list = bind_api(
        path = '/t/re_list',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['rootid', 'reqnum', 'flag', 'pageflag', 'pagetime',
                         'twitterid'],
    )

    """ 9.t/comment 点评一条微博 """
    _t_comment = bind_api(
        path = '/t/comment',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['reid', 'content', 'longitude', 'latitude', 'clientip'],
    )

    """ 10.t/add_music发表音乐微博 """
    _t_add_music = bind_api(
        path = '/t/add_music',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['url', 'title', 'author', 'content',
                         'longitude', 'latitude', 'clientip'],
    )

    """ 11.t/add_video发表视频微博 """
    _t_add_video = bind_api(
        path = '/t/add_video',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['url', 'content', 'longitude', 'latitude', 'clientip'],
    )

    """ 12.t/getvideoinfo 获取视频信息 """
    _t_getvideoinfo = bind_api(
        path = '/t/getvideoinfo',
        method = 'POST',
        payload_type = 'video',
        allowed_param = ['url'],
    )

    """ 13.t/list 根据微博ID批量获取微博内容（与索引合起来用） """
    _t_list = bind_api(
        path = '/t/list',
        method = 'GET',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['ids'],
    )

    """ 14.t/add_video_prev 预发表一条视频微博 """
    _t_add_video_prev = bind_api(
        path = '/t/add_video_prev',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'longitude', 'latitude', 'vid', 'title', 'clientip'],
    )

    """ 15.t/sub_re_count 获取转播的再次转播数（二次转发次数) """
    _t_sub_re_count = bind_api(
        path = '/t/sub_re_count',
        payload_type = 'dict',
        allowed_param = ['ids'],
    )

    """ 16.t/add_emotion 发表心情帖子 """
    _t_add_emotion = bind_api(
        path = '/t/add_emotion',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['signtype', 'content', 'longitude', 'latitude', 'clientip'],
    )

    _t_add_pic_url = bind_api(
        path = '/t/add_pic_url',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['pic_url', 'content', 'longitude', 'latitude', 'clientip'],
    )

    _t_add_multi = bind_api(
        path = '/t/add_multi',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'longitude', 'latitude', 'pic_url', 'video_url', 'music_url',
                         'music_title', 'music_author', 'clientip'],
    )

    _t_upload_pic = bind_api(
        path = '/t/upload_pic',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['pic_url'],
    )

    ## 帐户相关 ##
    """ 1.User/info获取自己的详细资料 """
    _user_info = bind_api(
        path = '/user/info',
        payload_type = 'user',
        allowed_param = [],

    )

    """ 2.user/update 更新用户信息 """
    _user_update = bind_api(
        path = '/user/update',
        method = 'POST',
        allowed_param = ['nick', 'sex', 'year', 'month',
                         'day', 'countrycode', 'provincecode',
                         'citycode', 'introduction'],

    )

    """ 3.user/update_head 更新用户头像信息 """
    def _user_update_head(self, filename):
        headers, post_data = mulitpart_urlencode("pic", filename)
        args = []
        allowed_param = []

        return bind_api(
            path = '/user/update_head',
            method = 'POST',

            allowed_param = allowed_param
            )(self, *args, post_data=post_data, headers=headers)

    """ 4.user/update_edu 更新用户教育信息 """
    # TODO: 吐槽此条API
    _user_update_edu = bind_api(
        path = '/user/update_edu',
        method = 'POST',
        allowed_param = ['feildid', 'year', 'schoolid', 'departmentid', 'level'],

    )

    """ 5.user/other_info 获取其他人资料 """
    _user_other_info = bind_api(
        path = '/user/other_info',
        payload_type = 'user',
        allowed_param = ['name'],

    )

    """ 6.user/infos 获取一批人的简单资料 """
    _user_infos = bind_api(
        path = '/user/infos',
        payload_type = 'user', payload_list = True,
        allowed_param = ['names'],

    )

    """ 7.user/verify 验证账户是否合法（是否注册微博） """
    _user_verify = bind_api(
        path = '/user/verify',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['name'],

    )

    """ 8.user/emotion 获取心情微博 """ # TODO: if empty returned, may fail
    _user_emotion = bind_api(
        path = '/user/emotion',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['name', 'reqnum', 'pageflag', 'timestamp', 'type',
                         'contenttype', 'accesslevel', 'emotiontype'],

    )

    """ 1.friends/fanslist 我的听众列表 """
    _friends_fanslist = bind_api(
        path = '/friends/fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],

    )

    """ 2.friends/idollist 我收听的人列表 """
    _friends_idollist = bind_api(
        path = '/friends/idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 3.Friends/blacklist 黑名单列表 """
    _friends_blacklist = bind_api(
        path = '/friends/blacklist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 4.Friends/speciallist 特别收听列表 """
    _friends_speciallist = bind_api(
        path = '/friends/speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 5.friends/add 收听某个用户 """
    _friends_add = bind_api(
        path = '/friends/add',
        method = 'POST',
        allowed_param = ['name'],
    )

    """ 6.friends/del取消收听某个用户 """
    _friends_del = bind_api(          # fix conflicts with del
        path = '/friends/del',
        method = 'POST',
        allowed_param = ['name'],
    )

    """ 7.friends/addspecial 特别收听某个用户 """
    _friends_addspecial = bind_api(
        path = '/friends/addspecial',
        method = 'POST',
        allowed_param = ['name'],
    )

    """ 8.friends/delspecial 取消特别收听某个用户 """
    _friends_delspecial = bind_api(
        path = '/friends/delspecial',
        method = 'POST',
        allowed_param = ['name'],

    )

    """ 9.friends/addblacklist 添加某个用户到黑名单 """
    _friends_addblacklist = bind_api(
        path = '/friends/addblacklist',
        method = 'POST',
        allowed_param = ['name'],

    )

    """ 10.friends/delblacklist 从黑名单中删除某个用户 """
    _friends_delblacklist = bind_api(
        path = '/friends/delblacklist',
        method = 'POST',
        allowed_param = ['name'],

    )

    """ 11.friends/check 检测是否我的听众或收听的人 """
    _friends_check = bind_api(
        path = '/friends/check',
        payload_type = 'json',
        allowed_param = ['names', 'flag'],

    )

    """ 12.friends/user_fanslist 其他帐户听众列表 """
    _friends_user_fanslist = bind_api(
        path = '/friends/user_fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
    )

    """ 13.friends/user_idollist 其他帐户收听的人列表 """
    _friends_user_idollist = bind_api(
        path = '/friends/user_idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
    )

    """ 14.friends/user_speciallist 其他帐户特别收听的人列表 """
    _friends_user_speciallist = bind_api(
        path = '/friends/user_speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
    )

    """ 15.friends/fanslist_s 我的听众列表，简单信息（200个）"""
    _friends_fanslist_s = bind_api(
        path = '/friends/fanslist_s',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 16.friends/idollist_s 我的收听列表，简单信息（200个） """
    _friends_idollist_s = bind_api(
        path = '/friends/idollist_s',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 17.friends/mutual_list 互听关系链列表 """
    _friends_mutual_list = bind_api(
        path = '/friends/mutual_list',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
    )

    """ 18.fanslist_name 我的听众列表，只输出name（200个） """
    _friends_fanslist_name = bind_api(
        path = '/friends/fanslist_name',
        payload_type = 'json', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """ 19.idollist_name 我的收听列表，只输出name（200个） """
    _friends_idollist_name = bind_api(
        path = '/friends/idollist_name',
        payload_type = 'json', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
    )

    """  获取用户最亲密的好友列表 """
    _friends_get_intimate_friends = bind_api(
        path = '/friends/get_intimate_friends',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum'],
    )

    """ 好友帐号输入提示 """
    _friends_match_nick_tips = bind_api(
        path = '/friends/match_nick_tips',
        payload_type = 'user', payload_list = True,
        allowed_param = ['match', 'reqnum'],
    )

    ## 私信相关 ##
    """ 1.private/add 发私信 """
    _private_add = bind_api(
        path = '/private/add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['name', 'content', 'longitude', 'latitude', 'clientip'],

    )

    """ 2.private/del 删除一条私信 """
    _private_del = bind_api(
        path = '/private/del',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 3.private/recv 收件箱 """
    _private_recv = bind_api(
        path = '/private/recv',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid'],

    )

    """ 4.private/send 发件箱 """
    _private_send = bind_api(
        path = '/private/send',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid'],

    )

    ## 搜索相关 ##
    """ 1.Search/user 搜索用户 """
    _search_user = bind_api(
        path = '/search/user',
        payload_type = 'user', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],

    )

    """ 2.Search/t 搜索微博 """
    _search_t = bind_api(
        path = '/search/t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],

    )

    """ 3.Search/userbytag 通过标签搜索用户 """
    _search_userbytag = bind_api(
        path = '/search/userbytag',
        payload_type = 'user', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],

    )

    # TODO: model parser
    ## 热度，趋势 ##
    """ 1.trends/ht 话题热榜 """
    _trends_ht = bind_api(
        path = '/trends/ht',
        payload_type = 'json',
        allowed_param = ['reqnum', 'type', 'pos'],

    )

    """ 2.Trends/t 转播热榜 """
    _trends_t = bind_api(
        path = '/trends/t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'type', 'pos'],

    )

    """ 3.trends/famouslist 推荐名人列表 """
    _trends_famouslist = bind_api(
        path = '/trends/famouslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['classid', 'subclassid'],

    )

    ## 数据更新相关 ##
    """ 1.info/update 查看数据更新条数 """
    _info_update = bind_api(
        path = '/info/update',
        payload_type = 'json',
        allowed_param = ['op', 'type'],

    )

    ## 数据收藏 ##
    """ 1.fav/addt 收藏一条微博 """
    _fav_addt = bind_api(
        path = '/fav/addt',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 2.fav/delt 从收藏删除一条微博 """
    _fav_delt = bind_api(
        path = '/fav/delt',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 3.fav/list_t 收藏的微博列表 """
    _fav_list_t = bind_api(
        path = '/fav/list_t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'nexttime', 'prevtime',
                         'lastid'],

    )

    """ 4.fav/addht 订阅话题 """
    _fav_addht = bind_api(
        path = '/fav/addht',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 5.fav/delht 从收藏删除话题 """
    _fav_delht = bind_api(
        path = '/fav/delht',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],

    )

    """ 6.fav/list_ht 获取已订阅话题列表 """
    _fav_list_ht = bind_api(
        path = '/fav/list_ht',
        payload_type = 'json', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime', 'lastid'],

    )

    ## lbs
    # todo: list parser
    _lbs_get_poi = bind_api(
        path = '/lbs/get_poi',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['longitude', 'latitude', 'radius', 'reqnum']
    )

    ## 话题相关 ##
    """ 1.ht/ids 根据话题名称查询话题ID """
    _ht_ids = bind_api(
        path = '/ht/ids',
        payload_type = 'json', payload_list = True,
        allowed_param = ['httexts'],

    )

    """ 2.ht/info 根据话题ID获取话题相关微博 """
    _ht_info = bind_api(
        path = '/ht/info',
        payload_type = 'json', payload_list = True,
        allowed_param = ['ids'],

    )

    ## 标签相关 ##
    """ 1.tag/add 添加标签 """
    _tag_add = bind_api(
        path = '/tag/add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['tag'],

    )

    """ 2.tag/del 删除标签 """
    _tag_del = bind_api(
        path = '/tag/del',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['tagid'],

    )

    ## 名单 ##
    # TODO

    ## 其他 ##
    """ 1.other/kownperson 我可能认识的人 """
    _other_kownperson = bind_api(
        path = '/other/kownperson',
        payload_type = 'user', payload_list = True,
        allowed_param = [],

    )

    """ 2.other/shorturl短URL变长URL """
    _other_shorturl = bind_api(
        path = '/other/shorturl',
        payload_type = 'json',
        allowed_param = ['url'],

    )

    """ 3.other/videokey 获取视频上传的KEY """
    _other_videokey = bind_api(
        path = '/other/videokey',
        payload_type = 'json',
        allowed_param = [],

    )

    """ 4.other/get_emotions 获取表情接口 """
    _other_get_emotions = bind_api(
        path = '/other/get_emotions',
        payload_type = 'json', payload_list = True,
        allowed_param = ['type'],

    )

    """ 5.other/gettopreadd 一键转播热门排行 """
    _other_gettopreadd = bind_api(
        path = '/other/gettopreadd',
        payload_type = 'retid', payload_list = True,
        allowed_param = ['type', 'country', 'province', 'city'],

    )

    """ Get the authenticated user """
    def me(self):
        return self.user.info()

    """ Internal use only """
    def _build_api_path(self):
        """bind all api function to its namespace"""
        self._bind_api_namespace('timeline',
                                 home=self._statuses_home_timeline,
                                 public=self._statuses_public_timeline,
                                 user=self._statuses_user_timeline,
                                 users=self._statuses_users_timeline,
                                 mentions=self._statuses_mentions_timeline,
                                 topic=self._statuses_ht_timeline,
                                 broadcast=self._statuses_broadcast_timeline,
                                 special=self._statuses_special_timeline,
                                 area=self._statuses_area_timeline,
                                 # ids
                                 homeids=self._statuses_home_timeline_ids,
                                 userids=self._statuses_user_timeline_ids,
                                 usersids=self._statuses_users_timeline_ids,
                                 broadcastids=self._statuses_broadcast_timeline_ids,
                                 mentionsids=self._statuses_mentions_timeline_ids)
        self._bind_api_namespace('tweet',
                                 show=self._t_show,
                                 add=self._t_add,
                                 delete=self._t_del,
                                 retweet=self._t_re_add,
                                 reply=self._t_reply,
                                 addpic=self._t_add_pic,
                                 retweetcount=self._t_re_count,
                                 retweetlist=self._t_re_list,
                                 comment=self._t_comment,
                                 addmusic=self._t_add_music,
                                 addvideo=self._t_add_video,
                                 list=self._t_list)
        self._bind_api_namespace('user',
                                 info=self._user_info,
                                 update=self._user_update,
                                 updatehead=self._user_update_head,
                                 userinfo=self._user_other_info,
                                 )
        self._bind_api_namespace('friends',
                                 fanslist=self._friends_fanslist,
                                 idollist=self._friends_idollist,
                                 blacklist=self._friends_blacklist,
                                 speciallist=self._friends_speciallist,
                                 add=self._friends_add,
                                 delete=self._friends_del,
                                 addspecial=self._friends_addspecial,
                                 deletespecial=self._friends_delspecial,
                                 addblacklist=self._friends_addblacklist,
                                 deleteblacklist=self._friends_delblacklist,
                                 check=self._friends_check,
                                 userfanslist=self._friends_user_fanslist,
                                 useridollist=self._friends_user_idollist,
                                 userspeciallist=self._friends_user_speciallist,
                                 )
        self._bind_api_namespace('private',
                                 add=self._private_add,
                                 delete=self._private_del,
                                 inbox=self._private_recv,
                                 outbox=self._private_send,
                                 )
        self._bind_api_namespace('search',
                                 user=self._search_user,
                                 tweet=self._search_t,
                                 userbytag=self._search_userbytag,
                                 )
        self._bind_api_namespace('trends',
                                 topic=self._trends_ht,
                                 tweet=self._trends_t
                                 )
        self._bind_api_namespace('info',
                                 update=self._info_update,
                                 )
        self._bind_api_namespace('fav',
                                 addtweet=self._fav_addt,
                                 deletetweet=self._fav_delt,
                                 listtweet=self._fav_list_t,
                                 addtopic=self._fav_addht,
                                 deletetopic=self._fav_delht,
                                 listtopic=self._fav_list_ht,
                                 )
        self._bind_api_namespace('topic',
                                 ids=self._ht_ids,
                                 info=self._ht_info,
                                 )
        self._bind_api_namespace('tag',
                                 add=self._tag_add,
                                 delete=self._tag_del,
                                 )
        self._bind_api_namespace('other',
                                 kownperson=self._other_kownperson,
                                 shorturl=self._other_shorturl,
                                 videokey=self._other_videokey,
                                 videoinfo=self._t_getvideoinfo,
                                 )
        self.t = self.tweet
        self.statuses = self.timeline   # fix 时间线 相关

    def _bind_api_namespace(self, base, **func_map):
        """ bind api to its path"""
        if base == '':
            for fname in func_map:
                setattr(self, fname, func_map[fname])
        else:
            if callable(getattr(self, base, None)):
                func_map['__call__'] = getattr(self, base)
            mapper = type('ApiPathMapper', (object,), func_map)()
            setattr(self, base, mapper)

    # TODO: more general method
    @staticmethod
    def _pack_image(filename, contentname, max_size=1024, **params):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise QWeiboError('File is too big, must be less than 700kb.')
        except os.error:
            raise QWeiboError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise QWeiboError('Could not determine file type')
        file_type = file_type[0]
        if file_type.split('/')[0] != 'image':
            raise QWeiboError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        BOUNDARY = 'QqWeIbObYaNdElF----'  # qqweibo by andelf
        body = []
        for key, val in params.items():
            if val is not None:
                body.append('--' + BOUNDARY)
                body.append('Content-Disposition: form-data; name="%s"' % key)
                body.append('Content-Type: text/plain; charset=UTF-8')
                body.append('Content-Transfer-Encoding: 8bit')
                body.append('')
                val = convert_to_utf8_bytes(val)
                body.append(val)
        fp = open(filename, 'rb')
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (contentname, filename.encode('utf-8')))
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(fp.read())
        body.append('--%s--' % BOUNDARY)
        body.append('')
        fp.close()
        body.append('--%s--' % BOUNDARY)
        body.append('')
        # fix py3k
        for i in range(len(body)):
            body[i] = convert_to_utf8_bytes(body[i])
        body = b'\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY,
            'Content-Length': len(body)
        }

        return headers, body
