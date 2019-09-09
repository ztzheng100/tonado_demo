#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_09_safe
# Description:  
# Author:       zzt
# Date:         2019/8/25
#-------------------------------------------------------------------------------
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
import time
import os

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self):
        self.set_cookie("n1", "v1")
        self.set_cookie("n2", "v2", path="/new", expires=time.strptime("2016-11-11 23:59:59", "%Y-%m-%d %H:%M:%S"))
        self.set_cookie("n3", "v3", expires_days=20)
        # 利用time.mktime将本地时间转换为UTC标准时间
        self.set_cookie("n4", "v4", expires=time.mktime(time.strptime("2016-11-11 23:59:59", "%Y-%m-%d %H:%M:%S")))
        self.write("OK")
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


class ClearOneCookieHandler(RequestHandler):
    def get(self):
        self.clear_cookie("n3")
        self.write("clear_cookie(n3)OK")

class SetCookieHandler(RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        self.set_secure_cookie("count", str(count))
        self.write(
            '<html><head><title>Cookie计数器</title></head>'
            '<body><h1>您已访问本页%d次。</h1>' % count +
            '</body></html>'
        )


class XSRFHandler(RequestHandler):
    def get(self):
        self.render("XSRF_test.html")

    def post(self):
        self.write("hello itcast")
'''
http://127.0.0.1:8000/
http://127.0.0.1:8000/clear/
http://127.0.0.1:8000/cur/
http://127.0.0.1:8000/XSRF/

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/clear/$", ClearOneCookieHandler),
        (r"/cur/$", SetCookieHandler),
        (r"/XSRF/$", XSRFHandler),
    ],
    cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
    xsrf_cookies=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
