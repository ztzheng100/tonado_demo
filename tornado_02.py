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

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
