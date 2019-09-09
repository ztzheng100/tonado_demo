#!usr/bin/env python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tornado_08_mysql
# Description:  
# Author:       zzt
# Date:         2019/8/25
#-------------------------------------------------------------------------------

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler, MissingArgumentError,StaticFileHandler
import os
import pymysql
define("port", default=8000, type=int, help="run server on the given port.")

db =  pymysql.Connection(host='127.0.0.1', database='testtornado', user='root', password='zzt123',charset='utf8')
class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self):
        self.render("db_op.html",res_str="")

    def post(self):
        cursor = self.application.db.cursor()
        test_sql = self.get_argument("text","")
        print(test_sql)
        res = cursor.execute(test_sql)
        res_str=""
        for i in cursor.fetchall():
            print(i)
            res_str= ";".join(i)
        print('共查询到：', cursor.rowcount, '条数据。')
        cursor.close()  # 关闭游标
        self.application.db.close()  # 关闭连接
        self.render("db_op.html", res_str=res_str)

'''

http://127.0.0.1:8000/zzt/

'''
if __name__ == "__main__":
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        (r'/zzt/$',IndexHandler),
    ],
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    template_path=os.path.join(os.path.dirname(__file__), "templates")

    )
    app.db = db
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
