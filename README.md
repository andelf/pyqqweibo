pyqqweibo
=========

腾讯微博 API Python 绑定, 基于 Twitter API 绑定库 tweepy 改写. 目前在不断完善中.

使用方法
--------

相关例子请参考 `examples` 目录.

	# simple use
	from qqweibo import OAuthHandler, API, JSONParser, ModelParser
	from qqweibo.utils import timestamp_to_str
	
	a = OAuthHandler('API_KEY', 'API_SECRET')
	
	# use this
	print a.get_authorization_url()
	verifier = raw_input('PIN: ').strip()
	a.get_access_token(verifier)
	
	# or directly use:
	#token = 'your token'
	#tokenSecret = 'your secret'
	#a.setToken(token, tokenSecret)
	
	api = API(a)
	
	me = api.me()  # also api.info(), api.user.info()
	print me.name, me.nick, me.location
	
	for t in me.timeline(reqnum=3):  # my timeline
	print t.nick, t.text, timestamp_to_str(t.timestamp)
	
	nba = api.user.otherinfo('NBA')
	for u in nba.followers(reqnum=3):  # got NBA's fans
	u.follow()
	break  # follow only 1 fans ;)
	u.unfollow()  # then unfollow
	
	for t in nba.timeline(reqnum=1):
	print t.text
	t.favorite()  # i like this very much
	
	for fav in api.fav.listt():
	if fav.id == t.id:
	fav.unfavorite()


已经完成功能
------------

* 授权
* 所有 API json 请求返回
* API model parser
* 部分 API 名字修正, 比如替换 ht 为 topic

Further TODO
------------

* Document
* fix bugs
* add more examples

About
-----

本 API 绑定是在 tweepy <https://github.com/joshthecoder/tweepy> 的基础上完成.

作者: andelf <andelf@gmail.com>

License: MIT

环境依赖:
	Python 2.7 测试通过
	Python 2.5 及之前可能需要安装 simplejson 支持包
	Python-OAuth <http://code.google.com/p/oauth> 已经包含

欢迎和我讨论相关问题 :)
