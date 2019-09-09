#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_03_RequestHandler
# Description:  RequestHandler的更多知识
# Author:       zzt
# Date:         2019/8/24
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
'''
http://127.0.0.1:8000/

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
