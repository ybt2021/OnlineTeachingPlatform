# from tornado.options import define, options, parse_command_line
import tornado
import tornado.web
import tornado.websocket

users = set()  # 所有当前用户

class permitHandler(tornado.websocket.WebSocketHandler):
    global users

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        users.add(self)

    def on_message(self, message):
        print("received")
        for user in users:
            user.write_message(message)

    def on_close(self) -> None:
        users.remove(self)