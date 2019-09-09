#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_03_RequestHandler
# Description:  RequestHandler的更多知识
# Author:       zzt
# Date:         2019/8/24
#-------------------------------------------------------------------------------

import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError
from tornado.httpclient import AsyncHTTPClient

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self):
        method = self.request.method
        host = self.request.host
        remoteip = self.request.remote_ip
        url = self.request.uri
        path  = self.request.path
        version = self.request.version
        body = self.request.body
        rep = "method:%s<br/>" % method
        rep += "host:%s<br/>" % host
        rep += "remoteip:%s<br/>" % remoteip
        rep += "url:%s<br/>" % url
        rep += "path:%s<br/>" % path
        rep += "host:%s<br/>" % host
        rep += "version:%s<br/>" % version
        rep += "body:%s<br/>" % body

        self.write(rep)
        # self.write(subject)

class WeatherHandler(RequestHandler):

    # @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    @tornado.gen.coroutine  #添加异步装饰器
    def get(self):
        client =AsyncHTTPClient()
        response = yield client.fetch("https://api.caiyunapp.com/v"
                     "2/TAkhjf8d1nlSlspN/121.6544,25.1552/realtime.json"
                     )
        json_data = response.body
        data = json.loads(json_data)
        self.write(response.body)  # 获取请求参数

    def on_response(self,resp):
        json_data = resp.body
        data = json.loads(json_data)
        self.write("15615")
        self.finish()


class WeatherHandler2(RequestHandler):

    # @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    @tornado.gen.coroutine  #添加异步装饰器
    def get(self):
        response = yield self.get_data()
        json_data = response.body
        data = json.loads(json_data)
        self.write(response.body)  # 获取请求参数

    def on_response(self,resp):
        json_data = resp.body
        data = json.loads(json_data)
        self.write("15615")
        self.finish()

    @tornado.gen.coroutine
    def get_data(self):
        client = AsyncHTTPClient()
        response = yield client.fetch("https://api.caiyunapp.com/v"
                                      "2/TAkhjf8d1nlSlspN/121.6544,25.1552/realtime.json"
                                      )
        raise tornado.gen.Return(response)


'''
http://127.0.0.1:8000/
http://127.0.0.1:8000/weather/
http://127.0.0.1:8000/weather2/     # 异步Web请求单独
'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/weather/", WeatherHandler),
        (r"/weather2/", WeatherHandler2),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

