#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_07_static
# Description:  
# Author:       zzt
# Date:         2019/8/24
#-------------------------------------------------------------------------------


import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError,StaticFileHandler
import os

define("port", default=8000, type=int, help="run server on the given port.")
def house_title_join(titles):
    return "+".join(titles)

class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self):
        house_list = [
            {
                "price": 398,
                "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            },
            {
                "price": 398,
                "titles": ["宽窄巷子", "160平大空间", "文化保护区双地铁"],
                "score": 5,
                "comments": 6,
                "position": "北京市丰台区六里桥地铁"
            }]
        self.render("index.html",text1="",houses=house_list, title_join = house_title_join)

    def post(self):
        text = self.get_argument("text1", "")
        print(text)
        self.render("index.html", text1=text,houses="", title_join = house_title_join)
'''
http://127.0.0.1:8000/static/html/index.html
http://127.0.0.1:8000/
http://127.0.0.1:8000/zzt/
http://127.0.0.1:8000/view/index.html

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        (r'^/$', StaticFileHandler,{"path": os.path.join(current_path, "statics/html"), "default_filename": "index.html"}),
        (r'^/view/(.*)$', StaticFileHandler, {"path": os.path.join(current_path, "statics/html")}),
        (r'/zzt/$',IndexHandler)
    ],
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

