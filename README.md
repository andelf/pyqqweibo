pyqqweibo
=========

By @andelf <andelf@gmail.com>

腾讯微博 API Python 绑定, 基于 Twitter API 绑定库 tweepy 改写. 目前在不断完善中.

已经更新到 5.27 日 API 版本.

我就不吐槽腾讯的 API 了. 相关吐槽请参考 `api.doc.rst`.

特色
----

* 缓存支持
* 友好的 Model 支持, 返回对象(对象列表)支持简单方法
* 可以返回 JSON 或 XML 数据(多 Parser 支持)
* 修改所有 API 绑定组织结构参数顺序及返回等
* 支持 Python 3
* 良好文档支持, 包括 doc string
* 单元测试

使用方法
--------

具体文档请参考 `api.doc.rst`.

API 使用例子请参考 `tests` 及 `example` 目录下文件.

简单 API 用法可直接 `help()`.

Further TODO
------------

* 翻页支持
* fix bugs
* add more examples

About
-----

作者: andelf <andelf@gmail.com>

License: MIT

环境依赖:

* Python 2.6 - Python 3.2 测试通过
* Python 2.5 及之前请安装 simplejson 后自由 hack
* Python-OAuth <http://code.google.com/p/oauth> 已经包含, 而且已经被改得体无完肤

欢迎和我讨论相关问题 :)
