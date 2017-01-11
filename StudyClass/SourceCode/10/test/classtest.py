# -*- coding: utf-8 -*-
import random
import re,json,os,time
import requests,MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]




#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8") 
    cursor = conn.cursor() 
    return conn



class UpdateBooks(object):

    def linkSQL(self,host,user,passwd,db):
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8")
        cursor = conn.cursor()
        return conn



    def checkbookbids(self,category_books):

        update_book_url="http://readapi.imread.com/api/book/update?source_bid="
        if len(category_books)==1:
            category_books=category_books+category_books
        nsql='select source_bid from con_book where source_bid in '+str(tuple(category_books))
        n = cursor.execute(nsql)
        nbids=[]
        for row in cursor.fetchall():
            nbids.append(str(row[0]))

        category_books=list(set(category_books))
        nbids=list(set(nbids))
        for check in category_books:
            if check not in nbids:
                url=update_book_url+str(check)
                r = requests.get(url,timeout=5)
                print check,r   
        return category_books

    def getbookids(self,category_books):
        bids=[]
        bidslist=[]
        i=0
        sql='select book_id from con_book where source_bid in '+str(tuple(category_books)).replace(',)',')')

        n = cursor.execute(sql)
        for row in cursor.fetchall():
            bidslist.append(str(row[0]))
        bidslist = list(set(bidslist))
        random.shuffle(bidslist)

        for bid in bidslist:
            i+=1
            bids.append(tuple([str(bid)]+[str(i)]))
        return bids

    def clearcategorycont(self,category_id):

        desql="delete from ebook_con.con_category_content where category_id='"+str(category_id)+"' and content_type='1'"
        n = cursor.execute(desql)
        conn.commit()


    def addcategorycont(self,category_id,bids):
        insql="insert into ebook_con.con_category_content(category_id,content_id,content_type,category_location,font_color) values('"+str(category_id)+"',%s,'1',%s,'333333')"
        if len(bids)==1:
            n = cursor.execute(insql,bids[0])
            conn.commit()
        elif len(bids)==0:
            print 'Has not extracted bids !!!'
        else:
            n = cursor.executemany(insql,bids)
            conn.commit()






def dealMRZsdk():
    try:
        global conn
        host="192.168.0.34"
        user="ebook"
        passwd="ebook%$amRead"
        conn=linkSQL(host,user,passwd,'ebook_con')

        category_books=['374609284','374662977','374830916']
        category_id=412
        x=UpdateBooks()
        category_books=x.checkbooks(category_books)
        bids=x.getbookids(category_books)
        x.clearbookids(category_id)
        x.addbookids(category_id,bids)
        print 'dealMRZsdk,ok !'
    except Exception,e :
        print e

if __name__ == '__main__':
    dealMRZsdk()
