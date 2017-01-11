# -*- coding: utf-8 -*-
import urllib2
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import requests,MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

class insertbooksheet(object):
    def __init__(self,_host,_user,_passwd,_db):
        self.host=_host
        self.user=_user
        self.passwd=_passwd
        self.db=_db

    def linkSQL(self):
        self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset="utf8") 
        self.cursor = conn.cursor() 

    def updateBookSheet(self,sheetconts):

        try:
            insql='insert into con_booksheet(sheet_id,sheet_name,sheet_brief,create_time,modify_time,online_status,creator_user_id,sheet_type,initial_uv) values (%s,%s,%s,now(),now(),1,0,1,0)'
            n = self.cursor.executemany(insql,sheetconts)
            self.conn.commit()    
        except Exception, e:
            raise e



    def updateBookSheetCont(self,contentids,sheetid):
        try:
            update_book_url="http://readapi.imread.com/api/book/update?source_bid="
            # if len(contentids)==1:
            #     contentids=contentids+contentids
            nsql='select source_bid from con_book where source_bid in '+str(tuple(contentids)).replace(',)',')')
            n = self.cursor.execute(nsql)
            nbids=[]
            for row in self.cursor.fetchall():
                nbids.append(str(row[0]))

            for check in contentids:
                if check not in nbids:
                    url=update_book_url+str(check)
                    r = requests.get(url)
                    print check,r
            bids=[]
            bidslist=[]       
            i=0
            sql='select book_id from con_book where source_bid in '+str(tuple(contentids))


            n = self.cursor.execute(sql)
            for row in self.cursor.fetchall():
                timeRandom = time.time()+random.randint(1,100)
                timeArray = time.localtime(timeRandom)
                createtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                bidslist.append(tuple([str(row[0]),str(createtime)]))
            print bidslist,'???'

            desql="delete from ebook_con.con_booksheet_content where sheet_id="+str(sheetid)+" and content_type='1'"
            
            n = self.cursor.execute(desql)
            self.conn.commit()

            insql="insert into ebook_con.con_booksheet_content(sheet_id,content_id,content_type,create_time) values('"+str(sheetid)+"',%s,'1',%s)"
            # print insql
            n = self.cursor.executemany(insql,bidslist)
            self.conn.commit()

        except Exception,e :
            print e
            return None
