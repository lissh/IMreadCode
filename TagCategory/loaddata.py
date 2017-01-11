#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import MySQLdb

global conn,cursor
host="192.168.0.34"
user="ebook"
passwd="ebook%$amRead"
db='ebook_con'
conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
cursor=conn.cursor()

def arithmeticData(bids,arithmeticid,arithmeticount):
    # print bids
    conn=MySQLdb.connect(host="182.92.184.14",user="cx_fujun",passwd="fjfjie%mysql3",db="ds_read",charset="utf8")
    cursor = conn.cursor()
    bid_sql=str(bids).replace('[','(').replace(']',')')
    if arithmeticid==1:
        arithmetic_sql="select DISTINCT book_id,read_uv/read_pv read_rate from ds_read.prd_bid_c where read_uv>3 and read_pv>30 and book_id in "+bid_sql+' ORDER BY read_uv/read_pv  desc limit '+str(arithmeticount)
    elif arithmeticid==2:
        arithmetic_sql="select DISTINCT book_id,chrg_uv/read_pv chrg_rate from ds_read.prd_bid_c where read_uv>3 and read_pv>30 and book_id in "+bid_sql+' ORDER BY chrg_uv/read_pv desc limit '+str(arithmeticount)

    elif arithmeticid==3:
        arithmetic_sql="select DISTINCT book_id,read_uv/read_pv*0.2+chrg_uv/read_pv*0.8 rc_rate from ds_read.prd_bid_c where read_uv>3 and read_pv>30 and book_id in "+bid_sql+' ORDER BY read_uv/read_pv*0.2+chrg_uv/read_pv*0.8 desc limit '+str(arithmeticount)

    elif arithmeticid==4:
        arithmetic_sql="select DISTINCT book_id,chrg_fee from ds_read.prd_bid_c where read_uv>3 and read_pv>30 and book_id in "+bid_sql+' ORDER BY chrg_fee  desc limit '+str(arithmeticount)

    # elif arithmeticid==5:
    #     arithmetic_sql=""
    else:
        print '该算法还未生成！'
        return []
    n=cursor.execute(arithmetic_sql)
    cbids=[int(row[0]) for row in cursor.fetchall()]

    cbidcount=len(cbids)
    i=0
    while cbidcount<arithmeticount:
        if int(bids[i]) not in cbids:
            cbidcount+=1
            cbids.append(int(bids[i]))
        i+=1
    return cbids





def loadData(categoryid):
    delete_sql="DELETE from ebook_con.con_category_content where category_id="+str(categoryid)
    n=cursor.execute(delete_sql)
    conn.commit()

    selectinfos_sql="select category_tag,arithmetic_id,arithmetic_count,class_id from ebook_con.con_category where category_id="+str(categoryid)
    n=cursor.execute(selectinfos_sql)

    infos= [row for row in cursor.fetchall()]
    categorytags=infos[0][0]
    arithmeticid=infos[0][1]
    arithmeticount=infos[0][2]
    classid=infos[0][3]

    #判断是否添加分类，如果没有添加，则不对分类进行限制
    if classid!=None and classid!='':
        classid_sql="and class_id="+str(int(classid))
    else:
        classid_sql=''

    #判断是否添加标签，如果没有添加，则直接根据在线图书的分类，及class_id获取
    if categorytags!=None and categorytags!='':
        bids_sql="""SELECT DISTINCT aa.* from
                    (SELECT DISTINCT book_id,book_score from  ebook_con.con_book  where book_status=1 """+classid_sql+""" )aa,
                    ( SELECT DISTINCT a.content_id from ebook_con.con_tag_content a,( select tag_id from ebook_con.con_tag where tag_id in ("""+categorytags+""") )  b where a.tag_id = b.tag_id)bb
                    where aa.book_id=bb.content_id ORDER BY aa.book_score desc """
    else:
        bids_sql="SELECT DISTINCT book_id from  ebook_con.con_book  where book_status=1 "+classid_sql+" ORDER BY book_score desc"



    n=cursor.execute(bids_sql)
    bids=[int(row[0]) for row in cursor.fetchall()]
    # arithmeticid=2
    cbids=arithmeticData(bids,arithmeticid,arithmeticount)

    categorycontents=[]
    locationI=0
    for cbid in cbids:
        locationI+=1
        categorycontents+=[(int(categoryid),int(cbid),1,locationI,'333333')]

    print categorycontents
    CategoryContents_sql="INSERT into ebook_con.con_category_content (category_id,content_id,content_type,category_location,font_color) values (%s,%s,%s,%s,%s)"
    n=cursor.executemany(CategoryContents_sql,categorycontents)
    conn.commit()





if __name__ == '__main__':
     loadData(478)
