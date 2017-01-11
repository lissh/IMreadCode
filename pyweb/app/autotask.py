# -*- coding: utf-8 *-*
import sys
sys.path.append('/Users/lish/PycharmProjects/pyweb/hive')
from tornado.options import options as opts
from app import DB
import pandas as pd
# from pandas import Series,DataFrame
from pandas import *
import tornado,time
import vote
from hive import hiveDB






class AutoTask(object):
    def __init__(self):
        self.r_db = DB(opts.db_r_host,opts.db_r_port,opts.db_r_name,opts.db_r_user,opts.db_r_password)
        self.w_db = DB(opts.db_w_host,opts.db_w_port,opts.db_w_name,opts.db_w_user,opts.db_w_password)
        self.r_hivedb=hiveDB('182.92.183.76',9084)

    def todf(self,para):
        self.df = DataFrame(para)
        # return self.df


    # 自动执行的计划任务
    def auto_check_task(self):
        vote.vote(1967)
        # # #从mysql数据库中取出数据
        # sql = "SELECT * from dim.dim_book_label limit 10000"
        # self.r_db.query(sql,None,self.todf)
        # bookdf=self.df
        # # print '?1', bookdf
        #
        # #从hive数据库中取出数据
        # vars_hql='desc dmn.us_am_uid_tag'
        # hql = 'select * from dmn.us_am_uid_tag'
        # self.r_hivedb.query(vars_hql,hql,self.todf)
        # userdf= self.df
        # # print '?2',userdf
        #
        # for user_id,ugroup in userdf.groupby('user_id'):
        #     tt={'userid':'','book_id':'','maxboookvalue':0}
        #     userid=user_id
        #     usertagsvalues=ugroup[['tag_id','read_pot']]
        #
        #
        #     maxboookvalue=0
        #     result = pd.concat([usertagsvalues,bookdf], axis=1)
        #     for book_id,bgroup in result.groupby('book_id'):
        #         book_values=0
        #         bookid=book_id
        #         bookpots=bgroup['read_pot']
        #         for bookpot in bookpots:
        #             book_values+=float(bookpot)
        #
        #         # print '?1',bookid
        #         # print '?2',book_values
        #
        #         if book_values>maxboookvalue:
        #             tt={'userid':userid,'book_id':bookid,'maxboookvalue':float(book_values)}
        #
        #     print tt

        print "hi~"

if __name__ == '__main__':
    app=AutoTask()
    app.auto_check_task()


