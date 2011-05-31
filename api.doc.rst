==================
pyqqweibo 参考文档
==================

--------
API 列表
--------


timeline 时间线
---------------

home 主页时间线
  :参数:
    (pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [Tweet]
  :翻页:
    pageflag+pagetime

  ::

    api.timeline.home()
    > [Tweet]
public 广播大厅时间线
  :参数:
    (reqnum, pos)
  :返回:
    [Tweet]

  ::

    api.timeline.public()
    > [Tweet]
user 其他用户发表时间线
  :参数:
    (name*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet]

  ::

    api.timeline.user('andelf')
    > [Tweet]
mentions 用户提及时间线
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype, accesslevel)
  :返回:
    [Tweet]

  ::

    api.timeline.mentions()
    > [Tweet]
topic 话题时间线
  :参数:
    (httext*, pageflag, pageinfo, reqnum)
  :返回:
    [Tweet]

  ::

    api.timeline.topic('CCTV')
    > [Tweet]
broadcast 我发表时间线
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet]

  ::

    api.timeline.broadcast()
    > [Tweet]
special 特别收听的人发表时间线
  :参数:
    (pageflag, pagetime, reqnum)
  :返回:
    [Tweet]

  ::

    api.timeline.special()
    > [Tweet]
area 地区发表时间线
  :参数:
    (country*, province*, city*, pos, reqnum)
  :返回:
    [Tweet]

  ::

    api.timeline.area(country=1, province=44, city=3)
    > [Tweet]
homeids 主页时间线索引
  :参数:
    (pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [RetId]

  ::

    api.timeline.homeids()
    > [RetId] # RetId 可通过 ret.id, ret.timestamp 获取属性
userids 其他用户发表时间线索引
  :参数:
    (name*, pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [RetId]

  ::

    api.timeline.userids(name='NBA')
    > [RetId]
broadcastids 我发表时间线索引
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId]

  ::

    apt.timeline.broadcastids()
    > [RetId]
mentionsids 用户提及时间线索引
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId]

  ::

    api.timeline.mentionsids()
    > [RetId]
users 多用户发表时间线
  :参数:
    (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet]

  ::

    api.timeline.users(['name1,'name2','andelf'])
    > [Tweet]
usersids 多用户发表时间线索引
  :参数:
    (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId]

  ::

    api.timeline.usersids(['name1,'name2','andelf'])
    > [Tweet]

tweet 微博相关(t)
-----------------

show 获取一条微博数据
  :参数:
    (id*)
  :返回:
    Tweet

  ::

    api.tweet.show(20574076418461)
    > Tweet
add 发表一条微博
  :参数:
    (content*, clientip*, jing, wei)
  :返回:
    RetId

  ::

    api.add('some text', clientip='?.?.?.?')
    > RetId
delete 删除一条微博
  :参数:
    (id*)
  :返回:
    RetId

  ::

    api.tweet.delete(ret.id)
    > RetID
retweet 转播一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
  :返回:
    RetId
reply 回复一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
  :返回:
    RetId
addpic 发表一条带图片的微博
  :参数:
    (filename*, content*, clientip*, jing, wei)
  :返回:
    RetId
retweetcount 转播数或点评数
  :参数:
    (ids*, flag)
  :返回:
    需要调用 as_dict() 特殊处理

  ::

    api.tweet.retweetcount(ids=[253446341312,34243234242]).as_dict()
    > {'34243234242': 0, ...}
retweetlist 获取单条微博的转发或点评列表
  :参数:
    (rootid*, flag, pageflag, pagetime, reqnum, twitterid)
comment 点评一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
addmusic 发表音乐微博
  :参数:
    (content*, url*, title*, author*, clientip*, jing, wei)
addvideo 发表视频微博
  :说明:
    后台自动分析视频信息，支持youku,tudou,ku6
  :参数:
    (content*, url*, clientip*, jing, wei)
getvideoinfo 获取视频信息
  :参数:
    (url*)

  ::

    api.tweet.getvideoinfo('http://v.youku.com/v_show/id_XMjcxNjEwMzI4.html')
    > [Video] # .title
list 根据微博ID批量获取微博内容（与索引合起来用）
  :参数:
    (ids*)

  ::

    api.tweet.list(ids=[45018014630554,20575117830267])
    > [Tweet]

user 帐户相关
-------------

info 获取自己的详细资料
  :参数:
    ()
update 更新用户信息
  :参数:
    (nick*, sex*, year*, month*, day*, countrycode*, provincecode*,
    citycode*, introduction*)
updatehead 更新用户头像信息
  :参数:
    (filename*)
userinfo 获取其他人资料
  :参数:
    (name*)

friends 关系链相关
------------------

fanslist 我的听众列表
  :参数:
    (reqnum, startindex)
idollist 我收听的人列表
  :参数:
    (reqnum, startindex)
blacklist 黑名单列表
  :参数:
    (reqnum, startindex)
speciallist 特别收听列表
  :参数:
    (reqnum, startindex)
add 收听某个用户
  :参数:
    (name*)
delete 取消收听某个用户
  :参数:
    (name*)
addspecial 特别收听某个用户
  :参数:
    (name*)
deletespecial 取消特别收听某个用户
  :参数:
    (name*)
addblacklist 添加某个用户到黑名单
  :参数:
    (name*)
deleteblacklist 从黑名单中删除某个用户
  :参数:
    (name*)
check  检测是否我的听众或收听的人
  :参数:
    (names*, flag)

  ::

    api.friends.check('andelf').as_dict()
    > {'andelf': False}
userfanslist 其他帐户听众列表
  :参数:
    (name*, reqnum, startindex)

  ::

    api.friends.userfanslist(name='andelf')
useridollist 其他帐户收听的人列表
  :参数:
    (name*, reqnum, startindex)
userspeciallist 其他帐户特别收听的人列表
  :参数:
    (name*, reqnum, startindex)

private 私信相关
----------------

add 发私信
  :参数:
    (name*, content*, clientip*, jing, wei)
delete 删除一条私信
  :参数:
    (id*)
inbox 收件箱
  :参数:
    (pageflag, pagetime, reqnum, lastid)
outbox 发件箱
  :参数:
    (pageflag, pagetime, reqnum, lastid)

search 搜索相关
---------------

user 搜索用户
  :参数:
    (keyword*, pagesize, page)
tweet 搜索微博
  :参数:
    (keyword*, pagesize, page)
userbytag 通过标签搜索用户
  :参数:
    (keyword*, pagesize, page)

trends 热度，趋势
-----------------

topic 话题热榜
  :参数:
    (type, reqnum, pos)
tweet 转播热榜
  :参数:
    (type, reqnum, pos)

  ::

    api.trends.tweet()
    > [Tweet]

info 数据更新相关
-----------------

update 查看数据更新条数
  :参数:
    (op, type)

  ::

    api.info.update().as_dict()
    > {u'home': 21, u'create': 12, ...}

fav 数据收藏
------------

addtweet 收藏一条微博
  :参数:
    (id*)
deletetweet 从收藏删除一条微博
  :参数:
    (id*)
listtweet 收藏的微博列表
  :参数:
    (pageflag, nexttime, prevtime, reqnum, lastid)
addtopic 订阅话题
  :参数:
    (id*)
deletetopic 从收藏删除话题
  :参数:
    (id*)
listtopic 获取已订阅话题列表
  :参数:
    (reqnum, pageflag, pagetime, lastid)

topic 话题相关
--------------

ids 根据话题名称查询话题ID
  :参数:
    (httexts*)

  ::

    api.topic.ids(u"地震")[0].id
info 根据话题ID获取话题相关情况
  :参数:
    (ids*)

  ::

    t = api.topic.info(5149259073282301489)[0]
    print t.text, t.tweetnum

tag 标签相关
------------

TODO: don't have a test account

add 添加标签
  :参数:
    (tag*)
delete 删除标签
  :参数:
    (tagid*)

other 其他
----------

kownperson 我可能认识的人
  :参数:
    ()

  ::

    api.other.kownperson()
    > [User]
shorturl 短URL变长URL
  :参数:
    (url*)

  ::

    # like http://url.cn/0jkApX
    api.other.shorturl('0jkApX').as_dict()
    > {'ctime': 0, 'longurl': u'http://...', 'secu': 3}
videokey 获取视频上传的KEY
  :参数:
    ()

  ::

    api.other.videokey().as_dict()
    > {'uid': u'VNcmwzbqxdu=', 'videokey': u'$xMcNnpvswmmftd5pPkm'}

----------
Model 列表
----------

Tweet
-----

::

    t = api.tweet.show(20574076418461)
    t.retweet("test")
    > <RetId id:15108001017434>
    api.tweet.show(_.id)
    > <Tweet object #15108001017434>

* delete()
* retweet(content, clientip, jing=None, wei=None)
* reply(content, clientip, jing=None, wei=None)
* comment(content, clientip, jing=None, wei=None)
* retweetlist(\*\*kwarg)
* retweetcount(flag=0)
* favorite()
* unfavorite()

User
----

* self
  是否为自己
* update(##kwargs)
* timeline(##kwargs)
* add() / follow()
* delete() / unfollow()
* addspecial()
* deletespecial()
* addblacklist() / block()
* deleteblacklist() / unblock()
* fanslist(\*\*kwargs) / followers()
* idollist(\*\*kwargs) / followers()
* speciallist(\*\*kwargs)
* pm(content, clientip, jing=None, wei=None)

--------
翻页教程
--------

pageflag + pagetime
-------------------

::

    api.timeline.home(reqnum=1)
    > [<Tweet object #76501075355511>]

    api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    > [<Tweet object #29107120390232>]

    api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    > [<Tweet object #78001074250068>]

pos
---

不推荐使用使用 pos 翻页.

::

    pos = 0
    reqnum = 20
    ret = api.timeline.public(reqnum=reqnum, pos=pos)
    if len(ret)< reqnum:
        break
    pos += len(ret)
    ret = api.timeline.public(reqnum=reqnum, pos=pos)

lastid
------

至今未成功过, 可见腾讯之垃圾.

pageflag + pageinfo
-------------------

TODO



