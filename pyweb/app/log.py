# -*- coding: utf-8 -*-
import logging
import logging.config
import os

from tornado.options import options

from app import path


def getAppLog():
    log_path = os.path.join(path.ETC_PATH, options.logging_config_file)
    logging.config.fileConfig(log_path)
    return logging.getLogger(options.logging_config_style)

def getHttpLog():
    log_path = os.path.join(path.ETC_PATH, options.logging_config_file)
    logging.config.fileConfig(log_path)
    return logging.getLogger(options.logging_config_http_style)
