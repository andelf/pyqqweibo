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
    # TODO: remove unsupported params
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
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    """ 2.Statuses/public_timeline 广播大厅时间线"""
    public_timeline = bind_api(
        path = '/api/statuses/public_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pos', 'reqnum'],
        require_auth = True
    )

    """ 3.Statuses/user_timeline 其他用户发表时间线"""
    user_timeline = bind_api(
        path = '/api/statuses/user_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['name', 'pageflag', 'pagetime', 'reqnum',
                         'lastid'],     # move name to first
        require_auth = True
    )

    """ 4.Statuses/mentions_timeline @提到我的时间线 """
    mentions_timeline = bind_api(
        path = '/api/statuses/mentions_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum', 'lastid'],
        require_auth = True
    )

    """ 5.Statuses/ht_timeline 话题时间线 """
    ht_timeline = bind_api(
        path = '/api/statuses/ht_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['httext', 'pageflag', 'pageinfo',
                         'reqnum'],
        require_auth = True
    )
    # 个人很鄙视 ht_....
    #topic_timeline = ht_timeline

    """ 6.Statuses/broadcast_timeline 我发表时间线 """
    broadcast_timeline = bind_api(
        path = '/api/statuses/broadcast_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    """ 7.Statuses/special_timeline 特别收听的人发表时间线 """
    special_timeline = bind_api(
        path = '/api/statuses/special_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    ## 微博相关 ##
    """ 1.t/show 获取一条微博数据 """
    show = bind_api(
        path = '/api/t/show',
        payload_type = 'tweet',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 2.t/add 发表一条微博 """
    add = bind_api(
        path = '/api/t/add',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip', 'jing', 'wei'],
        require_auth = True
    )

    """ 3.t/del 删除一条微博 """
    delete = bind_api(                  # del cofilicts with del in python
        path = '/api/t/del',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 4.t/re_add 转播一条微博 """
    re_add = bind_api(
        path = '/api/t/re_add',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 5.t/reply 回复一条微博 """
    reply = bind_api(
        path = '/api/t/reply',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 6.t/add_pic 发表一条带图片的微博 """
    # add_pic = bind_api(
    #     path = '/api/t/add_pic',
    #     method = 'POST',
    #     payload_type = 'tweet', payload_list = True,
    #     allowed_param = ['content', 'clientip',
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
            payload_type = 'json',
            require_auth = True,
            allowed_param = allowed_param            
            )(self, *args, post_data=post_data, headers=headers)

    """ 7.t/re_count 转播数或点评数 """ # FIXME
    # bug here
    re_count = bind_api(
        path = '/api/t/re_count',
        payload_type = 'json',
        allowed_param = ['ids', 'flag'],
        require_auth = True
    )

    """ 8.t/re_list 获取单条微博的转发或点评列表 """ # TODO: test
    re_list = bind_api(
        path = '/api/t/re_list',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['rootid', 'flag', 'pageflag', 'pagetime',
                         'reqnum', 'twitterid',],
        require_auth = True
    )

    """ 9.t/comment 点评一条微博 """
    comment = bind_api(
        path = '/api/t/comment',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip', 'jing', 'wei',
                         'reid'],
        require_auth = True
    )

    """ 10.t/add_music发表音乐微博 """
    add_music = bind_api(
        path = '/api/t/add_music',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip', 'jing', 'wei',
                         'url', 'title', 'author'],
        require_auth = True
    )

    """ 11.t/add_video发表视频微博 """
    add_video = bind_api(
        path = '/api/t/add_video',
        method = 'POST',
        payload_type = 'json',
        allowed_param = ['content', 'clientip', 'jing', 'wei',
                         'url'], # supports: youku,tudou,ku6
        require_auth = True
    )
    
    """ 12.t/getvideoinfo 获取视频信息 """
    getvideoinfo = bind_api(
        path = '/api/t/getvideoinfo',
        method = 'POST',
        payload_type = 'video',# fix
        allowed_param = ['url'], # supports: youku,tudou,ku6
        require_auth = True
    )

    ## 帐户相关 ##
    """ 1.User/info获取自己的详细资料 """
    info = bind_api(
        path = '/api/user/info',
        payload_type = 'user',
        allowed_param = [],
        require_auth = True
    )

    """ 2.user/update 更新用户信息 """
    update = bind_api(
        path = '/api/user/update',
        method = 'POST',
        allowed_param = ['nick', 'sex', 'year', 'month',
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
            require_auth = True,
            allowed_param = allowed_param            
            )(self, *args, post_data=post_data, headers=headers)

    """ 4.user/other_info 获取其他人资料 """
    other_info = bind_api(
        path = '/api/user/other_info',
        payload_type = 'user',
        allowed_param = ['name'],
        require_auth = True
    )

    ## 关系链相关 ##
    """ 1.friends/fanslist 我的听众列表 """
    fanslist = bind_api(
        path = '/api/friends/fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )

    """ 2.friends/idollist 我收听的人列表 """
    idollist = bind_api(
        path = '/api/friends/idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )

    """ 3.Friends/blacklist 黑名单列表 """
    blacklist = bind_api(
        path = '/api/friends/blacklist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )    

    """ 4.Friends/speciallist 特别收听列表 """
    speciallist = bind_api(
        path = '/api/friends/speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )    


    """ 5.friends/add 收听某个用户 """
    # TODO: fix confilicts with add message
    fadd = bind_api(
        path = '/api/friends/add',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    

    """ 6.friends/del取消收听某个用户 """
    # TODO: fix confilicts with add message
    fdelete = bind_api(          # fix confilicts with del
        path = '/api/friends/del',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    

    """ 7.friends/addspecial 特别收听某个用户 """
    addspecial = bind_api(
        path = '/api/friends/addspecial',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    

    """ 8.friends/delspecial 取消特别收听某个用户 """
    delspecial = bind_api(
        path = '/api/friends/delspecial',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    

    """ 9.friends/addblacklist 添加某个用户到黑名单 """
    addblacklist = bind_api(
        path = '/api/friends/addblacklist',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    

    """ 10.friends/delblacklist 从黑名单中删除某个用户 """
    delblacklist = bind_api(
        path = '/api/friends/delblacklist',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )    


    """ 11.friends/check 检测是否我的听众或收听的人 """
    check = bind_api(
        path = '/api/friends/check',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['names', 'flag'],
        require_auth = True
    )    

    """ 12.friends/user_fanslist 其他帐户听众列表 """
    user_fanslist = bind_api(
        path = '/api/friends/user_fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )

    """ 13.friends/user_idollist 其他帐户收听的人列表 """
    user_idollist = bind_api(
        path = '/api/friends/user_idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )

    """ 14.friends/user_speciallist 其他帐户特别收听的人列表 """
    user_speciallist = bind_api(
        path = '/api/friends/user_speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )    


    ## 私信相关 ""
    """ 1.private/add 发私信 """
    padd = bind_api(
        path = '/api/private/add',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['content', 'clientip', 'jing',
                         'wei', 'name'],
        require_auth = True
    )

    """ 2.private/del 删除一条私信 """
    pdel = bind_api(
        path = '/api/private/del',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['id'],
        require_auth = True
    )

    """ 3.private/recv 收件箱 """
    recv = bind_api(
        path = '/api/private/recv',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    """ 4.private/send 发件箱 """
    send = bind_api(
        path = '/api/private/send',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    ## 搜索相关 ##
    """ 1.Search/user 搜索用户 """
    user = bind_api(
        path = '/api/search/user',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    """ 2.Search/t 搜索微博 """
    t = bind_api(
        path = '/api/search/t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    """ 3.Search/userbytag 通过标签搜索用户 """
    userbytag = bind_api(
        path = '/api/search/userbytag',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    ## 热度，趋势 ##
    """ 1.trends/ht 话题热榜 """
    ht = bind_api(
        path = '/api/trends/ht',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['type', 'reqnum', 'pos'],
        require_auth = True
    )

    ## 数据更新相关 ##
    """ 1.info/update 查看数据更新条数 """
    iupdate = bind_api(
        path = '/api/info/update',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['op', 'type'],
        require_auth = True
    )

    ## 数据收藏 ##
    """ 1.fav/addt 收藏一条微博 """
    addt = bind_api(
        path = '/api/fav/addt',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['id'],
        require_auth = True
    )

    """ 2.fav/delt 删除一条微博从收藏 """
    delt = bind_api(
        path = '/api/fav/delt',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['id'],
        require_auth = True
    )

    """ 3.fav/list_t 收藏的微博列表 """
    list_t = bind_api(
        path = '/api/fav/list_t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'nexttime', 'prevtime',
                         'reqnum', 'lastid'],
        require_auth = True
    )

    """ 4.fav/addht 订阅话题 """
    addht = bind_api(
        path = '/api/fav/addht',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['id'],
        require_auth = True
    )

    """ 5.fav/delht 从收藏删除话题 """
    delht = bind_api(
        path = '/api/fav/delht',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['id'],
        require_auth = True
    )

    """ 6.fav/list_ht 获取已订阅话题列表 """
    list_ht = bind_api(
        path = '/api/fav/list_ht',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime',
                         'lastid'],
        require_auth = True
    )

    ## 话题相关 ##
    """ 1.ht/ids 根据话题名称查询话题ID """
    ids = bind_api(
        path = '/api/ht/ids',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['httexts'],
        require_auth = True
    )

    """ 2.ht/info 根据话题ID获取话题相关微博 """
    hinfo = bind_api(
        path = '/api/ht/info',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['ids'],
        require_auth = True
    )

    ## 标签相关 ##
    """ 1.tag/add 添加标签 """
    tadd = bind_api(
        path = '/api/tag/add',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['tag'],
        require_auth = True
    )

    """ 2.tag/del 删除标签 """
    tdel = bind_api(
        path = '/api/tag/del',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['tagid'],
        require_auth = True
    )


    ## 其他 ##
    """ 1.other/kownperson 我可能认识的人 """
    kownperson = bind_api(
        path = '/api/other/kownperson',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['ip', 'country_code', 'province_code',
                         'city_code'],
        require_auth = True
    )


    ####################
    
    """ Get the authenticated user """
    def me(self):
        return self.get_user(screen_name=self.auth.get_username())

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
        BOUNDARY = 'QqWeIbObYaNdElF'
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


