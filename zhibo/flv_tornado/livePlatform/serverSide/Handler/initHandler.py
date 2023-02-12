# import os
# from tornado.options import define, options, parse_command_line
import tornado
import tornado.web
import tornado.websocket
import json

users = set()  # 所有当前用户


class initHandler(tornado.websocket.WebSocketHandler):
    global users

    def check_origin(self, origin):
        return True

    def open(self):
        # users.add(self)
        room = str(self.get_argument('roomid'))  # 聊天室
        stu = str(self.get_argument('username'))  # 用户
        for user in users:
            user.write_message(json.dumps(
                {'room': room, 'message': stu+'已进入直播间'}))
        users.add(self)

    def on_message(self, message):
        pass
        # for user in users:
        #     user.write_message(message)

    def on_close(self) -> None:
        users.remove(self)
