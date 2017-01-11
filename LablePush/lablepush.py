# -*- coding: utf-8 *-*
import sys
sys.path.append('/Users/lish/PycharmProjects/LablePush/hive')
from hive import hiveDB
from igt_push import *
from igetui.igt_message import *
from BatchImpl import *

# toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'true'


global APPKEY,APPID,MASTERSECRET,HOST
APPKEY = "koOb7dOrV46y5XOHuH9pH9"
APPID = "Er1g7mLQUS6pToymO5bBK6"
MASTERSECRET = "JDQgdIzrapA0NShuqv2YZ8"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'



class HiveQuery(object):
    def __init__(self):
        self.r_hivedb=hiveDB('182.92.183.76',9084)

    def todf(self,hresulte):
        records={}
        keys=[]
        for row in  hresulte:
            uuid_tag=row.split('\t')
            key=uuid_tag[0]
            value=uuid_tag[1].decode('string_escape')
            # print value
            # key='f03811f9da177af413accebe96575ad2'
            if key not in keys:
                keys+=[key]
                records[key]=[]
            records[key]+=[value]
        self.ddict=records

    def query_task(self):
        #从hive数据库中取出数据
        statday=time.strftime('%Y%m%d',time.localtime(time.time() - 24*60*60) )
        # print statday
        hsql="select client_id,tag_name from  dmn.us_am_client_tag where stat_day=%s"%statday
        self.r_hivedb.query(hsql,self.todf)
        clienttags= self.ddict
        return clienttags


class Tagtask():
    def __init__(self,alias='请输入别名'):
        self.APPKEY = "koOb7dOrV46y5XOHuH9pH9"
        self.APPID = "Er1g7mLQUS6pToymO5bBK6"
        self.MASTERSECRET = "JDQgdIzrapA0NShuqv2YZ8"
        self.HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

    # 根据clientid设置标签功能
    def setTag(self,CID,TagList):
        push = IGeTui(self.HOST, self.APPKEY, self.MASTERSECRET)
        print push.setClientTag(self.APPID, CID, TagList)

    # 根据clientid查询标签
    def getUserTagsTest(self,CID):
        push = IGeTui(self.HOST, self.APPKEY, self.MASTERSECRET)
        dictz = push.getUserTags(self.APPID, CID)
        for key in dictz:
            print key + ":" + dictz[key].decode("utf-8")

    def httpPosttest(self,):
        params={'asdfs':'afdf'}
        push = IGeTui(self.HOST, self.APPKEY, self.MASTERSECRET)
        test=push.httpPost(self.host,params)


if __name__ == '__main__':

    hivequery=HiveQuery()
    queryresults=hivequery.query_task()
    app=Tagtask()
    app.httpPosttest()

    # for key, value in queryresults.items():
    #     CID=key
    #     taglist=value
    #     if CID!='' and taglist!='':
    #         # print CID,taglist
    #         try:
    #             app.setTag(CID,taglist)
    #             app.getUserTagsTest(CID)
    #
    #         except Exception,e :
    #             print e

