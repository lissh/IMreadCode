# -*- coding: utf-8 -*-
import Queue
from xml.dom.minidom import parse
import xml.dom.minidom
import threading
import time
import urllib2,cookielib,socket
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import requests,MySQLdb
import io,math
from PIL import Image
from urllib2 import urlopen
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path='/opt/www/api/attachment/imread/bookcontent/3'
isExists=os.path.exists(base_path)
if not isExists:
    os.makedirs(base_path)

#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db) 
    cursor = conn.cursor() 
    return conn



def getproxys():
    proxy_list=[]
    for page in range(1,3):
        #print page
        url = 'http://www.kuaidaili.com/proxylist/'+str(page)
        content = urllib2.urlopen(url).read()
        bids=re.findall('<tr>[^<]+<td>(.*?)</td>[^<]+<td>(\d+)</td>[^<]+<td>.*?</td>[^<]+<td>HTTP, HTTPS</td>[^<]+<td>.*?</td>[^<]+<td>(.*?)</td>', content)
        #print  bids[2] 
        for bid in bids:
            # if '移动' in bid[2] and len(bid[2])==17:
            #     #print len(bid[2]) 
                users = dict(http = str(bid[0])+":"+str(bid[1]))
                proxy_list.append(users)
    return proxy_list

def getagent():
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

    return random.choice(user_agents)

class WorkManager(object):
    def __init__(self, work_num=1000,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))
    def __init_work_queue(self, jobs_num):
        #print jobs_num
        for i in range(jobs_num):
            #print i
            cid=cinfos[i][0]
            self.add_job(gaincharcont,bid,cid,i)

    def add_job(self, func, *args):
        #print args
        self.work_queue.put((func,list(args)))

    def check_queue(self):
        return self.work_queue.qsize()

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()
        self.join()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                print args[1]

                self.work_queue.task_done()
                do(args[0],args[1])
            except Exception,e:
                print str(e)
                break

def cutpicture(bid,url,wsize,hsize):
    #url = 'http://www.qmcmw.com/files/article/image/0/689/689s.jpg'
    image_bytes = urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)
    pil_image_resized = pil_image.resize((wsize, hsize), Image.ANTIALIAS)
    xsize,ysize=pil_image_resized.size
    box=(0,0,xsize,ysize)

    path=coverpath+'/cover'+str(bid)+'b.jpg'
    pil_image_resized.crop(box).save(path)


def gaininfos(bid):
    try:
        f=open(base_path+'/infos.txt','a+')
        url = 'http://www.qmcmw.com/api/shuqi_info.php?id='+str(bid)
        content = urllib2.urlopen(url).read()

        #print content
        DOMTree = xml.dom.minidom.parseString(content)
        bookinfo = DOMTree.documentElement

        keys=['bookid','bookname','authorname','intro','genre','bookstatus','keywords','coverpath']
        keyconts=[]
        infos=''
        for key in keys:
            if bookinfo.getElementsByTagName(key)[0].childNodes!=[]:
                keycont=bookinfo.getElementsByTagName(key)[0].childNodes[0].data
                #缩放图片
                if key=='coverpath' and keycont!='':
                    cutpicture(bid,keycont,200,250)
                    keycont='http://static.imread.com/api/attachment/imread/bookcontent/3/'+str(bid)+'/cover/cover'+str(bid)+'b.jpg'
                keyconts.append(keycont)
                infos+=keycont+'|'


            else:
                keycont=''


        f.write(infos+'\n')

        return keyconts
    except Exception,e :
        print e
        return None






def gainclist(bid):
    try:
        #global cinfos
        #print '?1'       
        url = 'http://www.qmcmw.com/api/shuqi_chapter.php?id='+str(bid)
        #print url
        content = urllib2.urlopen(url,timeout=3).read()
        DOMTree = xml.dom.minidom.parseString(content)
        chapterinfo = DOMTree.documentElement
        volumes = chapterinfo.getElementsByTagName("volume")

        #print url
        #print len(volumes),volumes
        cinfos=[]
        #print '?2'
        for volume in volumes:
            #print "*****volume*****"

            vid=volume.getElementsByTagName('volumeid')[0].childNodes[0].data
            vname=volume.getElementsByTagName('volname')[0].childNodes[0].data

            chapters = volume.getElementsByTagName("chapters")[0].getElementsByTagName("chapter")
            #print len(chapters)
            #i=0
            #print '?3'
            for chapter in chapters:
                    #wordscount=wordscounts[i]
                cid=chapter.getElementsByTagName('chapterid')[0].childNodes[0].data
                cname=chapter.getElementsByTagName('chaptername')[0].childNodes[0].data
                cinfos.append((cid,cname,vid,vname,bid))
                    #print bid,vid,vname,cid,cname
                    #i+=1
            return cinfos
    except Exception,e :
        print e
        cinfos=[]
        return cinfos
        raise e



def gaincharcont(bid,cid):
    try:
        userAgent = getagent()
        proxyIp = random.choice(proxys)
        #print proxyIp

        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        proxy_support = urllib2.ProxyHandler(proxyIp)
        #opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        opener = urllib2.build_opener(proxy_support,cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        headers = {
                'User-Agent':userAgent
               }

        f=open(chapterpath+'/'+str(cid)+'.txt','w')
        url = 'http://www.qmcmw.com/api/shuqi_contentinfo.php?id='+str(bid)+'&cid='+str(cid)
        # t=random.randint(1,1000)
        # time.sleep(t/10000)
        content = urllib2.urlopen(urllib2.Request(url=url,headers = headers),timeout=5).read().replace('<![CDATA[','').replace(']]>','')
        #print content
        DOMTree = xml.dom.minidom.parseString(str(content))
        contentinfo = DOMTree.documentElement
        contents=contentinfo.getElementsByTagName('content')
        cont=''
        for content in contents:
            cont+=content.childNodes[0].data+'\n'
        #cont=re.findall('<content>([^<]+)</content>',content)

        # print cont
        if cont!='':
            wordscount=len((cont.replace('\n','')).encode("gbk").decode("gbk"))
        else:
            wordscount=0
        wordscounts.append(wordscount)

        #print cont
        f.write(cont)
        f.close()

        return wordscount

    except Exception, e:
        f=open(chapterpath+'/'+str(cid)+'.txt','w')

        time.sleep(2)
        headers = {
                'User-Agent':userAgent
               }
        url = 'http://www.qmcmw.com/api/shuqi_contentinfo.php?id='+str(bid)+'&cid='+str(cid)

        content = urllib2.urlopen(urllib2.Request(url=url,headers = headers),timeout=5).read().replace('<![CDATA[','').replace(']]>','')
        #print content
        DOMTree = xml.dom.minidom.parseString(str(content))
        contentinfo = DOMTree.documentElement
        contents=contentinfo.getElementsByTagName('content')
        cont=''
        for content in contents:
            cont+=content.childNodes[0].data+'\n'

        if cont!='':
            wordscount=len((cont.replace('\n','')).encode("gbk").decode("gbk"))
        else:
            wordscount=0
        wordscounts.append(wordscount)
        f.write(cont)
        f.close()
        return wordscount
        raise e
 


def UpdateOfficeTable():

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



        csql="""
                INSERT INTO ebook_con.con_chapter (
                    book_id,
                    chapter_id,
                    chapter_name,
                    price_type,
                    source_id,
                    source_bid,
                    create_time,
                    modify_time,
                    word_size
                ) SELECT DISTINCT
                    c.book_id,
                    a.c_id,
                    a.c_name,
                    a.c_price_type,
                    3,
                    a.source_book_id,
                    now(),
                    now(),
                    a.c_wordsize
                FROM
                    (
                        SELECT
                            *
                        FROM
                            ebook_con.con_book
                        WHERE
                            source_id = 3
                    ) c
                JOIN public_db.tmp_con_book_chapter_qm a
                LEFT JOIN (
                    SELECT
                        *
                    FROM
                        ebook_con.con_chapter
                    WHERE
                        source_id = 3
                ) b ON (
                    a.source_book_id = b.source_bid
                    AND c_id = b.chapter_id
                )
                WHERE
                    b.source_bid IS NULL
                AND c.source_bid = a.source_book_id"""

        n = cursor.execute(csql)
        conn.commit() 


        ##更新章节序号
        crsql="""
                #use ebook_con;
                UPDATE ebook_con.con_chapter a
                JOIN (
                    SELECT
                        empid,
                        deptid,
                        rank
                    FROM
                        (
                            SELECT
                                heyf_tmp.empid,
                                heyf_tmp.deptid,
                                @rownum :=@rownum + 1,

                            IF (
                                @pdept = heyf_tmp.deptid ,@rank :=@rank + 1 ,@rank := 1
                            ) AS rank,
                            @pdept := heyf_tmp.deptid
                        FROM
                            (
                                SELECT
                                    chapter_id empid,
                                    book_id deptid
                                FROM
                                    ebook_con.con_chapter
                                ORDER BY
                                    book_id ASC,
                                    chapter_id ASC
                            ) heyf_tmp,
                            (
                                SELECT
                                    @rownum := 0,
                                    @pdept := NULL ,@rank := 0
                            ) a
                        ) result
                ) b ON (a.book_id=b.deptid and a.chapter_id=b.empid) 
                set a.chapter_rank =rank"""
        n = cursor.execute(crsql)
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




def UpdateTmpTable(dealbids,flog):
    try:
        global bid,chapterpath,coverpath,wordscounts,cinfos
        fc=open(base_path+'/clist.txt','a+')

        for bid in dealbids:
            updatecinfos=[] 
            #定义需要更新章节的字数列表集合：wordscounts
            wordscounts=[]            
            #print bid
            #bid=56
            rootpath=base_path+'/'+str(bid)
            isExists=os.path.exists(rootpath)
            if not isExists:
                os.makedirs(rootpath)

            coverpath=rootpath+'/cover'
            isExists=os.path.exists(coverpath)
            if not isExists:
                os.makedirs(coverpath)

            chapterpath=base_path+'/'+str(bid)+'/chapters'
            isExists=os.path.exists(chapterpath)
            if not isExists:
                os.makedirs(chapterpath)


            if  flog=='addition':
                #print bid
                    #增加整本图书信息
                    print '图书ID：'+bid+'还未添加到在第三方书城中！！！'
                    cinfos= gainclist(bid)

                    work_manager =  WorkManager(len(cinfos),100)
                    work_manager.wait_allcomplete()

                    i=0
                    chapter_num=len(cinfos)*0.1
                    #print chapter_num,'???1'
                    chapter_free_num=math.ceil(chapter_num)
                    if chapter_free_num<2:
                        chapter_free_num=2
                    elif chapter_free_num>30:
                        chapter_free_num=30


                    binfos=gaininfos(bid)
                    serialize_status=binfos[5]

                    #对于serialize_status：0连载，1完本；  对于price_type：1按本，2按章
                    if (chapter_num>160 and serialize_status=='1') or serialize_status=='0':
                        price_type=2
                        book_price=8
                    else:
                        price_type=1
                        #<10万字=1元，10万-20万=2元，20万-30万=3元，30万-40万=4元，40万以上=5元
                        total_word=sum(wordscounts)/10000.00
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

                    insql='insert into public_db.tmp_con_book_qm(source_book_id,book_name,author,book_brief,class_name,serialize_status,key_word,image_url,word_size,free_chapter_count,price_type,book_price) values (%s,%s,%s,%s,%s,%s,%s,%s,0,'+str(chapter_free_num)+','+str(price_type)+','+str(book_price)+')'

                    n = cursor.execute(insql,binfos)
                    conn.commit()

                    print '图书ID：',bid,'正在加载新增中！' 
                    for cinfo in cinfos:
                        if  wordscounts !=[] and len(wordscounts)==len(cinfos) :

                            if i<=chapter_free_num:
                                c_price_type=0
                                #print cinfo+tuple([wordscounts[i]])
                                fc.write(cinfo[0]+'|'+cinfo[1]+'|'+cinfo[2]+'|'+cinfo[3]+'|'+str(cinfo[4])+'|'+str(wordscounts[i])+'|0'+'\n')
                                updatecinfos.append(cinfo+tuple([c_price_type])+tuple([wordscounts[i]]))
                            else:
                                c_price_type=1                            
                                fc.write(cinfo[0]+'|'+cinfo[1]+'|'+cinfo[2]+'|'+cinfo[3]+'|'+str(cinfo[4])+'|'+str(wordscounts[i])+'|0'+'\n')
                                updatecinfos.append(cinfo+tuple([c_price_type])+tuple([wordscounts[i]])) 
                            i+=1
                    print '图书ID：',bid,'已加载新增完成！' 

                        
            elif flog=='update':
                print '图书：'+str(bid)+' '+'已存在第三方书城中，检查是否需要更新中！！！'
                #bid=287
                cinfos= gainclist(bid)

                # cnsql='select chapter_count from con_book where source_bid'+str(bid)
                # n = cursor.execute(sql)
                # #for row in cursor.fetchall():
                # old_chapter_cont= cursor.fetchall()[0][0]
                # #print old_chapter_cont,'???????1'

                chapterflogs=[]
                sql='select chapter_id  from ebook_con.con_chapter where source_bid='+str(bid)
                n = cursor.execute(sql)
                for row in cursor.fetchall():
                    chapterflogs.append(str(row[0]))

                bcids=[]   
                for cinfo in cinfos:
                    bcids.append(str(cinfo[0]))
                set1 = set(chapterflogs)
                set2 = set(bcids)
                cids = list(set2 - set1)

                #chapter_num=len(chapterflogs)+len(cids)


                i=0
                for cinfo in cinfos:
                    i+=1
                    #print cinfo
                    #cid=31015
                    cid=cinfo[0]

                    if cid in cids:
                        wordscount=gaincharcont(bid,cid)
                        print '图书ID：',bid,'正在更新的章节ID：' ,cid,'该章节字数为：',wordscount                       
                        ##增加图书更新章节内容
                        c_price_type=1
                        fc.write(cinfo[0]+'|'+cinfo[1]+'|'+cinfo[2]+'|'+cinfo[3]+'|'+str(cinfo[4])+'|'+str(wordscount)+'\n')
                        updatecinfos.append(cinfo+tuple([c_price_type])+tuple([wordscount]))
                print '图书：'+str(bid)+' '+'已更新完成！！！'

            
            insql='insert into public_db.tmp_con_book_chapter_qm(c_id,c_name,v_id,v_name,source_book_id,c_price_type,c_wordsize) values (%s,%s,%s,%s,%s,%s,%s)'

            if  len(updatecinfos)==1:
                n = cursor.execute(insql,updatecinfos[0])
                conn.commit()       
            elif len(updatecinfos)>1:
                print len(updatecinfos)
                n = cursor.executemany(insql,updatecinfos)
                conn.commit()

            UpdateOfficeTable()
        fc.close()
    except Exception,e :

        print e
        return None




def mian():
    try:
        global proxys,conn,flogs,updatebids,cinfos,updatecinfos

        start = time.time()

        host="rdsljqv187pt04s68726.mysql.rds.aliyuncs.com"
        user="crawl"
        passwd="vDwoiExZ26jYaMsyZokz"
        conn=linkSQL(host,user,passwd,'ebook_con')
        #情况临时表tmp_con_book_chapter_qm和tmp_con_book_qm
        tr_tmp_chapter_qm_sql='TRUNCATE TABLE public_db.tmp_con_book_chapter_qm'
        tr_tmp_qm_sql='TRUNCATE TABLE public_db.tmp_con_book_qm'
        n = cursor.execute(tr_tmp_chapter_qm_sql)
        n = cursor.execute(tr_tmp_qm_sql)


        #获取数据源图书ID列表：booklists
        proxys=getproxys()
        url = 'http://www.qmcmw.com/api/shuqi_list.php?page=1'
        content = urllib2.urlopen(url).read()
        DOMTree = xml.dom.minidom.parseString(content)
        booklists = DOMTree.documentElement.getElementsByTagName('bookid')
        #print len(booklists)

        #获取数据库con_book中存在的第三方书城ID列表：flogs
        flogs=[]
        sql='select source_bid FROM ebook_con.con_book WHERE source_id=3'
        n = cursor.execute(sql)
        for row in cursor.fetchall():
            flogs.append(str(row[0]))
        bids=[]
        for booklist in booklists:
            bids.append(booklist.childNodes[0].data)
        #print bids
        set3 = set(flogs)
        set4 = set(bids)
        addbids = list(set4 - set3)
        updatebids=list(set4&set3)
        print len(addbids),len (updatebids)
        UpdateTmpTable(addbids,'addition')
        UpdateTmpTable(updatebids,'update')



        end = time.time()
        print "cost all time: %s" % (end-start) 

    except Exception,e :

        print e
        return None



if __name__ == '__main__':
    mian()


