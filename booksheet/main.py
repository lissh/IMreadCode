# -*- coding: utf-8 -*-
__author__ = 'lish'
from insertBSheet import insertbooksheet as insertbs
import urllib2,bs4,re
import urllib2
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import requests,MySQLdb
import GenerateSheetCover as gsc
import sys
reload(sys)
sys.setdefaultencoding('utf8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8")
    cursor = conn.cursor()
    return conn

def updateBookSheet(sheetconts):

    try:
        # print sheetconts
        insql='insert into con_booksheet(sheet_id,sheet_name,content_cnt,sheet_brief,create_time,online_status,creator_user_id,sheet_type,initial_uv) values (%s,%s,0,%s,now(),1,0,1,0)'
        n = cursor.executemany(insql,sheetconts)
        conn.commit()
    except Exception, e:
        raise e




def updateBookSheetCont(contentids,sheetid):
    try:
        update_book_url="http://readapi.imread.com/api/book/update?source_bid="
        if len(contentids)==1:
            contentids=contentids+contentids
        nsql='select source_bid from con_book where source_bid in '+str(tuple(contentids)).replace("',)","')")
        n = cursor.execute(nsql)
        nbids=[]
        for row in cursor.fetchall():
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

        n = cursor.execute(sql)
        for row in cursor.fetchall():
            create_time=str(time.strftime('%Y-%m-%d %H:%m:',time.localtime(time.time())))+str(random.randint(10,59))
            bidslist.append(tuple([sheetid,str(row[0]),create_time]))
        # print bidslist,'???'

        desql="delete from ebook_con.con_booksheet_content where sheet_id="+str(sheetid)+" and content_type='1'"

        n = cursor.execute(desql)
        conn.commit()

        insql="insert into ebook_con.con_booksheet_content(sheet_id,content_id,content_type,create_time) values(%s,%s,1,%s)"
        n = cursor.executemany(insql,bidslist)
        conn.commit()

    except Exception,e :
        print e
        return None



def booklist():
    host="100.98.73.21"
    # host="rdsljqv187pt04s68726.mysql.rds.aliyuncs.com"
    user="ebook"
    passwd="4titbrVcvnP6LSFA"
    conn=linkSQL(host,user,passwd,'ebook_con')

    # tt=insertbs("192.168.0.34","ebook","ebook%$amRead",'ebook_con')
    headers={
            'Host':"www.cmread.com",
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
            'Accept':"application/json, text/javascript, */*; q=0.01",
            'Content-Type':"application/x-www-form-urlencoded",
            'X-Requested-With':"XMLHttpRequest",
            # 'Referer':"http://www.cmread.com/u/bookSheetSquare",
            'Connection':"keep-alive"
            }

    mgurl='http://www.cmread.com/u/bookSheetSquare'
    req=urllib2.Request(mgurl,headers = headers)
    mgcont = urllib2.urlopen(req).read()
    soup=bs4.BeautifulSoup(mgcont,'lxml')
    MostsharedCont=soup.findAll('div',{'id':"main_down_div_1"})[0]
    sheetconts=[]
    sheetids=['124413']
    for para in MostsharedCont.findAll('a',{'style':"cursor:pointer;"}):
        sheetid=re.findall('/u/bookSheet/(\d+)',para['href'])[0]
        title= para.h1.findAll('div')[0].text
        brief= para.p['title']
        sheetids+=[sheetid]
        sheetconts+=[(sheetid,title,brief)]

    #判断是否是新增的书单
    sql ='select sheet_id from con_booksheet where sheet_id in '+str(sheetids).replace('[','(').replace(']',')')

    n = cursor.execute(sql)
    isExistsheetids=[]
    for row in cursor.fetchall():
        isExistsheetids.append(str(row[0]))
    # print isExistsheetids
    newsheetids=list(set(sheetids)-set(isExistsheetids))
    print '需要更新的图书书单列表:',newsheetids
    #剔除已经存在的书单
    newsheetconts=[]
    for sheetcont in sheetconts:
        if sheetcont[0] in newsheetids:
            newsheetconts+=[sheetcont]
    # print newsheetconts

    #更新con_booksheet表
    updateBookSheet(newsheetconts)

    for sheetid in sheetids:
        if sheetid!=None or sheetid!='':
            bids=[]
            for page in range(1,10):

                url = 'http://wap.cmread.com/hbc/f/sheetDetail?page='+str(page)+'&std='+str(sheetid)
                # print url
                content = urllib2.urlopen(url).read()
                tbids=re.findall('/hbc/cover_file/\d+/(\d+)/\d+/cover', content)
                # print tbids
                try:
                    if tbids[0] not in bids :
                        bids+=tbids
                    else:
                        break
                except Exception,e :
                    print e
            updateBookSheetCont(bids,sheetid)
            gsc.mergepicture(sheetid)
        print bids


if __name__ == '__main__':
    booklist()


