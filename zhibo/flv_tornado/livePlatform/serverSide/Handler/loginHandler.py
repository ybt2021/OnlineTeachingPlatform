# import datetime
# import os
import json
import tornado.web
import tornado.ioloop
# from tornado.options import define, options, parse_command_line
import tornado.websocket
import torndb_for_python3 as torndb
# from collections import defaultdict


class LoginHandler(tornado.web.RequestHandler):

    def get(self):
        error = ''
        self.render('login.html', error=error)

    def post(self):
        # 获取登录用户信息
        username = self.get_argument('username')
        password = self.get_argument('password')

        # 1.连接数据库
        db = torndb.Connection(
            host='localhost',
            database='live',
            user='root',
            password='111111'
        )

        # 2.简单查询
        try:
            result = db.query(
                'select * from user where username="'+username+'"')
            s_json = json.dumps(result[0])
            print(result)
            s_dict = json.loads(s_json)
            password_res = s_dict["password"]
            userid_res = s_dict["userid"]
            print(userid_res)
            if password == password_res:
                self.set_cookie('username', username)
                self.set_cookie('userid', str(userid_res))
                self.render('rooms.html', username=username)

            else:
                self.render('login.html', error="wrong password")

        except:
            print("no such user")
            self.render('login.html', error="no such user")

        # 3.关闭连接
        db.close()
