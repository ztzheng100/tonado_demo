#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_03_RequestHandler
# Description:  RequestHandler的更多知识
# Author:       zzt
# Date:         2019/8/24
#-------------------------------------------------------------------------------
import os
import json
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError
from tornado.httpclient import AsyncHTTPClient
from tornado.websocket import WebSocketHandler
import datetime


define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self):
        self.render("web_chat.html")
class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
'''
http://127.0.0.1:8000/
http://127.0.0.1:8000/chat/

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat/", ChatHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
