#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tonodo_01
# Description:  
# Author:       zzt
# Date:         2019/8/24
#-------------------------------------------------------------------------------


import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
