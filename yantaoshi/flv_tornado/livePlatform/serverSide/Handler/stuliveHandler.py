import tornado.web
import tornado.ioloop
# from tornado.options import define, options, parse_command_line
import tornado.websocket

import torndb_for_python3 as torndb


db = torndb.Connection(
    host='localhost',
    database='live',
    user='root',
    password='111111'
)


class stuLiveHandler(tornado.web.RequestHandler):
    def get(self, userid, roomid):
        # error = ''
        sql = 'select username from user where userid = %s'
        ret = db.get(sql, userid)
        username = ret['username']
        db.close()
        self.render('stulive.html', userid=userid,
                    roomid=roomid, username=username)
