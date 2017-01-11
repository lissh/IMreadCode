#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import MySQLdb

global conn,cursor
host="100.98.73.21"
user="ebook"
passwd="4titbrVcvnP6LSFA"
db='ebook_con'
conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
cursor=conn.cursor()


def loadData():
    selectinfos_sql="select category_id,category_tag from ebook_con.con_category where parent_category_id in (434,435) and category_tag <>''"
    n=cursor.execute(selectinfos_sql)


    for row in cursor.fetchall():
        categoryid=row[0]
        delete_sql="DELETE from ebook_con.con_category_content where category_id="+str(categoryid)
        n=cursor.execute(delete_sql)
        conn.commit()
        # print delete_sql
        categorytags=row[1]
        tags_sql='"'+categorytags.replace(',','","')+'"'
        print tags_sql
        bids_sql="""SELECT DISTINCT aa.* from
                    (select DISTINCT b.book_id from public_db.mg_book_ordfee a, ebook_con.con_book b where a.book_id=b.source_bid and b.book_status=1 order by a.ord_fee desc)aa,
                    (select DISTINCT a.content_id from ebook_con.con_tag_content a,( select tag_id from ebook_con.con_tag where tag_name in ("""+tags_sql+""") )  b where a.tag_id = b.tag_id)bb
                    where aa.book_id=bb.content_id"""
        n=cursor.execute(bids_sql)
        categorycontents=[]
        locationI=0
        for row in cursor.fetchall():
            locationI+=1
            categorycontents+=[(int(categoryid),int(row[0]),1,locationI,'333333')]
        print categorycontents
        CategoryContents_sql="INSERT into ebook_con.con_category_content (category_id,content_id,content_type,category_location,font_color) values (%s,%s,%s,%s,%s)"
        n=cursor.executemany(CategoryContents_sql,categorycontents)
        conn.commit()


if __name__ == '__main__':
     loadData()