==================
pyqqweibo 参考文档
==================

---------
Auth 教程
---------

::

  from qqweibo import OAuthHandler, API, JSONParser, ModelParser
  auth = OAuthHandler('API_KEY', 'API_SECRET')

获取用户 Access Token
---------------------

::

  print auth.get_authorization_url()
  verifier = raw_input('PIN: ').strip()
  auth.get_access_token(verifier)

使用已保存的 Token
------------------

::

  token = 'your token'
  tokenSecret = 'your secret'
  auth.setToken(token, tokenSecret)

建立 API 对象
-------------

::

  api = API(a)
  # test
  me = api.user.info()
  print me.name, me.nick, me.location

--------
API 参考
--------

参数名带 **\*** 表示必须传递该参数.

timeline 时间线
---------------

home 主页时间线
  :参数:
    (pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [Tweet_]
  :翻页:
    pageflag+pagetime

  ::

    > api.timeline.home()
    [Tweet]
public 广播大厅时间线
  :参数:
    (reqnum, pos)
  :返回:
    [Tweet_]

  ::

    > api.timeline.public()
    [Tweet]
user 其他用户发表时间线
  :参数:
    (name*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet_]

  ::

    > api.timeline.user('andelf')
    [Tweet]
mentions 用户提及时间线
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype, accesslevel)
  :返回:
    [Tweet_]

  ::

    > api.timeline.mentions()
    [Tweet]
topic 话题时间线
  :参数:
    (httext*, pageflag, pageinfo, reqnum)
  :返回:
    [Tweet_]

  ::

    > api.timeline.topic('CCTV')
    [Tweet]
broadcast 我发表时间线
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet_]

  ::

    > api.timeline.broadcast()
    [Tweet]
special 特别收听的人发表时间线
  :参数:
    (pageflag, pagetime, reqnum)
  :返回:
    [Tweet_]

  ::

    > api.timeline.special()
    [Tweet]
area 地区发表时间线
  :参数:
    (country*, province*, city*, pos, reqnum)
  :返回:
    [Tweet_]

  ::

    > api.timeline.area(country=1, province=44, city=3)
    [Tweet]
homeids 主页时间线索引
  :参数:
    (pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [RetId_]

  ::

    > api.timeline.homeids()
    [RetId] # RetId 可通过 ret.id, ret.timestamp 获取属性
userids 其他用户发表时间线索引
  :参数:
    (name*, pageflag, pagetime, reqnum, type, contenttype)
  :返回:
    [RetId_]

  ::

    > api.timeline.userids(name='NBA')
    [RetId]
broadcastids 我发表时间线索引
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId_]

  ::

    > apt.timeline.broadcastids()
    [RetId]
mentionsids 用户提及时间线索引
  :参数:
    (pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId_]

  ::

    > api.timeline.mentionsids()
    [RetId]
users 多用户发表时间线
  :参数:
    (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [Tweet_]

  ::

    > api.timeline.users(['name1,'name2','andelf'])
    [Tweet]
usersids 多用户发表时间线索引
  :参数:
    (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
  :返回:
    [RetId_]

  ::

    > api.timeline.usersids(['name1,'name2','andelf'])
    [Tweet]

tweet 微博相关(t)
-----------------

show 获取一条微博数据
  :参数:
    (id*)
  :返回:
    Tweet_

  ::

    > api.tweet.show(20574076418461)
    Tweet
add 发表一条微博
  :参数:
    (content*, clientip*, jing, wei)
  :返回:
    RetId_

  ::

    > api.add('some text', clientip='?.?.?.?')
    RetId
delete 删除一条微博
  :参数:
    (id*)
  :返回:
    RetId_

  ::

    > api.tweet.delete(ret.id)
    RetID
retweet 转播一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
  :返回:
    RetId_

  ::

    > api.tweet.retweet(ret.id, "Hello world", '?.?.?.?')
    RetId
reply 回复一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
  :返回:
    RetId_
addpic 发表一条带图片的微博
  :参数:
    (filename*, content*, clientip*, jing, wei)
  :返回:
    RetId_
retweetcount 转播数或点评数
  :参数:
    (ids*, flag)
  :返回:
    需要调用 as_dict() 特殊处理

  ::

    > api.tweet.retweetcount(ids=[253446341312,34243234242]).as_dict()
    {'34243234242': 0, ...}
retweetlist 获取单条微博的转发或点评列表
  :参数:
    (rootid*, flag, pageflag, pagetime, reqnum, twitterid)
  :返回:
    [Tweet_]
comment 点评一条微博
  :参数:
    (reid*, content*, clientip*, jing, wei)
  :返回:
    RetId_
addmusic 发表音乐微博
  :参数:
    (content*, url*, title*, author*, clientip*, jing, wei)
  :返回:
    RetId_
addvideo 发表视频微博
  :说明:
    后台自动分析视频信息，支持youku,tudou,ku6
  :参数:
    (content*, url*, clientip*, jing, wei)
  :返回:
    RetId_
getvideoinfo 获取视频信息
  :参数:
    (url*)
  :返回:
    Video_

  ::

    > api.tweet.getvideoinfo('http://v.youku.com/v_show/id_XMjcxNjEwMzI4.html')
    Video
list 根据微博ID批量获取微博内容（与索引合起来用）
  :参数:
    (ids*)
  :返回:
    [Tweet_]

  ::

    > api.tweet.list(ids=[45018014630554,20575117830267])
    [Tweet]

user 帐户相关
-------------

info 获取自己的详细资料
  :参数:
    ()
  :返回:
    User_
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
  :返回:
    User_

friends 关系链相关
------------------

fanslist 我的听众列表
  :参数:
    (reqnum, startindex)
  :返回:
    [User_]
idollist 我收听的人列表
  :参数:
    (reqnum, startindex)
  :返回:
    [User_]
blacklist 黑名单列表
  :参数:
    (reqnum, startindex)
  :返回:
    [User_]
speciallist 特别收听列表
  :参数:
    (reqnum, startindex)
  :返回:
    [User_]
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
  :返回:
    需要用 as_dict() 处理.

  ::

    > api.friends.check('andelf').as_dict()
    {'andelf': False}
userfanslist 其他帐户听众列表
  :参数:
    (name*, reqnum, startindex)
  :返回:
    [User_]

  ::

    > api.friends.userfanslist(name='andelf')
useridollist 其他帐户收听的人列表
  :参数:
    (name*, reqnum, startindex)
  :返回:
    [User_]
userspeciallist 其他帐户特别收听的人列表
  :参数:
    (name*, reqnum, startindex)
  :返回:
    [User_]

private 私信相关
----------------

add 发私信
  :参数:
    (name*, content*, clientip*, jing, wei)
  :返回:
    RetId_
delete 删除一条私信
  :参数:
    (id*)
  :返回:
    RetId_
inbox 收件箱
  :参数:
    (pageflag, pagetime, reqnum, lastid)
  :返回:
    [Tweet_]
outbox 发件箱
  :参数:
    (pageflag, pagetime, reqnum, lastid)
  :返回:
    [Tweet_]

search 搜索相关
---------------

user 搜索用户
  :参数:
    (keyword*, pagesize, page)
  :返回:
    [User_]
tweet 搜索微博
  :参数:
    (keyword*, pagesize, page)
  :返回:
    [Tweet_]
userbytag 通过标签搜索用户
  :参数:
    (keyword*, pagesize, page)
  :返回:
    [User_]

trends 热度，趋势
-----------------

topic 话题热榜
  :参数:
    (type, reqnum, pos)
tweet 转播热榜
  :参数:
    (type, reqnum, pos)
  :返回:
    [Tweet_]

  ::

    > api.trends.tweet()
    [Tweet]

info 数据更新相关
-----------------

update 查看数据更新条数
  :参数:
    (op, type)
  :返回:
    需要用 as_dict() 处理. 或直接作为属性访问.

  ::

    > api.info.update().as_dict()
    {u'home': 21, u'create': 12, ...}

fav 数据收藏
------------

addtweet 收藏一条微博
  :参数:
    (id*)
  :返回:
    RetId_
deletetweet 从收藏删除一条微博
  :参数:
    (id*)
  :返回:
    RetId_
listtweet 收藏的微博列表
  :参数:
    (pageflag, nexttime, prevtime, reqnum, lastid)
  :返回:
    [Tweet_]
addtopic 订阅话题
  :参数:
    (id*)
  :返回:
    RetId_
deletetopic 从收藏删除话题
  :参数:
    (id*)
  :返回:
    RetId_
listtopic 获取已订阅话题列表
  :参数:
    (reqnum, pageflag, pagetime, lastid)
  :返回:
    TODO

topic 话题相关
--------------

ids 根据话题名称查询话题ID
  :参数:
    (httexts*)
  :返回:
    TODO

  ::

    > api.topic.ids(u"地震")[0].id
info 根据话题ID获取话题相关情况
  :参数:
    (ids*)
  :返回:
    TODO

  ::

    > t = api.topic.info(5149259073282301489)[0]
    > print t.text, t.tweetnum

tag 标签相关
------------

TODO: don't have a test account

add 添加标签
  :参数:
    (tag*)
  :返回:
    TODO
delete 删除标签
  :参数:
    (tagid*)
  :返回:
    TODO

other 其他
----------

kownperson 我可能认识的人
  :参数:
    ()
  :返回:
    TODO

  ::

    api.other.kownperson()
    > [User]
shorturl 短URL变长URL
  :参数:
    (url*)
  :返回:
    使用 as_dict() 获取或者直接作为属性访问.

  ::

    # like http://url.cn/0jkApX
    api.other.shorturl('0jkApX').as_dict()
    > {'ctime': 0, 'longurl': u'http://...', 'secu': 3}
videokey 获取视频上传的KEY
  :参数:
    ()
  :返回:
    使用 as_dict() 获取或者直接作为属性访问.

  ::

    api.other.videokey().as_dict()
    > {'uid': u'VNcmwzbqxdu=', 'videokey': u'$xMcNnpvswmmftd5pPkm'}

----------
Model 列表
----------

.. _Tweet:

Tweet
-----

::

    > t = api.tweet.show(20574076418461)
    > t.retweet("test")
    <RetId id:15108001017434>
    > api.tweet.show(_.id)
    <Tweet object #15108001017434>

* delete()
* retweet(content, clientip, jing=None, wei=None)
* reply(content, clientip, jing=None, wei=None)
* comment(content, clientip, jing=None, wei=None)
* retweetlist(\*\*kwarg)
* retweetcount(flag=0)
* favorite()
* unfavorite()

.. _User:

User
----

* self
  是否为自己
* update(\*\*kwargs)
* timeline(\*\*kwargs)
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

.. _Video:

Video
-----

* title
* minipic
* palyer
* real
* short

.. _RetId:

RetId
-----

* id
* timestamp 某些情况下没有

--------
翻页教程
--------

pageflag + pagetime
-------------------

::

    > api.timeline.home(reqnum=1)
    [<Tweet object #76501075355511>]

    > api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    [<Tweet object #29107120390232>]

    > api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    [<Tweet object #78001074250068>]

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



