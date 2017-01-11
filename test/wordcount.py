# -*- coding: utf-8 -*-
__author__ = 'lish'
import imdb
import os,sys
base_path='/opt/www/api/attachment/imread/chapcontent/'
imreaddb=imdb.IMReadDB("100.98.73.21",3306,"ebook","4titbrVcvnP6LSFA")

selectsql='SELECT book_id from ebook_con.con_book where mcp_id is null and source_id=2 and word_count is null'
resultebids=imreaddb.selectdb(selectsql)

for resultebid in resultebids:   
    bid=int(resultebid[0])
    print '正在更新图书bid:%s word_count字段内容！'%bid
    wordcount=0
    selectsql='SELECT chapter_id from ebook_con.con_chapter where book_id=%s'%bid
    resultecids=imreaddb.selectdb(selectsql)
    for resultecid in resultecids:
        cid=int(resultecid[0])
        try:
            chapterpath=base_path+'%s/charpters/%s.txt'%(bid,cid)
            fr=open(chapterpath,'r')
            conts=fr.readlines()

            for cont in conts:
                wordcount+=len(cont.replace('\n','').replace(' ',''))/3
        except:
            continue
    wordcount=str(float(wordcount)/10000)+'万'

    if wordcount!='0.0万':
        updatesql="update ebook_con.con_book set  word_count='%s' where book_id=%s"%(wordcount,bid)
        print updatesql
        imreaddb.updatedb(updatesql)
        print '已经更新图书bid:%s word_count字段内容！'%bid

