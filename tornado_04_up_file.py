#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_03_RequestHandler
# Description:  上传图片
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
        print(type(self.request.files))
        print(self.request.files.keys())
        print(type(self.request.files['image1']))
        # self.request.files['image1']
        if self.request.files['image1'] :
            file = open(r"./tet.jpg","wb")
            file.write(self.request.files['image1'][0]['body'])

            file.close()
            self.write("ok")
        else:
            self.write("false")
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

