import tornado
import tornado.web
import tornado.websocket
import json
import torndb_for_python3 as torndb


db = torndb.Connection(
    host='localhost',
    database='live',
    user='root',
    password='111111'
)


class teaIndexHandler(tornado.web.RequestHandler):
    def get(self):
        sno = self.get_argument("username")
        lno = self.get_argument("roomid")
        self.render("tea_stub.html", sno=sno, lno=lno)

    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")
        self.render("tea_stub.html", sno=sno, lno=lno)


class teaCheckHandler(tornado.web.RequestHandler):

    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")

        # 先判断是否开启打卡，否则跳转错误界面
        sql = 'select status from room where roomid = %s;'
        ret = db.query(sql, lno)
        db.close()
        flag = ret[0]['status']
        if flag == 1:
            self.render("tea_check.html", sno=sno, lno=lno)
        else:
            self.render("teaSignError.html", sno=sno,
                        lno=lno, error_message="您尚未发起签到！")


class signAnalyseHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        pass

    def on_message(self, target_lesson_str):
        target_lesson = json.loads(target_lesson_str)

        # 提取要查询课堂id
        lno = target_lesson["lno"]
        sql = 'select * from sign_records where roomid = %s;'
        ret = db.query(sql, lno)
        db.close()

        # 生成出勤者名单
        attend_lst = []
        for i in range(len(ret)):
            attend_lst.append(ret[i]['username'])

        # 从选课表调入学生名单
        sql = 'select * from xk where roomid = %s;'
        ret = db.query(sql, lno)
        db.close()
        all_lst = []
        for i in range(len(ret)):
            all_lst.append(ret[i]['username'])

        # 对比两个名单，记录缺席名单，计算出勤率
        absent_lst = []
        for i in range(len(all_lst)):
            if all_lst[i] not in attend_lst:
                absent_lst.append(all_lst[i])
        attend_rate = float('%.2f' % (len(attend_lst)/len(all_lst)*100))

        # 发送
        attendance_report = {
            'attend_rate': attend_rate,
            'absent_lst': absent_lst
        }
        self.write_message(json.dumps(attendance_report))

    def on_close(self) -> None:
        pass


class teaClearHandler(tornado.web.RequestHandler):
    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")

        # 设置该课程不可打卡
        sql = 'update room set status = %s where roomid = %s;'
        db.execute(sql, 0, lno)
        self.render("tea_stub.html", sno=sno, lno=lno)


class teaNewSignHandler(tornado.web.RequestHandler):
    def post(self):
        sno = self.get_argument("sno")
        lno = self.get_argument("lno")

        # 先判断是否开启打卡，否则跳转错误界面
        sql = 'select status from room where roomid = %s;'
        ret = db.get(sql, lno)
        flag = ret['status']
        if flag == 1:
            self.render("teaSignError.html", sno=sno,
                        lno=lno, error_message="您已发起签到！")
        else:
            # 设置该课程可以打卡
            sql = 'update room set status = %s where roomid = %s;'
            db.execute(sql, 1, lno)
            self.render("tea_success.html", sno=sno, lno=lno)
