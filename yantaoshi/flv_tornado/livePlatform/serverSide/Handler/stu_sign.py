import tornado
import tornado.web
import torndb_for_python3 as torndb


db = torndb.Connection(
    host='localhost',
    database='live',
    user='root',
    password='111111'
)


class stuIndexHandler(tornado.web.RequestHandler):
    def get(self):
        sno = self.get_argument("username")
        lno = self.get_argument("roomid")
        self.render("stu_stub.html", sno=sno, lno=lno)

    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")
        self.render("stu_stub.html", sno=sno, lno=lno)


class stuSignHandler(tornado.web.RequestHandler):
    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")

        # 先判断是否开启打卡，否则跳转错误界面
        sql = 'select status from room where roomid = %s;'
        ret = db.query(sql, lno)
        db.close()
        flag = ret[0]['status']
        if flag == 1:
            self.render("stu_sign.html", sno=sno, lno=lno)
        else:
            self.render("stuSignError.html", sno=sno, lno=lno,
                        error_message="现在不是签到时间！")


class signProcessHandler(tornado.web.RequestHandler):
    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")
        # 写入数据库，sign_records表存放学生签到记录

        # 先判断是否已经打过卡
        sql = 'select * from sign_records where username = %s and roomid = %s;'
        ret = db.get(sql, sno, lno)
        db.close()
        if (ret == None):
            sql = 'insert into sign_records(username,roomid) values(%s,%s);'
            db.execute(sql, sno, lno)
            db.close()
            self.render("stu_success.html", sno=sno, lno=lno)
        else:
            db.close()
            self.render("stuSignError.html", sno=sno, lno=lno,
                        error_message="你已签到，请不要重复签到！")
