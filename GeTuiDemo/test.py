# -*- coding=utf-8 -*-
#!/bin/env python
__author__ = 'lish'

# import tornado
# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
# import tornado.web
# import tornado.httpclient
# import motor
#
# db = motor.MotorClient().open_sync().test
# class AutoTask(object):
#     def __init__(self):
#         self.r_db = DB(opts.db_r_host,opts.db_r_port,opts.db_r_name,opts.db_r_user,opts.db_r_password)
#         self.w_db = DB(opts.db_w_host,opts.db_w_port,opts.db_w_name,opts.db_w_user,opts.db_w_password)
#
#     # 自动执行的计划任务
#     def auto_check_task(self):
#         #从数据库中取出状态为2的订单
#
#         print "hi~"
#
#
# auto_task = AutoTask()
# tornado.ioloop.PeriodicCallback(auto_task.auto_check_task, 3000).start()



#!/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor
import time
from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)
class SleepHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(2)
    #executor 是局部变量  不是全局的
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # 假如你执行的异步会返回值被继续调用可以这样(只是为了演示),否则直接yield就行
        res = yield self.sleep()
        self.write("when i sleep %s s" % res)
        self.finish()
    @run_on_executor
    def sleep(self):
        time.sleep(5)
        return 5
class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler), (r"/justnow", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
