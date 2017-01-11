# -*- coding: utf-8 -*-
__author__ = 'lish'
from multiprocessing.dummy import Pool as ThreadPool
from IMOpenAPI import imxmlapi as imxml
import imdb
import ConfigParser
import os

global mcpid,base_url,base_path,apiurls
cf = ConfigParser.ConfigParser()
cf.read("imopenapi.conf")
mcpid = cf.getint("mcp", "ym_mcpid")
base_url = cf.get("prefixurl", "base_url")
base_path = cf.get("prefixpath", "base_path")
apiurls=dict(
    bookinfos=cf.get("ym_apiurl", "bookinfos"),
    bookchapterids=cf.get("ym_apiurl", "bookchapterids"),
    bookchaptercont=cf.get("ym_apiurl", "bookchaptercont"),
    bookids=cf.get("ym_apiurl", "bookids"),
    bookcategorys=cf.get("ym_apiurl", "bookcategorys")
    )

db_port = cf.getint("db", "db_port")
db_user = cf.get("db", "db_user")
db_host = cf.get("db", "db_host")
db_pass = cf.get("db", "db_pass")
imreaddb=imdb.IMReadDB(db_host,db_port,db_user,db_pass)




def addbooks(isNewSids,mcpid):
    for sbid in isNewSids:
        ###清空临时章节表数据
        truncatesql='TRUNCATE TABLE public_db.con_own_tmpchapter'
        imreaddb.truncatedb(truncatesql)
        ###清空public_db.con_own_tmpbook，并将接口获得的新图书内容插入public_db.con_own_tmpbook表格
        truncatesql='TRUNCATE TABLE public_db.con_own_tmpbook'
        imreaddb.truncatedb(truncatesql)
        try:
            print '正在解析图书sbid:%s的图书信息'%sbid
            bookinfos=yuemingapp.BookInfos(sbid,mcpid)
            # print bookinfos

            insertsql='insert into public_db.con_own_tmpbook (mcp_id,source_bid,book_name,author_name,book_brief,class_id,class_name,book_status,key_word,image_url,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,score,last_update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,[tuple(bookinfos)])
            ###将con_own_tmpbook更新到con_book中
            insertsql="""INSERT ebook_con.con_book (mcp_id,source_bid,book_name,author_name,book_brief,class_id,class_name,book_tag,big_thumb,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,book_score,modify_time,source_id,book_status)
                                            SELECT mcp_id,source_bid,book_name,author_name,book_brief,class_id,class_name,key_word,image_url,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,score,last_update_time,2,0 FROM public_db.con_own_tmpbook
                        """
            imreaddb.insertdb(insertsql)

            ###获得图书的bid
            selectsql='select source_bid,book_id,big_thumb from ebook_con.con_book where mcp_id=%s and source_bid=%s'%(mcpid,sbid)
            keydata=imreaddb.selectdb(selectsql)[0]

   
            sbid=keydata[0]
            bid=keydata[1]
            imageurl=keydata[2]
            print '正在处理新增图书sbid:%s,bid:%s！'%(sbid,bid)

            ###下载图片，并更新con_book中的big_thum字段
            imdb.cutpicture(bid,imageurl,200,250)
            bigthum=base_url+str(bid)+'/cover/cover'+str(bid)+'b.jpg'
            updatesql='UPDATE ebook_con.con_book set big_thumb=\'%s\' WHERE book_id=%s'%(bigthum,bid)
            imreaddb.updatedb(updatesql)

            ###获取该本图书章节信息列表
            chaptersinfos=yuemingapp.BookChapterIds(sbid,bid)

            ###将章节数据插入临时章节表
            insertsql='insert into con_own_tmpchapter (source_bid,book_id,chapter_id,chapter_name,price_type,chapter_rank) VALUES (%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,chaptersinfos)
            ###创建服务器章节存放数据
            chapterpath=base_path+'%s/charpters/'%(bid)
            isExists=os.path.exists(chapterpath)
            if not isExists:
                os.makedirs(chapterpath)
            # print chaptersinfos
            ###获取章节内容并存放在服务器指定路径下
            # 用线程池进行快速订购bookLoadsUrls
            pool = ThreadPool(3)
            results = pool.map(yuemingapp.BookChapterCont,chaptersinfos)
            pool.close()
            pool.join()
            ###将更新的图书上线
            updatesql='UPDATE ebook_con.con_book set book_status=2 WHERE book_id=%s'%bid
            imreaddb.updatedb(updatesql)
            print '成功新增图书sbid:%s,bid:%s！'%(sbid,bid)

            ###将临时章节表的数据插入正式库章节表
            insertsql="""INSERT ebook_con.con_chapter (book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,source_id)
                                                    SELECT book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,2 FROM public_db.con_own_tmpchapter
                            """
            imreaddb.updatedb(insertsql)


        except Exception, e:
            print e


def renewbooks(isOldSids,mcpid):
    ###清空临时章节表数据
    truncatesql='TRUNCATE TABLE public_db.con_own_tmpchapter'
    imreaddb.truncatedb(truncatesql)

    selectsql='select source_bid,book_id from ebook_con.con_book where mcp_id=%s and serialize_status=0 and source_bid in '%mcpid+str(tuple(isOldSids)).replace(',)',')')
    keydatalist=imreaddb.selectdb(selectsql)

    for keydata in keydatalist:
        sbid=keydata[0]
        bid=keydata[1]
        print '正在处理更新图书sbid:%s,bid:%s！'%(sbid,bid)
        ###获取该本图书章节信息列表
        chaptersinfos=yuemingapp.BookChapterIds(sbid,bid)

        selectsql='select chapter_id from ebook_con.con_chapter where book_id=%s'%bid
        results=imreaddb.selectdb(selectsql)
        isOldCids=[]
        for result in results:
            isOldCids.append(str(result[0]))


        isNewchaptersinfos=[]
        for chapterinfos in chaptersinfos:
            # print str(chapterinfos[2])
            if str(chapterinfos[2]) not in isOldCids:
                isNewchaptersinfos.append(chapterinfos)

        ###将章节数据插入临时章节表
        if isNewchaptersinfos !=[]:
            insertsql='insert into con_own_tmpchapter (source_bid,book_id,chapter_id,chapter_name,price_type,chapter_rank) VALUES (%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,isNewchaptersinfos)

            ###创建服务器章节存放数据
            chapterpath=base_path+'%s/charpters/'%(bid)
            isExists=os.path.exists(chapterpath)
            if not isExists:
                os.makedirs(chapterpath)
            ###获取章节内容并存放在服务器指定路径下
            # 用线程池进行快速订购bookLoadsUrls
            pool = ThreadPool(3)
            results = pool.map(yuemingapp.BookChapterCont,isNewchaptersinfos)
            pool.close()
            pool.join()
            print '成功更新图书sbid:%s,bid:%s！'%(sbid,bid)
        else:
            print '图书sbid:%s,bid:%s暂无更新！'%(sbid,bid)


    ###将临时章节表的数据插入正式库章节表
    insertsql="""INSERT ebook_con.con_chapter (book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank)
                                        SELECT book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank FROM public_db.con_own_tmpchapter
                """
    imreaddb.insertdb(insertsql)





if __name__ == '__main__':
    yuemingapp=imxml.IMxmlAPI(apiurls)

    ##第一次插入分类
    # bookcategorys=yuemingapp.BookCategorys()
    # categoryinfos=[]
    # for key,value in bookcategorys.items():
    #     categoryinfos.append((int(mcpid),int(key),value))
    # insertsql='INSERT ebook_con.con_class_mcp (mcp_id,mcp_class_id,mcp_class_name) values (%s,%s,%s)'
    # imreaddb.insertdb(insertsql,categoryinfos)
    # print categoryinfos


    bids=yuemingapp.BookIds()
    selectsql='select source_bid from ebook_con.con_book where mcp_id=%s'%mcpid
    isOldSids=[]
    results=imreaddb.selectdb(selectsql)
    for result in results:
        isOldSids.append(str(result[0]))
    isNewSids=list(set(bids)-set(isOldSids))


    if isOldSids!=[]:
        renewbooks(isOldSids,mcpid)
    if isNewSids!=[]:
        addbooks(isNewSids,mcpid)

    updatesql="""UPDATE ebook_con.con_book a
                JOIN (
                    SELECT book_id, min(chapter_id) f_chpater_id, max(chapter_id) l_chpater_id
                    FROM ebook_con.con_chapter GROUP BY book_id ) b
                ON (a.book_id = b.book_id)
                SET
                  first_chpater_id = b.f_chpater_id,
                  last_chapter_id=b.l_chpater_id
                WHERE
                    a.source_id=2 and a.mcp_id=%s"""%mcpid
    imreaddb.updatedb(updatesql)



