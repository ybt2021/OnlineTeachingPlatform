import tornado.web
import tornado.ioloop
# from tornado.options import define, options, parse_command_line
import tornado.websocket


class ShowWhiteboardHandler(tornado.web.RequestHandler):
    def get(self):
        # error = ''
        self.render('whiteboard.html')
