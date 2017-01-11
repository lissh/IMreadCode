# -*- coding: utf-8 *-*

import logging
import os
import sys

import tornado

from app import options, log, Application as MyApp
from tornado.ioloop import IOLoop
from tornado.options import options as opts

from app import path
from app.autotask import AutoTask

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == "__main__":
    path.HOME_PATH = os.path.dirname(os.path.realpath(__file__))
    options.setup_options('etc/app.conf')
    app_logger = log.getAppLog()
    app_logger.info("init config")

    http_server = MyApp()
    http_server.listen(opts.port)
    auto_task = AutoTask()
    tornado.ioloop.PeriodicCallback(auto_task.auto_check_task, 1000).start()

    logging.info('Web server listening on %s port.' % opts.port)
    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info('Exiting with keyboard interrupt.')
