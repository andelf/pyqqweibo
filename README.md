pyqqweibo
=========

腾讯微博 API Python 绑定, 基于 Twitter API 绑定库 tweepy 改写. 目前在不断完善中.

已经更新到 5.27 日 API 版本.

我就不吐槽腾讯的 API 了.

特色
----

* 缓存支持
* 友好的 Model 支持, 返回对象(对象列表)支持简单方法
* 可以返回 JSON 数据
* 删除所有 API 函数中下划线, 全小写

具体参考 `api.doc.rst` 及　`Changelog`

使用方法
--------

相关例子请参考 `examples` 目录.

`api.doc.rst` 文件为参考文档.

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

	me = api.user.info()
	print me.name, me.nick, me.location

	for t in me.timeline(reqnum=3):  # my timeline
		print t.nick, t.text, timestamp_to_str(t.timestamp)

	nba = api.user.userinfo('NBA')
	for u in nba.followers(reqnum=3):  # got NBA's fans
		u.follow()
		break  # follow only 1 fans ;)
	u.unfollow()  # then unfollow

	for t in nba.timeline(reqnum=1):
		print t.text
		t.favorite()  # i like this very much

	for fav in api.fav.listtweet():
		if fav.id == t.id:
			fav.unfavorite()

Further TODO
------------

* 翻页支持
* fix bugs
* add more examples

About
-----

本 API 绑定是在 tweepy <https://github.com/joshthecoder/tweepy> 的基础上完成.

作者: andelf <andelf@gmail.com>

License: MIT

环境依赖:

* Python 2.7 测试通过
* Python 2.5 及之前可能需要安装 simplejson 支持包
* Python-OAuth <http://code.google.com/p/oauth> 已经包含

欢迎和我讨论相关问题 :)
