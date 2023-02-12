# import datetime
# import os
import tornado.web
import tornado.ioloop
# from tornado.options import define, options, parse_command_line
import tornado.websocket
import torndb_for_python3 as torndb
# import json
# from collections import defaultdict


class RoomsHandler(tornado.web.RequestHandler):

    def get(self):
        error = ''
        pagesize = self.get_argument('pageSize')
        pagenumber = self.get_argument('pageNumber')

        # --------------此处连接数据库room表分页获取房间--------------------
        # 1.连接数据库
        db = torndb.Connection(
            host='localhost',
            database='live',
            user='root',
            password='111111'
        )
        try:
            result = db.query('select * from room limit ' +
                              pagenumber+","+pagesize)
            self.write(str(result))

        except:
            self.write("wrong in getting rooms")
        # 3.关闭连接
        db.close()

    def post(self):
        # 获取登录用户信息
        username = self.get_argument('username')
        password = self.get_argument('password')
        # self.get_body_argument()
