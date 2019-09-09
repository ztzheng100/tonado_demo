#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_10_auth
# Description:  
# Author:       zzt
# Date:         2019/8/25
#-------------------------------------------------------------------------------


import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get_current_user(self):
        """在此完成用户的认证逻辑"""
        user_name = self.get_argument("name", None)
        return user_name

    @tornado.web.authenticated
    def get(self):
        self.write("ok")


class LoginHandler(RequestHandler):
    def get(self):
        """在此返回登陆页面"""
        self.write("登陆页面")
        """登陆处理，完成登陆后跳转回前一页面"""
        next = self.get_argument("next", "/")
        print(next)
        self.redirect(next + "?name=logined")


class ProfileHandler(RequestHandler):
    def get_current_user(self):
        """在此完成用户的认证逻辑"""
        user_name = self.get_argument("name", None)
        return user_name

    @tornado.web.authenticated
    def get(self):
        self.write("这是我的个人主页。")

'''
http://127.0.0.1:8000/index
http://127.0.0.1:8000/
'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/profile", ProfileHandler),
        ],
        login_url="/login"
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
