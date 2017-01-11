# -*- coding: utf-8 -*-
import urllib2
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import requests,MySQLdb
import GenerateSheetCover as gsc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8") 
    cursor = conn.cursor() 
    return conn

def updateBookSheet(sheetconts):

    try:
        insql='insert into con_booksheet(sheet_id,sheet_name,sheet_brief,create_time,modify_time,online_status,creator_user_id,sheet_type,initial_uv) values (%s,%s,%s,now(),now(),1,0,1,0)'
        n = cursor.executemany(insql,sheetconts)
        conn.commit()    
    except Exception, e:
        raise e




def updateBookSheetCont(contentids,sheetid):
    try:
        update_book_url="http://readapi.imread.com/api/book/update?source_bid="
        # if len(contentids)==1:
        #     contentids=contentids+contentids
        nsql='select source_bid from con_book where source_bid in '+str(tuple(contentids)).replace(',)',')')
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
            timeRandom = time.time()+random.randint(1,100)
            timeArray = time.localtime(timeRandom)
            createtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            bidslist.append(tuple([str(row[0]),str(createtime)]))
        print bidslist,'???'

        desql="delete from ebook_con.con_booksheet_content where sheet_id="+str(sheetid)+" and content_type='1'"
        
        n = cursor.execute(desql)
        conn.commit()

        insql="insert into ebook_con.con_booksheet_content(sheet_id,content_id,content_type,create_time) values('"+str(sheetid)+"',%s,'1',%s)"
        # print insql
        n = cursor.executemany(insql,bidslist)
        conn.commit()

    except Exception,e :
        print e
        return None


#更新自有APP中的书单：修真路漫漫和神仙也要谈恋爱  中的图书ID，数据来源：咪咕APP
def booklist():
    try:
        host="100.98.73.21"
        # host="rdsljqv187pt04s68726.mysql.rds.aliyuncs.com"
        user="ebook"
        passwd="4titbrVcvnP6LSFA"
        conn=linkSQL(host,user,passwd,'ebook_con')


        # host="192.168.0.34"
        # user="ebook"
        # passwd="ebook%$amRead"
        # conn=linkSQL(host,user,passwd,'ebook_con')


        mgurl='http://wap.cmread.com/hbc/p/Channelpage.jsp?'
        mgcont = urllib2.urlopen(mgurl).read()
        mgbooklistconts=re.findall('<ul class="textCon textCon4 mB10">[^~]+?<div class="line_hui mT10"><\/div>', mgcont)
        # print len(mgbooklistconts)

        #获取书单信息及书单列表
        sheetconts=[]
        sheetids=['124413']
        for mgbooklistcont in mgbooklistconts:
            # print mgbooklistcont
            sheetconts+=re.findall('.*?std=(\d+).*?<span>(.*?)</span>.*?<p>(.*?)</p>',mgbooklistcont)
            sheetids+=re.findall('.*?std=(\d+)',mgbooklistcont)
        # print sheetids
        #判断是否是新增的书单
        sql ='select sheet_id from con_booksheet where sheet_id in '+str(sheetids).replace('[','(').replace(']',')')
        # print sql
        n = cursor.execute(sql)
        isExistsheetids=[]
        for row in cursor.fetchall():
            isExistsheetids.append(str(row[0]))
        # print isExistsheetids
        newsheetids=list(set(sheetids)-set(isExistsheetids))
        # print newsheetids
        #剔除已经存在的书单
        newsheetconts=[]
        for sheetcont in sheetconts:
            if sheetcont[0] in newsheetids:
                newsheetconts+=[sheetcont]

        # print newsheetconts

        #更新con_booksheet表
        updateBookSheet(newsheetconts)

        #更新con_booksheet_content表
        for sheetid in newsheetids:
            print sheetid
            bids=[]
            for page in range(1,10):

                url = 'http://wap.cmread.com/hbc/f/sheetDetail?page='+str(page)+'&std='+str(sheetid)
                # print url
                content = urllib2.urlopen(url).read()
                tbids=re.findall('/hbc/cover_file/\d+/(\d+)/\d+/cover', content)

                if tbids[0] not in bids :
                    bids+=tbids
                else:
                    break
            print bids,'?@@@'
            updateBookSheetCont(bids,sheetid)
            time.sleep(1)
            gsc.mergepicture(sheetid)


        print 'mgboolist,ok !'
    except Exception,e :
        print e
        return None


if __name__ == '__main__':
    booklist()



