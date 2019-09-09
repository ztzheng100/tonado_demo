#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_05_resposn
# Description:  
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

define("port", default=8000, type=int, help="run server on the given port.")
class IndexHandler_err(RequestHandler):
    def get(self):
        err_code = self.get_argument("code", None) # 注意返回的是unicode字符串，下同
        err_title = self.get_argument("title", "")
        err_content = self.get_argument("content", "")
        if err_code:
            self.send_error(int(err_code), title=err_title, content=err_content)
        else:
            self.write("主页")

    def write_error(self, status_code, **kwargs):
        self.write(u"<h1>出错了，程序员GG正在赶过来！</h1>")
        self.write(u"<p>错误名：%s</p>" % kwargs["title"])
        self.write(u"<p>错误详情：%s</p>" % kwargs["content"])

class IndexHandler(RequestHandler):
    def set_default_headers(self):
        print("执行了set_default_headers()")
        # 设置get与post方式的默认响应体格式为json
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        # 设置一个名为itcast、值为python的header
        self.set_header("itcast", "python")
        self.set_status(404,"故意的")

    def get(self):
        print("执行了get()")
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
        self.set_header("itcast", "i love python") # 注意此处重写了header中的itcast字段

    def post(self):
        print("执行了post()")
        stu = {
            "name":"zhangsan",
            "age":24,
            "gender":1,
        }
        stu_json = json.dumps(stu)
        self.write(stu_json)
'''
http://127.0.0.1:8000/
http://127.0.0.1:8000/err/
http://127.0.0.1:8000/err/?code=404&title=test&content=hhh

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/err/", IndexHandler_err),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()