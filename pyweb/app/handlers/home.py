# -*- encoding: utf-8 -*-
import json
import re
import urllib

import time
import tornado
from tornado.web import RequestHandler

from app import helpers, options as opts
from tornado.options import options


class BaseHandler(RequestHandler):

    current_user = None
    current_menu = None

    @property
    def r_db(self):
        return self.application.r_db

    @property
    def w_db(self):
        return self.application.w_db

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, action):
        if hasattr(self, action):
            getattr(self, action)()
        else:
            # yield tornado.gen.Task(self.send_error_html, 404, "Action %s is not supported" % action)
            self.send_error_html(404, "Action %s is not supported" % action)

    @tornado.gen.engine
    def get_current_user_async(self, callback):
        user = None
        account = self.get_secure_cookie("current_user") or False
        # account = "admin"
        if not account:
            callback(None)
        else:
            sql = "select * from s_muser where account = %s limit 1"
            callback((yield tornado.gen.Task(self.r_db.get, sql, account)))


    @tornado.gen.engine
    def get_all_menu_async(self, uid, callback):
        if not self.current_user:
            callback(None)
            return
        if uid == 1:
            sql = "select * from s_routes order by fid,ordercount desc"
        else:
            sql = "select * from s_routes where id in(SELECT route_id FROM mdata.s_access where role_id = (select role_id from s_role_user where user_id = %s)) order by fid,ordercount desc" % uid;
        # print sql
        # sql = "select * from s_routes where isshow=1 order by fid,ordercount"
        callback((yield tornado.gen.Task(self.r_db.query, sql, None)))

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace.update({
            'arguments': self.request.arguments,
            'helpers': helpers,
            'options': options,
            'opts': opts,
            'user': self.current_user,
            'menu': self.current_menu,
            'request_uri': self.request.uri,
            'language_choices': opts.get_allowed_languages()
        })
        return namespace

    @tornado.gen.engine
    @tornado.web.asynchronous
    def render(self, template_name, **kwargs):
        kwargs.update({
            'url_path': self.request.uri,
            '_next': self.get_argument('next', ''),
            'opts': opts,
            'options': options,
        })
        super(BaseHandler, self).render(template_name, **kwargs)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def send_error_html(self,code,msg):
        self.clear()
        self.set_status(code)
        if self.get_argument("t", "") == "ajax" or self.get_body_argument("t", "") == "ajax":
            self.write('{"code":"%s","msg":"%s"}'% (code, msg))
            self.flush()
        else:
            self.render("%d.html"%code,code=code, msg=msg)


class HomeHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # sql demo
        # panels = []
        # sql = "select count(*) as counts from s_orderlog where date(reqtime) = '%s' and ((hour(now())-hour(reqtime))*3600+(minute(now())-minute(reqtime))*60+second(now())-second(reqtime))<900 limit 1"
        # orders_count = yield tornado.gen.Task(self.r_db.get, sql, (time.strftime("%Y-%m-%d"),))

        # result = dict(
        #     code = 200,
        #     reason = "ok"
        # )
        # self.write(json.dumps(result))
        # self.flush()
        self.render("home.html")
