#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2009-2010 Joshua Roesslein
# Copyright 2011 andelf <andelf@gmail.com>
# See LICENSE for details.

import os
import mimetypes

from qqweibo.binder import bind_api
from qqweibo.error import QWeiboError
from qqweibo.parsers import ModelParser


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

        self._build_api_path()
    ## 时间线 ##
    """ 1.Statuses/home_timeline 主页时间线 """
    _home_timeline = bind_api(
        path = '/api/statuses/home_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    """ 2.Statuses/public_timeline 广播大厅时间线"""
    _public_timeline = bind_api(
        path = '/api/statuses/public_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pos', 'reqnum'],
        require_auth = True
    )

    """ 3.Statuses/user_timeline 其他用户发表时间线"""
    _user_timeline = bind_api(
        path = '/api/statuses/user_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['name', 'pageflag', 'pagetime', 'reqnum',
                         'lastid'],     # move name to first
        require_auth = True
    )

    """ 4.Statuses/mentions_timeline @提到我的时间线 """
    _mentions_timeline = bind_api(
        path = '/api/statuses/mentions_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum', 'lastid'],
        require_auth = True
    )

    """ 5.Statuses/ht_timeline 话题时间线 """
    _ht_timeline = bind_api(
        path = '/api/statuses/ht_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['httext', 'pageflag', 'pageinfo',
                         'reqnum'],
        require_auth = True
    )

    """ 6.Statuses/broadcast_timeline 我发表时间线 """
    _broadcast_timeline = bind_api(
        path = '/api/statuses/broadcast_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    """ 7.Statuses/special_timeline 特别收听的人发表时间线 """
    _special_timeline = bind_api(
        path = '/api/statuses/special_timeline',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum'],
        require_auth = True
    )

    ## 微博相关 ##
    """ 1.t/show 获取一条微博数据 """
    _tshow = bind_api(
        path = '/api/t/show',
        payload_type = 'tweet',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 2.t/add 发表一条微博 """
    _tadd = bind_api(
        path = '/api/t/add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'clientip', 'jing', 'wei'],
        require_auth = True
    )

    """ 3.t/del 删除一条微博 """
    _tdel = bind_api(                  # del cofilicts with del in python
        path = '/api/t/del',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 4.t/re_add 转播一条微博 """
    _tre_add = bind_api(
        path = '/api/t/re_add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 5.t/reply 回复一条微博 """
    _treply = bind_api(
        path = '/api/t/reply',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'clientip',
                         'jing', 'wei', 'reid'],
        require_auth = True
    )

    """ 6.t/add_pic 发表一条带图片的微博 """
    def _tadd_pic(self, filename, content, clientip, jing=None, wei=None):
        headers, post_data = API._pack_image(filename, contentname="pic", content=content, clientip=clientip, jing=jing, wei=wei, )
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
            payload_type = 'retid',
            require_auth = True,
            allowed_param = allowed_param
            )(self, *args, post_data=post_data, headers=headers)

    """ 7.t/re_count 转播数或点评数 """ # FIXME
    # bug here
    _tre_count = bind_api(
        path = '/api/t/re_count',
        payload_type = 'json',
        allowed_param = ['ids', 'flag'],
        require_auth = True
    )

    """ 8.t/re_list 获取单条微博的转发或点评列表 """ # TODO: test
    _tre_list = bind_api(
        path = '/api/t/re_list',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['rootid', 'flag', 'pageflag', 'pagetime',
                         'reqnum', 'twitterid',],
        require_auth = True
    )

    """ 9.t/comment 点评一条微博 """
    _tcomment = bind_api(
        path = '/api/t/comment',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'clientip', 'jing', 'wei',
                         'reid'],
        require_auth = True
    )

    """ 10.t/add_music发表音乐微博 """
    _tadd_music = bind_api(
        path = '/api/t/add_music',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['content', 'clientip', 'jing', 'wei',
                         'url', 'title', 'author'],
        require_auth = True
    )

    """ 11.t/add_video发表视频微博 """
    _tadd_video = bind_api(
        path = '/api/t/add_video',
        method = 'POST',
        payload_type = 'retid',
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
    info = bind_api(                  # info confilicts with api namespace
        path = '/api/user/info',
        payload_type = 'user',
        allowed_param = [],
        require_auth = True
    )

    """ 2.user/update 更新用户信息 """
    _uupdate = bind_api(
        path = '/api/user/update',
        method = 'POST',
        allowed_param = ['nick', 'sex', 'year', 'month',
                         'day', 'countrycode', 'provincecode',
                         'citycode', 'introduction'],
        require_auth = True
    )

    """ 3.user/update_head 更新用户头像信息 """
    def _uupdate_head(self, filename):
        headers, post_data = API._pack_image(filename, "pic")
        args = []
        allowed_param = []

        return bind_api(
            path = '/api/user/update_head',
            method = 'POST',
            require_auth = True,
            allowed_param = allowed_param
            )(self, *args, post_data=post_data, headers=headers)

    """ 4.user/other_info 获取其他人资料 """
    _uother_info = bind_api(
        path = '/api/user/other_info',
        payload_type = 'user',
        allowed_param = ['name'],
        require_auth = True
    )

    ## 关系链相关 ##
    """ 1.friends/fanslist 我的听众列表 """
    _ffanslist = bind_api(
        path = '/api/friends/fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )

    """ 2.friends/idollist 我收听的人列表 """
    _fidollist = bind_api(
        path = '/api/friends/idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )

    """ 3.Friends/blacklist 黑名单列表 """
    _fblacklist = bind_api(
        path = '/api/friends/blacklist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )

    """ 4.Friends/speciallist 特别收听列表 """
    _fspeciallist = bind_api(
        path = '/api/friends/speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['reqnum', 'startindex'],
        require_auth = True
    )


    """ 5.friends/add 收听某个用户 """
    _fadd = bind_api(
        path = '/api/friends/add',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )

    """ 6.friends/del取消收听某个用户 """
    _fdel = bind_api(          # fix confilicts with del
        path = '/api/friends/del',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )

    """ 7.friends/addspecial 特别收听某个用户 """
    _faddspecial = bind_api(
        path = '/api/friends/addspecial',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )

    """ 8.friends/delspecial 取消特别收听某个用户 """
    _fdelspecial = bind_api(
        path = '/api/friends/delspecial',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )

    """ 9.friends/addblacklist 添加某个用户到黑名单 """
    _faddblacklist = bind_api(
        path = '/api/friends/addblacklist',
        method = 'POST',
        allowed_param = ['name'],
        require_auth = True
    )

    """ 10.friends/delblacklist 从黑名单中删除某个用户 """
    _fdelblacklist = bind_api(
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
    _fuser_fanslist = bind_api(
        path = '/api/friends/user_fanslist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )

    """ 13.friends/user_idollist 其他帐户收听的人列表 """
    _fuser_idollist = bind_api(
        path = '/api/friends/user_idollist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )

    """ 14.friends/user_speciallist 其他帐户特别收听的人列表 """
    _fuser_speciallist = bind_api(
        path = '/api/friends/user_speciallist',
        payload_type = 'user', payload_list = True,
        allowed_param = ['name', 'reqnum', 'startindex'],
        require_auth = True
    )


    ## 私信相关 ##
    """ 1.private/add 发私信 """
    _padd = bind_api(
        path = '/api/private/add',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['name', 'content', 'clientip', 'jing',
                         'wei'],
        require_auth = True
    )

    """ 2.private/del 删除一条私信 """
    _pdel = bind_api(
        path = '/api/private/del',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 3.private/recv 收件箱 """
    _precv = bind_api(
        path = '/api/private/recv',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum', 'lastid'],
        require_auth = True
    )

    """ 4.private/send 发件箱 """
    _psend = bind_api(
        path = '/api/private/send',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'pagetime', 'reqnum',
                         'lastid'],
        require_auth = True
    )

    ## 搜索相关 ##
    """ 1.Search/user 搜索用户 """
    _suser = bind_api(
        path = '/api/search/user',
        payload_type = 'user', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    """ 2.Search/t 搜索微博 """
    _st = bind_api(
        path = '/api/search/t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    """ 3.Search/userbytag 通过标签搜索用户 """
    _suserbytag = bind_api(
        path = '/api/search/userbytag',
        payload_type = 'user', payload_list = True,
        allowed_param = ['keyword', 'pagesize', 'page'],
        require_auth = True
    )

    # TODO: model parser
    ## 热度，趋势 ##
    """ 1.trends/ht 话题热榜 """
    ht = bind_api(
        path = '/api/trends/ht',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['type', 'reqnum', 'pos'],
        require_auth = True
    )
    topic = ht

    ## 数据更新相关 ##
    """ 1.info/update 查看数据更新条数 """
    iupdate = bind_api(
        path = '/api/info/update',
        payload_type = 'json',
        allowed_param = ['op', 'type'],
        require_auth = True
    )

    ## 数据收藏 ##
    """ 1.fav/addt 收藏一条微博 """
    _faddt = bind_api(
        path = '/api/fav/addt',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 2.fav/delt 从收藏删除一条微博 """
    _fdelt = bind_api(
        path = '/api/fav/delt',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 3.fav/list_t 收藏的微博列表 """
    _flist_t = bind_api(
        path = '/api/fav/list_t',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['pageflag', 'nexttime', 'prevtime',
                         'reqnum', 'lastid'],
        require_auth = True
    )

    """ 4.fav/addht 订阅话题 """
    _faddht = bind_api(
        path = '/api/fav/addht',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 5.fav/delht 从收藏删除话题 """
    _fdelht = bind_api(
        path = '/api/fav/delht',
        method = 'POST',
        payload_type = 'retid',
        allowed_param = ['id'],
        require_auth = True
    )

    """ 6.fav/list_ht 获取已订阅话题列表 """
    _flist_ht = bind_api(
        path = '/api/fav/list_ht',
        payload_type = 'json', payload_list = True,
        allowed_param = ['reqnum', 'pageflag', 'pagetime',
                         'lastid'],
        require_auth = True
    )

    ## 话题相关 ##
    """ 1.ht/ids 根据话题名称查询话题ID """
    _hids = bind_api(
        path = '/api/ht/ids',
        payload_type = 'json', payload_list = True,
        allowed_param = ['httexts'],
        require_auth = True
    )

    """ 2.ht/info 根据话题ID获取话题相关微博 """
    _hinfo = bind_api(
        path = '/api/ht/info',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['ids'],
        require_auth = True
    )

    ## 标签相关 ##
    """ 1.tag/add 添加标签 """
    _tag_add = bind_api(
        path = '/api/tag/add',
        method = 'POST',
        payload_type = 'tweet', payload_list = True,
        allowed_param = ['tag'],
        require_auth = True
    )

    """ 2.tag/del 删除标签 """
    _tag_del = bind_api(
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

    """ Get the authenticated user """
    def me(self):
        return self.user.info()
    ####################
    """ Internal use only """
    def _build_api_path(self):
        self._bind_api_namespace('timeline',
                                 home=self._home_timeline,
                                 public=self._public_timeline,
                                 user=self._user_timeline,
                                 mentions=self._mentions_timeline,
                                 topic=self._ht_timeline,
                                 broadcast=self._broadcast_timeline,
                                 special=self._special_timeline)
        self._bind_api_namespace('t',
                                 show=self._tshow,
                                 add=self._tadd,
                                 delete=self._tdel,
                                 retweet=self._tre_add,
                                 reply=self._treply,
                                 addpic=self._tadd_pic,
                                 #retweets=self._tre_count, # bad
                                 retweets=self._tre_list,
                                 comment=self._tcomment,
                                 addmusic=self._tadd_music,
                                 addvideo=self._tadd_video,
                                 getvideoinfo=self.getvideoinfo)
        self._bind_api_namespace('user',
                                 info=self.info, # :) shortcut
                                 update=self._uupdate,
                                 updatehead=self._uupdate_head,
                                 otherinfo=self._uother_info,
                                 userinfo=self._uother_info, # M
                                 )
        self._bind_api_namespace('friends',
                                 fanslist=self._ffanslist,
                                 idollist=self._fidollist,
                                 blacklist=self._fblacklist,
                                 speciallist=self._fspeciallist,
                                 add=self._fadd,
                                 delete=self._fdel,
                                 addspecial=self._faddspecial,
                                 delspecial=self._fdelspecial,
                                 deletespecial=self._fdelspecial,
                                 addblacklist=self._faddblacklist,
                                 delblacklist=self._fdelblacklist,
                                 deleteblacklist=self._fdelblacklist,
                                 check=self.check,
                                 otherfanslist=self._fuser_fanslist,
                                 otheridollist=self._fuser_idollist,
                                 otherspeciallist=self._fuser_speciallist,
                                 userfanslist=self._fuser_fanslist,
                                 useridollist=self._fuser_idollist,
                                 userspeciallist=self._fuser_speciallist,
                                 # ends here
                                 )
        self._bind_api_namespace('private',
                                 add=self._padd,
                                 delete=self._pdel,
                                 recv=self._precv,
                                 send=self._psend,
                                 )
        self._bind_api_namespace('search',
                                 user=self._suser,
                                 t=self._st,
                                 tweet=self._st, # multiple binding
                                 userbytag=self._suserbytag,
                                 )
        self._bind_api_namespace('trends',
                                 topic=self.ht,
                                 )
        self._bind_api_namespace('info',
                                 update=self.iupdate,
                                 )
        self._bind_api_namespace('fav',
                                 addt=self._faddt,
                                 delt=self._fdelt,
                                 deletet=self._fdelt, # multiple binding
                                 listt=self._flist_t, # M
                                 listtweet=self._flist_t,
                                 addtopic=self._faddht,
                                 deltopic=self._fdelht,
                                 deletetopic=self._fdelht,
                                 listtopic=self._flist_ht,
                                 )
        self._bind_api_namespace('topic', # no more `ht`..
                                 ids=self._hids,
                                 info=self._hinfo,
                                 )
        self._bind_api_namespace('tag',
                                 add=self._tag_add,
                                 delete=self._tag_del,
                                 )
        self._bind_api_namespace('other',
                                 kownperson=self.kownperson,
                                 )
        self.tweet = self.t
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
        #except os.error, e:
        except os.error:
            raise QWeiboError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise QWeiboError('Could not determine file type')
        file_type = file_type[0]
        if file_type.split('/')[0] != 'image': # dummy
            raise QWeiboError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        BOUNDARY = 'QqWeIbObYaNdElF----' # qqweibo by andelf
        body = []
        for key, val in params.items():
            if val is not None:
                body.append('--' + BOUNDARY)
                body.append('Content-Disposition: form-data; name="%s"' % key)
                body.append('Content-Type: text/plain; charset=UTF-8')
                body.append('Content-Transfer-Encoding: 8bit')
                body.append('')
                if isinstance(val, unicode):
                    val = val.encode('utf-8')
                body.append(str(content))
        fp = open(filename, 'rb')
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


