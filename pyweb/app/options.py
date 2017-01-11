# -*- coding: utf-8 *-*
import base64
import logging
import os

import tornado.locale

from tornado.options import (define, options, parse_command_line, parse_config_file)

def get_allowed_languages():
    return sorted([(k, v['name_en']) for k, v in
        list(tornado.locale.LOCALE_NAMES.items()) if k in
        tornado.locale.get_supported_locales()])

def define_options():
    #Tornado
    group = 'Tornado'
    define("use_pyuv", default=False, type=bool, help=('Configure IOLoop for using libuv, needs tornado_pyuv ' 'installed; useful on Windows environments.'), group=group)
    #HTTP Server
    group = 'HTTP Server'
    define("port", default=8004, type=int, help='HTTP server port', group=group)

    #Site
    group = 'Site'
    define('base_url', default='http://127.0.0.1:8004', type=str, help='Base URL', group=group)
    define('title', default='', type=str, help='Site title', group=group)

    #Database
    group = 'Database'
    define("db_r_host", default="localhost", type=str,help='MySQL database Host', group=group)
    define("db_r_port", default="3306", type=int,help='MySQL database Port', group=group)
    define("db_r_name", default="mdata", type=str, help='MySQL database name', group=group)
    define("db_r_user", default="root", type=str, help='MySQL database user',group=group)
    define("db_r_password", default="root", type=str,help='MySQL database password',group=group)

    define("db_w_host", default="localhost", type=str,help='MySQL database Host', group=group)
    define("db_w_port", default="3306", type=int,help='MySQL database Port', group=group)
    define("db_w_name", default="mdata", type=str, help='MySQL database name', group=group)
    define("db_w_user", default="root", type=str, help='MySQL database user',group=group)
    define("db_w_password", default="root", type=str,help='MySQL database password',group=group)

    # Cache
    group = 'Cache'
    define("redis_host", default="localhost", type=str,help='Redis database Host', group=group)
    define("redis_port", default=6379, type=str,help='Redis database Port', group=group)
    define("redis_db", default=1, type=str, help='Redis database name', group=group)
    define("redis_pre", default="mdata_", type=str, help='Redis database name', group=group)

    #Application
    group = 'Application'
    define('cookie_secret', default='', type=str, group=group)
    define("debug", default=False, type=bool, help=('Turn on autoreload, log to stderr only'), group=group)
    define("autoreload", default=True, type=bool, help=('Turn on autoreload, log to stderr only'), group=group)
    define('themes_directory', default='themes', type=str, help='Themes directory name', group=group)
    define('selected_theme', default='default', type=str, help='Selected theme directory name', group=group)
    define('static_url_prefix', default=None, type=str, help='Static files prefix', group=group)
    define('logging_config_file', default="log.conf", type=bool, help='logging config file', group=group)
    define('logging_config_style', default="simple", type=bool, help='logging config style', group=group)
    define('logging_config_http_style', default="logger_tornado.access", type=bool, help='logging config http style', group=group)



def setup_options(path):
    """Must be called before to starting the application. For security
    propuses, it will set a random cookie secret."""
    define_options()
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),path)
    if os.path.exists(path):
        parse_config_file(path)
    else:
        raise ValueError('No config file at %s' % path)
    parse_command_line()
    if not options.cookie_secret:
        options.cookie_secret = base64.b64encode(os.urandom(32))
        logging.warning('System will use a random cookie_secret: %s' % options.cookie_secret)
    return options