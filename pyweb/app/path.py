# -*- coding:utf-8 -*-
import os

HOME_PATH = os.path.dirname(os.path.realpath(__file__))
if HOME_PATH.endswith("/app"):
    HOME_PATH = HOME_PATH.strip("app")
print HOME_PATH
ETC_PATH = os.path.join(HOME_PATH, 'etc')
