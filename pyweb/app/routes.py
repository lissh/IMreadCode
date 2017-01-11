# -*- coding: utf-8 *-*
from tornado.web import url

from app import handlers

urls = [
    url(r"/", handlers.HomeHandler, name='home')
    ]