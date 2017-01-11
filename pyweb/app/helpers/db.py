# -*- coding: utf-8 *-*
import hashlib
import logging
import pickle
import re
import urllib
import warnings

import sys
import tormysql
import tornado
from tornado import gen
from tornado.concurrent import is_future
from tornado.options import options as opts

def query_finish(result):
    return result


class DB():
    def __init__(self, _host, _port, _db, _db_user, _db_password):
        self.pool = None
        self.logger = logging.getLogger('database')
        self.host = _host
        self.port = _port
        self.db = _db
        self.db_user = _db_user
        self.db_password = _db_password
        self.init()

    def init(self):
        self.pool = tormysql.ConnectionPool(
            max_connections=20,  # max open connections
            idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
            wait_connection_timeout=3,  # wait connection timeout
            host=self.host,
            user=self.db_user,
            passwd=self.db_password,
            db=self.db,
            charset="utf8",
            cursorclass=tormysql.cursor.OriginDictCursor
        )

    @tornado.gen.engine
    def query(self, sql, params, callback):
        # sql = self.clean_sql(sql,params)
        try:
            if self.pool.closed:
                self.init()
            with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    yield cursor.execute(sql)
                    datas = cursor.fetchall()
            # print datas
            callback(query_finish(datas))
            yield self.pool.close()
        except:
            callback(None)

    @tornado.gen.engine
    def get(self, sql, params, callback):
        print callback.__name__
        sql = self.clean_sql(sql,params)
        print sql
        try:
            if self.pool.closed:
                self.init()
            with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    yield cursor.execute(sql)
                    datas = cursor.fetchone()
                    if isinstance(datas,list):
                        datas = datas[0]
                    callback(query_finish(datas))
            yield self.pool.close()
        except:
            callback(None)

    @tornado.gen.engine
    def update_by_dict(self, tablename, idname, rowdict, callback):
        if self.pool.closed:
            self.init()
        try:
            with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    yield cursor.execute("describe %s" % tablename)
                    field_list =  cursor.fetchall()
                    allowed_keys = set(row["Field"] for row in field_list)
                    keys = allowed_keys.intersection(rowdict)
                    # if len(rowdict) > len(keys):
                    #     unknown_keys = set(rowdict) - allowed_keys
                    #     logging.error("skipping keys: %s", ", ".join(unknown_keys))

                    update_list = []
                    for key in keys:
                        if(key == idname):continue
                        update_list.append("%s ='%s'" % (key, self.to_string(rowdict[key])))
                    update_str = ", ".join(update_list)
                    print update_str
                    sql = "Update %s set %s where %s = '%s'" %(tablename,update_str,idname,rowdict[idname])
                    print sql
                    yield cursor.execute(sql)
        except:
            yield conn.rollback()
        else:
            yield conn.commit()
        callback(None)


    def escape_str(self, str):
        str = tornado.escape.utf8(str)
        str = str.replace(" or ", "")
        str = str.replace(" and ", "")
        str = str.replace("'","\\'")
        return str.replace('%', '%%')

    def clean_sql(self,sql, _params):
        if not _params:
            return sql
        if isinstance(_params, str):
            _params = "'%s'" % self.to_string(_params)
            sql = sql % _params
        else:
            params = []
            values = []
            for param in _params:
                params.append(self.to_string(param))
            print params
            if values:
                params = ', '.join(values)
                sql = sql % params[1:-1]
            else:
                sql = sql % tuple(params)

        return sql

    def to_string(self,temp):
        if isinstance(temp, basestring):
            return self.escape_str(temp)
        else:
            return str(temp)


