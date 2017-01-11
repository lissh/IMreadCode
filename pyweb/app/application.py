# -*- coding: utf-8 *-*
import os

import tornado
from app.helpers import DB
from tornado.options import options as opts

import routes
from app import path


class Application(tornado.web.Application):
    def __init__(self):
        self.r_db = DB(opts.db_r_host,opts.db_r_port,opts.db_r_name,opts.db_r_user,opts.db_r_password)
        self.w_db = DB(opts.db_w_host,opts.db_w_port,opts.db_w_name,opts.db_w_user,opts.db_w_password)
        self.theme_path = os.path.join(opts.themes_directory,opts.selected_theme)
        self.theme_path = os.path.join(path.HOME_PATH, self.theme_path)
        print os.path.join(self.theme_path, 'static')
        settings = {
            'login_url': '/login',
            'static_path': os.path.join(self.theme_path, 'static'),
            'template_path': os.path.join(self.theme_path, 'templates'),
            'xsrf_cookies': True,
            'cookie_secret': opts.cookie_secret,
            'debug': opts.debug
        }

        if opts.static_url_prefix:
            settings['static_url_prefix'] = opts.static_url_prefix
        tornado.web.Application.__init__(self, routes.urls +
                                         [(r"/(favicon\.ico)", tornado.web.StaticFileHandler,{'path': settings['static_path']})], **settings)
