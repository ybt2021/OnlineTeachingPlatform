import tornado.web
import tornado.ioloop
# from tornado.options import define, options, parse_command_line
import tornado.websocket
# from collections import defaultdict


class RegisterHandler(tornado.web.RequestHandler):

    def get(self):
        error = ''
        self.render('register.html', error=error)

    def post(self):
        # 获取登录用户信息
        username = self.get_argument('username')
        password = self.get_argument('password')
        # self.get_body_argument()

# --------------此处连接数据库user表,如果用户未存在,新增一条用户记录--------------------
