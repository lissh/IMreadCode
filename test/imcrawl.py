# -*- coding: utf-8 -*-
__author__ = 'lish'
from multiprocessing.dummy import Pool as ThreadPool
from PIL import Image
import urllib2
import ConfigParser
import sys,io,os
reload(sys)
sys.setdefaultencoding('utf-8')

global mcpid,base_url,base_path,apiurls
conf_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/'
cf = ConfigParser.ConfigParser()
cf.read(conf_path+"imopenapi.conf")
base_url = cf.get("prefixurl", "base_url")
base_path = cf.get("prefixpath", "base_path")






def cutpicture(bid,url,wsize,hsize):
    image_bytes = urllib2.urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)
    pil_image_resized = pil_image.resize((wsize, hsize), Image.ANTIALIAS)
    xsize,ysize=pil_image_resized.size
    box=(0,0,xsize,ysize)

    cover_path=base_path+str(bid)+'/cover/cover'+str(bid)+'b.jpg'
    isExists=os.path.exists(cover_path)
    if not isExists:
        os.makedirs(base_path+str(bid)+'/cover/')
    pil_image_resized.crop(box).save(cover_path)

def addbooks(app,imreaddb,isNewSids,mcpid,sourceid=2):
    for sbid in isNewSids:
        ###清空临时章节表数据
        truncatesql='TRUNCATE TABLE public_db.con_own_tmpchapter'
        imreaddb.truncatedb(truncatesql)
        ###清空public_db.con_own_tmpbook，并将接口获得的新图书内容插入public_db.con_own_tmpbook表格
        truncatesql='TRUNCATE TABLE public_db.con_own_tmpbook'
        imreaddb.truncatedb(truncatesql)
        try:
            print '正在解析图书sbid:%s的图书信息'%sbid
            binfos=app.BookInfos(sbid,mcpid)
            # print bookinfos
            #字典的keys:['mcpid','bookid','bookname','authorname','brief','classid','classname','bookstatus','keywords','coverpath','price','pricetype','serialize_status','chaptercount','freechaptercount','wordcount','score','lastupdatetime']
            insertdata=[(binfos['mcpid'],binfos['bookid'],binfos['bookname'],binfos['authorname'],binfos['brief'],binfos['classid'],binfos['classname'],binfos['bookstatus'],binfos['keywords'],binfos['coverpath'],binfos['price'],binfos['pricetype'],binfos['serialize_status'],binfos['chaptercount'],binfos['freechaptercount'],binfos['wordcount'],binfos['score'],binfos['lastupdatetime'])]
            insertsql='insert into public_db.con_own_tmpbook (mcp_id,source_bid,book_name,author_name,book_brief,mcp_class_id,mcp_class_name,book_status,key_word,image_url,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,score,last_update_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,insertdata)
            ###将con_own_tmpbook更新到con_book中
            insertsql="""INSERT ebook_con.con_book (mcp_id,source_bid,book_name,author_name,book_brief,mcp_class_id,book_tag,big_thumb,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,book_score,modify_time,source_id,book_status)
                                            SELECT mcp_id,source_bid,book_name,author_name,book_brief,mcp_class_id,key_word,image_url,book_price,price_type,serialize_status,chapter_count,free_chapter_count,word_count,score,last_update_time,%s,0 FROM public_db.con_own_tmpbook
                        """%sourceid
            imreaddb.insertdb(insertsql)

            ###获得图书的bid
            selectsql='select source_bid,book_id,big_thumb from ebook_con.con_book where mcp_id=%s and source_bid=%s'%(mcpid,sbid)
            keydata=imreaddb.selectdb(selectsql)[0]


            sbid=keydata[0]
            bid=keydata[1]
            imageurl=keydata[2]
            print '正在处理新增图书sbid:%s,bid:%s！'%(sbid,bid)

            ###下载图片，并更新con_book中的big_thum字段
            cutpicture(bid,imageurl,200,250)
            bigthum=base_url+str(bid)+'/cover/cover'+str(bid)+'b.jpg'
            updatesql='UPDATE ebook_con.con_book set big_thumb=\'%s\' WHERE book_id=%s'%(bigthum,bid)
            imreaddb.updatedb(updatesql)

            ###获取该本图书章节信息列表
            chaptersinfos=app.BookChaptersinfos(sbid,bid)
            cinfosname=chapterinfos[0].keys()
            insertdata=[chapterinfos.values() for chapterinfos in chaptersinfos]
            ###将章节数据插入临时章节表
            adjustsql=str(tuple(cinfosname)).replace("'",'')
            insertsql='insert into con_own_tmpchapter '+adjustsql+' VALUES (%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,insertdata)
            ###创建服务器章节存放数据
            chapterpath=base_path+'%s/charpters/'%(bid)
            isExists=os.path.exists(chapterpath)
            if not isExists:
                os.makedirs(chapterpath)
            # print chaptersinfos
            ###获取章节内容并存放在服务器指定路径下
            # 用线程池进行快速订购bookLoadsUrls
            pool = ThreadPool(3)
            results = pool.map(app.BookChapterCont,chaptersinfos)
            print results
            pool.close()
            pool.join()
            ###将更新的图书上线
            updatesql='UPDATE ebook_con.con_book set book_status=2 WHERE book_id=%s'%bid
            imreaddb.updatedb(updatesql)
            print '成功新增图书sbid:%s,bid:%s！'%(sbid,bid)

            ###将临时章节表的数据插入正式库章节表
            insertsql="""INSERT ebook_con.con_chapter (book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,source_id)
                                                    SELECT book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,%s FROM public_db.con_own_tmpchapter
                            """%sourceid
            imreaddb.updatedb(insertsql)


        except Exception, e:
            print e


def renewbooks(app,imreaddb,isOldSids,mcpid):
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
        chaptersinfos=app.BookChaptersinfos(sbid,bid)

        selectsql='select chapter_id from ebook_con.con_chapter where book_id=%s'%bid
        results=imreaddb.selectdb(selectsql)
        isOldCids=[]
        for result in results:
            isOldCids.append(str(result[0]))


        isNewchaptersinfos=[]
        for chapterinfos in chaptersinfos:
            # print str(chapterinfos[2])
            if str(chapterinfos['chapter_id']) not in isOldCids:
                isNewchaptersinfos.append(chapterinfos)

        if isNewchaptersinfos !=[]:
            # print isNewchaptersinfos
            ###将章节数据插入临时章节表
            cinfosname=isNewchaptersinfos[0].keys()
            insertdata=[isNewchapterinfos.values() for isNewchapterinfos in isNewchaptersinfos]
            adjustsql=str(tuple(cinfosname)).replace("'",'')
            insertsql='insert into con_own_tmpchapter '+adjustsql+' VALUES (%s,%s,%s,%s,%s,%s)'
            imreaddb.insertdb(insertsql,insertdata)



            ###创建服务器章节存放数据
            chapterpath=base_path+'%s/charpters/'%(bid)
            isExists=os.path.exists(chapterpath)
            if not isExists:
                os.makedirs(chapterpath)
            ###获取章节内容并存放在服务器指定路径下
            # 用线程池进行快速订购bookLoadsUrls
            pool = ThreadPool(3)
            results = pool.map(app.BookChapterCont,isNewchaptersinfos)
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





