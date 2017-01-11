# -*- coding: utf-8 -*-
__author__ = 'lish'
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool
import io,os,time,random,math
import xml.dom.minidom
import urllib2
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/'
base_url='http://static.imread.com/api/attachment/imread/chaptercontent/'
# base_path='/opt/www/api/attachment/imread/chaptercontent/'

user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                    ]
userAgent=random.choice(user_agents)



#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db,port=3307)
    cursor = conn.cursor()
    return conn

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


def resolveBookInfos(bid):
        f=open(base_path+'/bookinfos.txt','a+')
        url = 'http://www.qmcmw.com/api/shuqi_info.php?id='+str(bid)
        content = urllib2.urlopen(url).read()
        # print content
        DOMTree = xml.dom.minidom.parseString(content)
        bookinfo = DOMTree.documentElement
        #图书ID，图书名，作者名，简介，分类，图书状态，关键词，封面链接
        keys=['bookid','bookname','authorname','intro','genre','bookstatus','keywords','coverpath']
        keyconts=[]
        infos=''
        for key in keys:
            if bookinfo.getElementsByTagName(key)[0].childNodes!=[]:
                keycont=bookinfo.getElementsByTagName(key)[0].childNodes[0].data
                #缩放图片
                if key=='coverpath' and keycont!='':
                    cutpicture(bid,keycont,200,250)
                    keycont=base_url+str(bid)+'/cover/cover'+str(bid)+'b.jpg'
                keyconts.append(keycont)
                infos+=keycont+'|'

        f.write(infos+'\n')
        return keyconts



def resolveChapterInfos(bid):
        url = 'http://www.qmcmw.com/api/shuqi_chapter.php?id='+str(bid)
        content = urllib2.urlopen(url,timeout=3).read()
        DOMTree = xml.dom.minidom.parseString(content)
        chapterinfo = DOMTree.documentElement
        volumes = chapterinfo.getElementsByTagName("volume")
        chapterinfos=[]
        chapterrank=0
        for volume in volumes:
            # vid=volume.getElementsByTagName('volumeid')[0].childNodes[0].data #卷ID
            # vname=volume.getElementsByTagName('volname')[0].childNodes[0].data #卷名
            chapters = volume.getElementsByTagName("chapters")[0].getElementsByTagName("chapter")
            for chapter in chapters:
                chapterrank+=1
                chapterid=chapter.getElementsByTagName('chapterid')[0].childNodes[0].data
                chaptername=chapter.getElementsByTagName('chaptername')[0].childNodes[0].data
                chapterinfos.append((str(bid),chapterid,chaptername,chapterrank))
        # print chapterinfos
        return chapterinfos




def resolveChapterCont(bcids):
    try:
        bid=bcids[0]
        cid=bcids[1]
        wordscount=0
        url = 'http://www.qmcmw.com/api/shuqi_contentinfo.php?id='+str(bid)+'&cid='+str(cid)
        headers = {'User-Agent':userAgent}

        chapterpath=base_path+str(bid)+'/chapters/'+str(cid)+'.txt'
        ischapterExists=os.path.exists(chapterpath)
        if not ischapterExists:
            # print chapterpath,'?1'
            fw=open(chapterpath,'w')
            content = urllib2.urlopen(urllib2.Request(url=url,headers = headers),timeout=5).read().replace('<![CDATA[','').replace(']]>','')
            # print content
            DOMTree = xml.dom.minidom.parseString(str(content))
            contentinfo = DOMTree.documentElement
            contents=contentinfo.getElementsByTagName('content')
            cont=''
            for content in contents:
                cont+=content.childNodes[0].data+'\n'

            if cont!='':
                wordscount=len((cont.replace('\n','')).encode("gbk").decode("gbk"))

            fw.write(cont)
            fw.close()

        else:
            print chapterpath,'?2'
            fr=open(chapterpath,'r+')
            chapterlines=fr.readlines()
            for chapterline in chapterlines:
                wordscount+=len((chapterline.replace('\n','')).encode("gbk").decode("gbk"))
            fr.close()

            if wordscount==0:
                fw=open(chapterpath,'w')
                content = urllib2.urlopen(urllib2.Request(url=url,headers = headers),timeout=5).read().replace('<![CDATA[','').replace(']]>','')
                # print content
                DOMTree = xml.dom.minidom.parseString(str(content))
                contentinfo = DOMTree.documentElement
                contents=contentinfo.getElementsByTagName('content')
                cont=''
                for content in contents:
                    cont+=content.childNodes[0].data+'\n'

                if cont!='':
                    wordscount=len((cont.replace('\n','')).encode("gbk").decode("gbk"))

                fw.write(cont)
                fw.close()
        return wordscount
    except Exception,e:
        print e


def updateConbook():

    try:
        bsql="""
                INSERT INTO ebook_con.con_book (
                    book_status,
                    source_id,
                    source_bid,
                    book_name,
                    author_name,
                    book_brief,
                    class_name,
                    serialize_status,
                    book_tag,
                    big_thumb,
                    create_time,
                    class_id,
                    price_type,
                    book_price,
                    free_chapter_count
                ) SELECT DISTINCT
                    1,
                    3,
                    t.source_book_id,
                    t.book_name,
                    t.author,
                    t.book_brief,
                    t.class_name,
                    t.serialize_status,
                    t.key_word,
                    t.image_url,
                    now(),
                    0,
                    t.price_type,
                    t.book_price,
                    t.free_chapter_count
                FROM
                    public_db.tmp_con_book_qm t left join
                    (select * from ebook_con.con_book where source_id=3) b
                   on (t.source_book_id=b.source_bid)
                   where b.source_bid is null """

        n = cursor.execute(bsql)
        conn.commit()


    ##更新图书
        bisql="""
                #use ebook_con;
                UPDATE ebook_con.con_book a
                JOIN (
                    SELECT
                        book_id,
                        count(*) cnt,
                        min(chapter_id) f_chpater_id,
                        max(chapter_id) l_chpater_id,
                        count(
                            CASE
                            WHEN price_type = 0 THEN
                                chapter_id
                            END
                        ) free_cnt,
                    case when sum(word_size) >10000 then  CONCAT(round(sum(word_size)/10000,2),'万') else sum(word_size) end word_size
                    FROM
                        ebook_con.con_chapter
                    GROUP BY
                        book_id
                ) b ON (a.book_id = b.book_id)
                SET
                  first_chpater_id = b.f_chpater_id,
                  last_chapter_id=b.l_chpater_id,
                  chapter_count = b.cnt,
                  free_chapter_count = b.free_cnt,
                  word_count= b.word_size
                WHERE
                    a.source_id IN (3);"""
        n = cursor.execute(bisql)
        conn.commit()
    except Exception, e:
        print e
        raise e



def renewYWbooks(bid):

    print '图书：'+str(bid)+' '+'已存在第三方书城中，检查是否需要更新中！！！'
    chapterpath=base_path+str(bid)+'/chapters/'
    isExists=os.path.exists(chapterpath)
    if not isExists:
        os.makedirs(chapterpath)

    needUpdateChapters=[]
    chapterinfos= resolveChapterInfos(bid)


    sql='select chapter_id  from ebook_con.con_chapter where source_bid='+str(bid)
    n = cursor.execute(sql)
    isExistchapters=[str(row[0]) for row in cursor.fetchall()]

    isUpdatecids=[]
    for chapterinfo in chapterinfos:
         bcid=str(chapterinfo[1])
         if bcid not in isExistchapters:
            isUpdatecids.append(bcid)

            wordscount=resolveChapterCont((bid,bcid))
            print '图书ID：',bid,'正在更新的章节ID：' ,bcid,'该章节字数为：',wordscount
            ##增加图书更新章节内容
            price_type=1
            needUpdateChapters.append(chapterinfo+(str(price_type),str(wordscount)))
    print '图书：'+str(bid)+' '+'已更新完成！！！'


    if needUpdateChapters !=[]:
        # print needUpdateChapters
        insertTCCC_sql='INSERT INTO public_db.con_own_tmpchapter (source_bid,chapter_id,chapter_name,chapter_rank,price_type,wordsize) VALUES(%s,%s,%s,%s,%s,%s)'
        n=cursor.executemany(insertTCCC_sql,needUpdateChapters)
        conn.commit()


def addYWbooks(bid):
    addBChapters=[]
    wordsizes=[]
    #增加整本图书信息
    print '图书ID：'+bid+'还未添加到在第三方书城中！！！'
    #(str(bid),chapterid,chaptername,chapterrank)
    chapterinfos= resolveChapterInfos(bid)

    bcids=[(chapterinfo[0],chapterinfo[1]) for chapterinfo in chapterinfos]
    chapterpath=base_path+str(bid)+'/chapters/'
    isExists=os.path.exists(chapterpath)
    if not isExists:
        os.makedirs(chapterpath)


    pool = ThreadPool(20)
    pool.map(resolveChapterCont,bcids)
    pool.close()
    pool.join()

    chapter_num=len(chapterinfos)*0.1
    #print chapter_num,'???1'
    chapter_free_num=math.ceil(chapter_num)
    if chapter_free_num<2:
        chapter_free_num=2
    elif chapter_free_num>30:
        chapter_free_num=30

    #['bookid','bookname','authorname','intro','genre','bookstatus','keywords','coverpath']
    binfos=resolveBookInfos(bid)
    serialize_status=binfos[5]

    #对于serialize_status：0连载，1完本；  对于price_type：1按本，2按章
    if (chapter_num>160 and serialize_status=='1') or serialize_status=='0':
        price_type=2
        book_price=8
    else:
        price_type=1


    i=0
    
    for cinfo in chapterinfos:
        cid=cinfo[1]
        print '图书ID：',bid,'正在加载新增中章节：',cid

        # chapterwordsize=resolveChapterCont(bid,cid)
        chapterwordsize=0
        chapterpath=base_path+str(bid)+'/chapters/'+str(cid)+'.txt'
        f=open(chapterpath,'r+')
        chapterlines=f.readlines()
        for chapterline in chapterlines:
            chapterwordsize+=len((chapterline.replace('\n','')).encode("gbk").decode("gbk"))

        wordsizes+=[chapterwordsize]
        if i<chapter_free_num:
            price_type=0
        else:
            price_type=1
        addBChapters.append(cinfo+(str(price_type),str(chapterwordsize)))
        # print cinfo+(price_type,chapterwordsize)
        i+=1
    #<10万字=1元，10万-20万=2元，20万-30万=3元，30万-40万=4元，40万以上=5元
    total_word=sum(wordsizes)/10000.00
    if total_word<10.00:
        book_price=100
    elif 10.00<=total_word<20.00:
        book_price=200
    elif 20.00<=total_word<30.00:
        book_price=300
    elif 30.00<=total_word<40.00:
        book_price=400
    else:
        book_price=500


    if addBChapters !=[]:
        # print addBChapters
        insertTCCC_sql='INSERT INTO public_db.con_own_tmpchapter (source_bid,chapter_id,chapter_name,chapter_rank,price_type,wordsize) VALUES(%s,%s,%s,%s,%s,%s)'
        n=cursor.executemany(insertTCCC_sql,addBChapters)
        conn.commit()

    #['bookid','bookname','authorname','intro','genre','bookstatus','keywords','coverpath']
    bookinfos=binfos+[str(total_word),str(chapter_free_num),str(price_type),str(book_price)]
    # print bookinfos
    insql='insert into public_db.tmp_con_book_qm(source_book_id,book_name,author,book_brief,class_name,serialize_status,key_word,image_url,word_size,free_chapter_count,price_type,book_price) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    n = cursor.execute(insql,bookinfos)
    conn.commit()

    print '图书ID：',bid,'已加载新增完成！'





def mian():
    try:
        start = time.time()
        host="123.56.138.94"
        user="ebook"
        passwd="4titbrVcvnP6LSFA"
        conn=linkSQL(host,user,passwd,'ebook_con')
        #情况临时表tmp_con_book_chapter_qm和tmp_con_book_qm
        con_own_tmpchapter_sql='TRUNCATE TABLE public_db.con_own_tmpchapter'
        tr_tmp_qm_sql='TRUNCATE TABLE public_db.tmp_con_book_qm'
        n = cursor.execute(con_own_tmpchapter_sql)
        n = cursor.execute(tr_tmp_qm_sql)

        #获取数据源图书ID列表：booklists
        url = 'http://www.qmcmw.com/api/shuqi_list.php?page=1'
        content = urllib2.urlopen(url).read()
        DOMTree = xml.dom.minidom.parseString(content)
        YWWebblists = DOMTree.documentElement.getElementsByTagName('bookid')
        #print len(booklists)

        #获取数据库con_book中存在的第三方书城原文的ID列表：YWbids
        YWbids=[]
        sql='select source_bid FROM ebook_con.con_book WHERE source_id=3'
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            YWbids.append(str(row[0]))
        # print YWbids
        addYWWebbids=[]
        updateYWWebbids=[]
        for YWWebbid in YWWebblists:
            YWWebbid= YWWebbid.childNodes[0].data
            if YWWebbid not in YWbids:
                # print '1'
                addYWWebbids.append(YWWebbid)
                addYWbooks(YWWebbid)
            else:
                updateYWWebbids.append(YWWebbid)
                renewYWbooks(YWWebbid)

        # print len(addYWWebbids),len (updateYWWebbids)
        ###将图书的book_id更新到艾美阅读正式数据库临时表public_db.con_own_tmpchapter中
        updateTCCC_sql="""update  public_db.con_own_tmpchapter  cc
                          JOIN (SELECT a.source_bid,a.book_id FROM ebook_con.con_book a,(SELECT source_bid FROM public_db.con_own_book) b WHERE a.source_bid = b.source_bid) bb
                          ON (cc.source_bid = bb.source_bid)
                          SET cc.book_id = bb.book_id"""
        n=cursor.execute(updateTCCC_sql)
        conn.commit()

        ###将爬到的图书章节详情从艾美阅读正式数据库临时表public_db.con_own_tmpchapter导入表ebook_con.con_chapter中
        insertCC_sql="""INSERT INTO ebook_con.con_chapter(book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,source_id)
                                      SELECT aa.book_id,aa.source_bid,aa.chapter_id,aa.chapter_name,aa.price_type,aa.chapter_rank,%d from
                                        (SELECT DISTINCT a.* from public_db.con_own_tmpchapter a,ebook_con.con_book b WHERE a.source_bid=b.source_bid) aa
                                        left join ebook_con.con_chapter bb on (aa.source_bid = bb.source_bid and aa.chapter_id=bb.chapter_id) where bb.chapter_id is null GROUP BY chapter_id """%sourceid
        # print insertCC_sql
        n=cursor.execute(insertCC_sql)
        conn.commit()

        updateConbook()

        end = time.time()
        print "cost all time: %s" % (end-start)

    except Exception,e :

        print e
        return None

if __name__ == '__main__':

    mian()


