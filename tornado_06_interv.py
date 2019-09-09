#!usr/bin/env python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         tornado_06_interv
# Description:  
# Author:       zzt
# Date:         2019/8/24
# -------------------------------------------------------------------------------

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError

define("port", default=8000, type=int, help="run server on the given port.")


class InterfaceHandler(RequestHandler):

    def initialize(self,database):
        print( "调用了initialize()"+database)

    def prepare(self):
        print( "调用了prepare()")

    def set_default_headers(self):
        print("调用了set_default_headers()")

    def write_error(self, status_code, **kwargs):
        print("调用了write_error()")

    def get(self):
        print("调用了get()")

    def post(self):
        print("调用了post()")
        self.send_error(200)  # 注意此出抛出了错误

    def on_finish(self):
        print("调用了on_finish()")

class ProfileHandler(RequestHandler):
    def initialize(self, database):
        print("call ProfileHandler_initialize() ")
        self.database = database

    def get(self):
        print("call ProfileHandler_get() ")
        self.write("ok")


class IndexHandler(RequestHandler):
    """主路由处理类"""

    def get(self):
        """对应http的get请求方式"""
        # subject = self.get_argument('q')
        # query_arg = self.get_query_argument('q')
        subject = self.get_arguments('q')
        query_arg = self.get_query_arguments('q')
        self.write(','.join(query_arg))
        # self.write(subject)


'''
http://127.0.0.1:8000/?q=1&q=0
http://127.0.0.1:8000/user/11/
http://127.0.0.1:8000/l1/

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r'/user/(?P<database>.*)', ProfileHandler, {"database": "python"}),
        (r'/l1/', InterfaceHandler, {"database": "python"}),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
