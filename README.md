pyqqweibo
=========

By @andelf <andelf@gmail.com>

腾讯微博 API Python 绑定, 基于 Twitter API 绑定库 tweepy 改写. 目前在不断完善中.

已经更新到 5.27 日 API 版本.

我就不吐槽腾讯的 API 了.

特色
----

* 缓存支持
* 友好的 Model 支持, 返回对象(对象列表)支持简单方法
* 可以返回 JSON 或 XML 数据(多 Parser 支持)
* 修改所有 API 绑定组织结构参数顺序及返回等

具体参考 `api.doc.rst` 及　`Changelog`

使用方法
--------

`api.doc.rst` 文件为参考文档.

相关例子请参考 `examples` 目录.

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
