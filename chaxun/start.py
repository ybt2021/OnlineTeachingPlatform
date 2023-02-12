import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb_for_python3 as torndb

db = torndb.Connection(
    host='localhost',
    database='live',
    user='root',
    password='111111'
)


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class backHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("index.html")


class stuHandler(tornado.web.RequestHandler):
    def post(self):
        stuid = self.get_argument("stuid")
        sql1 = "select * from attendency where username = %s;"
        ret1 = db.query(sql1, stuid)
        sql2 = "select * from attendency where username = %s and status = 'attend';"
        ret2 = db.query(sql2, stuid)
        db.close()
        rate = float('%.2f' % (len(ret2)/len(ret1)*100))
        self.render("stu.html", stuid=stuid, rate=rate)


class clsHandler(tornado.web.RequestHandler):
    def post(self):
        clsid = self.get_argument("clsid")
        sql1 = "select * from attendency where roomid = %s;"
        ret1 = db.query(sql1, clsid)
        sql2 = "select * from attendency where roomid = %s and status = 'attend';"
        ret2 = db.query(sql2, clsid)
        db.close()
        rate = float('%.2f' % (len(ret2)/len(ret1)*100))
        self.render("cls.html", clsid=clsid, rate=rate)


class teaHandler(tornado.web.RequestHandler):
    def post(self):
        teaid = self.get_argument("teaid")
        sql = "select * from score where teaid = %s;"
        ret = db.query(sql, teaid)
        db.close()
        total = 0
        for i in range(len(ret)):
            total += ret[i]['score']
        score = float('%.2f' % (total/len(ret)))
        self.render("tea.html", teaid=teaid, score=score)


class scoreHandler(tornado.web.RequestHandler):
    def post(self):
        targetid = self.get_argument("targetid")
        score = self.get_argument("score")
        sql = "insert into score (teaid,score) values(%s,%s);"
        db.execute(sql, targetid, score)
        db.close()
        self.render("score.html")


def make_app():
    return tornado.web.Application(
        [
            (r"/", indexHandler),
            (r"/stu", stuHandler),
            (r"/cls", clsHandler),
            (r"/tea", teaHandler),
            (r"/score", scoreHandler),
            (r"/back", backHandler),
        ],

        template_path='../chaxun/',
        static_path='../chaxun/',
    )


if __name__ == "__main__":
    # start the server on 8888
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
