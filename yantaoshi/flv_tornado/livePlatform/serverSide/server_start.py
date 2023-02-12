import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
# from tornado.options import define, options

from Handler.loginHandler import LoginHandler
from Handler.registerHandler import RegisterHandler
from Handler.chatHandler import chatHandler
from Handler.whiteboardHandler import WhiteboardHandler, whiteboardIndexHandler
from Handler.showWhiteboardHandler import ShowWhiteboardHandler
from Handler.liveHandler import LiveHandler
from Handler.roomsHandler import RoomsHandler
from Handler.stuliveHandler import stuLiveHandler
from Handler.wstestHandler import wstestHandler
from Handler.permitHandler import permitHandler
from Handler.handHandler import handHandler
from Handler.initHandler import initHandler

from Handler.stu_sign import stuIndexHandler, stuSignHandler, signProcessHandler
from Handler.tea_sign import teaCheckHandler, signAnalyseHandler, teaClearHandler, teaIndexHandler, teaNewSignHandler


def make_app():
    return tornado.web.Application(
        [
            # (r"/",handler name ),
            (r"/", LoginHandler),
            (r"/register", RegisterHandler),
            (r"/showwhiteboard", ShowWhiteboardHandler),
            (r"/whiteboard", WhiteboardHandler),
            (r"/live/userid=(\d+)/roomid=(\d+)", LiveHandler),
            (r"/stulive/userid=(\d+)/roomid=(\d+)", stuLiveHandler),
            (r"/rooms", RoomsHandler),
            (r"/whiteboardIndex", whiteboardIndexHandler),
            (r'/whiteboard', WhiteboardHandler),
            (r'/wstest', wstestHandler),
            (r'/permittest', permitHandler),
            (r'/chat', chatHandler),
            (r'/hand', handHandler),
            (r'/init/', initHandler),

            (r"/stu_index/", stuIndexHandler),
            (r"/stu_sign", stuSignHandler),
            (r"/sign_process", signProcessHandler),
            (r"/tea_check", teaCheckHandler),
            (r"/sign_analyse", signAnalyseHandler),
            (r"/tea_clear", teaClearHandler),
            (r"/tea_index/", teaIndexHandler),
            (r"/tea_new_sign", teaNewSignHandler)
        ],

        template_path='../yantaoshi/flv_tornado/livePlatform/template/',
        static_path='../yantaoshi/flv_tornado/livePlatform/static/',

        debug=True,
        cookie_secret='taoware'
    )


if __name__ == "__main__":
    # start the server on 8888
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
