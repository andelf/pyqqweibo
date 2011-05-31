# -*- mode: org -*-

pyqqweibo document
==================

# API 列表

## timeline 时间线
* home 主页时间线

  (pageflag, pagetime, reqnum, type, contenttype)
  翻页: pageflag+pagetime
      api.timeline.home()
      > [Tweet]
* public 广播大厅时间线

  (reqnum, pos)
      api.timeline.public()
      > [Tweet]
* user 其他用户发表时间线
  (name*, pageflag, pagetime, reqnum, lastid, type, contenttype)
      api.timeline.user('andelf')
      > [Tweet]
* mentions 用户提及时间线
  (pageflag, pagetime, reqnum, lastid, type, contenttype, accesslevel)
      api.timeline.mentions()
      > [Tweet]
* topic 话题时间线
  (httext*, pageflag, pageinfo, reqnum)
      api.timeline.topic('CCTV')
      > [Tweet]
* broadcast 我发表时间线
  (pageflag, pagetime, reqnum, lastid, type, contenttype)
      api.timeline.broadcast()
      > [Tweet]
* special 特别收听的人发表时间线
  (pageflag, pagetime, reqnum)
      api.timeline.special()
      > [Tweet]
* area 地区发表时间线
  (country*, province*, city*, pos, reqnum)
      api.timeline.area(country=1, province=44, city=3)
      > [Tweet]
* homeids 主页时间线索引
  (pageflag, pagetime, reqnum, type, contenttype)
      api.timeline.homeids()
      > [RetId] # RetId 可通过 ret.id, ret.timestamp 获取属性
* userids 其他用户发表时间线索引
  (name*, pageflag, pagetime, reqnum, type, contenttype)
      api.timeline.userids(name='NBA')
      [RetId]
* broadcastids 我发表时间线索引
  (pageflag, pagetime, reqnum, lastid, type, contenttype)
      apt.timeline.broadcastids()
      > [RetId]
* mentionsids 用户提及时间线索引
  (pageflag, pagetime, reqnum, lastid, type, contenttype)
      api.timeline.mentionsids()
      > [RetId]
* users 多用户发表时间线
  (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
      api.timeline.users(['name1,'name2','andelf'])
      > [Tweet]
* usersids 多用户发表时间线索引
  (names*, pageflag, pagetime, reqnum, lastid, type, contenttype)
      api.timeline.usersids(['name1,'name2','andelf'])
      > [Tweet]

## tweet 微博相关(t)
* show 获取一条微博数据
  (id*)
      api.tweet.show(20574076418461)
      > Tweet
* add 发表一条微博
  (content*, clientip*, jing, wei)
      api.add('some text', clientip='?.?.?.?')
      > RetId
* delete 删除一条微博
  (id*)
      api.tweet.delete(ret.id)
      > RetID
* retweet 转播一条微博
  (reid*, content*, clientip*, jing, wei)
* reply 回复一条微博
* addpic 发表一条带图片的微博
  (filename*, content*, clientip*, jing, wei)
* retweetcount 转播数或点评数
  (ids*, flag)
      api.tweet.retweetcount(ids=[253446341312,34243234242]).as_dict()
      > {'34243234242': 0, ...}
* retweetlist 获取单条微博的转发或点评列表
  (rootid*, flag, pageflag, pagetime, reqnum, twitterid)
* comment 点评一条微博
  (reid*, content*, clientip*, jing, wei)
* addmusic 发表音乐微博
  (content*, url*, title*, author*, clientip*, jing, wei)
* addvideo 发表视频微博
  # 后台自动分析视频信息，支持youku,tudou,ku6
  (content*, url*, clientip*, jing, wei)
* getvideoinfo 获取视频信息
  (url*)
      api.tweet.getvideoinfo('http://v.youku.com/v_show/id_XMjcxNjEwMzI4.html')
      > [Video] # .title
* list 根据微博ID批量获取微博内容（与索引合起来用）
  (ids*)
      api.tweet.list(ids=[45018014630554,20575117830267])
      > [Tweet]

## user 帐户相关
* info 获取自己的详细资料
  ()
* update 更新用户信息
  (nick*, sex*, year*, month*, day*, countrycode*, provincecode*,
   citycode*, introduction*)
* updatehead 更新用户头像信息
  (filename*)
* userinfo 获取其他人资料
  (name*)

## friends 关系链相关
* fanslist 我的听众列表
  (reqnum, startindex)
* idollist 我收听的人列表
  (reqnum, startindex)
* blacklist 黑名单列表
  (reqnum, startindex)
* speciallist 特别收听列表
  (reqnum, startindex)
* add 收听某个用户
  (name*)
* delete 取消收听某个用户
  (name*)
* addspecial 特别收听某个用户
  (name*)
* deletespecial 取消特别收听某个用户
  (name*)
* addblacklist 添加某个用户到黑名单
  (name*)
* deleteblacklist 从黑名单中删除某个用户
  (name*)
* check  检测是否我的听众或收听的人
  (names*, flag)
    api.friends.check('andelf').as_dict()
    > {'andelf': False}
* userfanslist 其他帐户听众列表
  (name*, reqnum, startindex)
    api.friends.userfanslist(name='andelf')
* useridollist 其他帐户收听的人列表
  (name*, reqnum, startindex)
* userspeciallist 其他帐户特别收听的人列表
  (name*, reqnum, startindex)

## private 私信相关
* add 发私信
  (name*, content*, clientip*, jing, wei)
* delete 删除一条私信
  (id*)
* inbox 收件箱
  (pageflag, pagetime, reqnum, lastid)
* outbox 发件箱
  (pageflag, pagetime, reqnum, lastid)

## search 搜索相关
* user 搜索用户
  (keyword*, pagesize, page)
* tweet 搜索微博
  (keyword*, pagesize, page)
* userbytag 通过标签搜索用户
  (keyword*, pagesize, page)

## trends 热度，趋势
* topic 话题热榜
  (type, reqnum, pos)
* tweet 转播热榜
  (type, reqnum, pos)
    api.trends.tweet()
    [Tweet]

## info 数据更新相关
* update 查看数据更新条数
  (op, type)
    api.info.update().as_dict()
    > {u'home': 21, u'create': 12, ...}

## fav 数据收藏
* addtweet 收藏一条微博
  (id*)
* deletetweet 从收藏删除一条微博
  (id*)
* listtweet 收藏的微博列表
  (pageflag, nexttime, prevtime, reqnum, lastid)
* addtopic 订阅话题
  (id*)
* deletetopic 从收藏删除话题
  (id*)
* listtopic 获取已订阅话题列表
  (reqnum, pageflag, pagetime, lastid)

## topic 话题相关
* ids 根据话题名称查询话题ID
  (httexts*)
      api.topic.ids(u"地震")[0].id
* info 根据话题ID获取话题相关情况
  (ids*)
      t = api.topic.info(5149259073282301489)[0]
      print t.text, t.tweetnum

## tag 标签相关
TODO: don't have a test account
* add 添加标签
  (tag*)
* delete 删除标签
  (tagid*)

## other 其他
* kownperson 我可能认识的人
  ()
      api.other.kownperson()
      > [User]
* shorturl 短URL变长URL
  (url*)
      # like http://url.cn/0jkApX
      api.other.shorturl('0jkApX').as_dict()
      > {'ctime': 0, 'longurl': u'http://...', 'secu': 3}
* videokey 获取视频上传的KEY
  ()
      api.other.videokey().as_dict()
      > {'uid': u'VNcmwzbqxdu=', 'videokey': u'$xMcNnpvswmmftd5pPkm'}

# Model 列表
## Tweet
    t = api.tweet.show(20574076418461)
    t.retweet("test")
    > <RetId id:15108001017434>
    api.tweet.show(_.id)
    > <Tweet object #15108001017434>

* delete()
* retweet(content, clientip, jing=None, wei=None)
* reply(content, clientip, jing=None, wei=None)
* comment(content, clientip, jing=None, wei=None)
* retweetlist(#kwarg)
* retweetcount(flag=0)
* favorite()
* unfavorite()

## User
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
* fanslist(##kwargs) / followers()
* idollist(##kwargs) / followers()
* speciallist(##kwargs)
* pm(content, clientip, jing=None, wei=None)

# 翻页教程
## pageflag + pagetime
    api.timeline.home(reqnum=1)
    > [<Tweet object #76501075355511>]

    api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    > [<Tweet object #29107120390232>]

    api.timeline.home(reqnum=1, pageflag=1, pagetime=_[-1].timestamp)
    > [<Tweet object #78001074250068>]

## pos
不推荐使用使用 pos 翻页.

    pos = 0
    reqnum = 20
    ret = api.timeline.public(reqnum=reqnum, pos=pos)
    if len(ret)< reqnum:
        break
    pos += len(ret)
    ret = api.timeline.public(reqnum=reqnum, pos=pos)

## lastid
至今未成功过, 可见腾讯之垃圾.

## pageflag + pageinfo
TODO



