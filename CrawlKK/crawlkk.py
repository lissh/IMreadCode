# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2,re,urllib,json,time,bs4
import MySQLdb,random,os,StringIO,gzip
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
sourceid=1
base_path='/opt/www/api/attachment/imread/chapcontent'

global pub
pub=dict(
         sign="b906679d1c7b9e26e652824aad354293",
         screen="1080x1920",
         appCode="ishugui",
         dzPaySupport="2",
         userId="42774302",
         apiVersion="1.4.02.12150",
         pname="com.ishugui",
         clientHash="NTIxODJlNTMzODgxM2YyYzQwNDU3NWE3YmFjMGQzMGM=\\n",
         channelCode="K102023",
         os="android2",
         imei="865790020544813",
         clientAgent="svnVer_12150",
         apn="wifi",
         imsi="460012534459440",
         channelFee="K101001",
         model="YQ601"
        )



def gainSBID():
    """
    该函数用于从数据表中获得需抓取图书内容的图书ID的列表bids.
    """
    #and b.book_status=1 and a.serialize_status=0 and a.source_id=%d
    new_sql="""SELECT  aa.*  from (select a.source_bid from public_db.con_own_book a,ebook_con.con_book b where a.source_bid=b.source_bid and b.book_status=1 and a.source_id=%d )aa
                        LEFT join
                            (select source_bid from ebook_con.con_chapter  group by source_bid)bb
                        ON aa.source_bid=bb.source_bid
                        where bb.source_bid is null"""%sourceid
    n=cursor.execute(new_sql)
    new_sbids=[int(row[0]) for row in cursor.fetchall()]

    serialize_sql='select source_bid from public_db.con_own_book where serialize_status=0'
    n=cursor.execute(serialize_sql)
    serialize_sbids=[int(row[0]) for row in cursor.fetchall()]
    # print serialize_sbids
    sbids=new_sbids+serialize_sbids

    return sbids

def resolveChapterInfos(sourceBid):

    # 拿到咪咕的章节信息
    chapterInfo_url='http://wap.cmread.com/r/p/catalogdata.jsp?bid=%s&orderType=asc&page=1&pageSize=100000&vt=9'%sourceBid
    req = urllib2.Request(chapterInfo_url)
    chaptercont = urllib2.urlopen(req).read()
    jsoncont=json.loads(chaptercont)
    chapterList=jsoncont['chapterList']

    # 获取已经更新到章节表ebook_con.con_chapter 中的章节
    isExsitCids_sql='select chapter_id from ebook_con.con_chapter WHERE source_bid=%s'%sourceBid
    n=cursor.execute(isExsitCids_sql)
    isExsitCids=[str(row[0]) for row in cursor.fetchall()]
    # 获取已经爬过的临时章节表public_db.con_own_tmpchapter 中的章节
    isCrawlCids_sql='select chapter_id from public_db.con_own_tmpchapter WHERE source_bid=%s'%sourceBid
    n=cursor.execute(isCrawlCids_sql)
    isCrawlCids=[str(row[0]) for row in cursor.fetchall()]
    # 不需要抓取的章节
    # print isCrawlCids[1:3]
    notNeedCids=isCrawlCids+isExsitCids

    # 快看的章节信息
    pri=dict(v="2",defbook="1",chapterStatus="5000",bookId=str(sourceBid),chapterEndId="",marketId="M3910010", vtv="9",payWay="2",needBlockList="1",chapterId="")
    bejson=dict(pub=pub, pri=pri)
    urldata = dict( json=bejson, call='110')
    url='http://101.251.204.195/asg/portal.do?'+str(urllib.urlencode(urldata))
    req = urllib2.Request(url)
    chapterIdListCont = urllib2.urlopen(req).read()
    # print chapterIdListCont
    chapterIdListContJson=json.loads(chapterIdListCont)

    if chapterIdListContJson['pri']!=[]:
        # 由于快看的章节顺序可能不准确，这里我们直接用咪咕的章节列表信息

        chapterAllInfos=[]
        needLoadChapterIdsinfo=[]
        chapter_rank=0
        for para in chapterList:
            chapter_rank+=1
            tomeName=para['tomeName']
            chapterName=para['chapterName']
            feeType=para['feeType']
            cid=para['cid']
            # 除去已经抓取过的和已经更新过的章节
            if str(cid) not in notNeedCids:
                needLoadChapterIdsinfo+=[(cid,chapterName,feeType,chapter_rank,sourceBid)]

        # chapterNum=len(chapterIdList)
        # needLoadChapterIds=list(set(chapterIdList)-set(isExsitChapterIds))
        chapterNum=len(needLoadChapterIdsinfo)
        countI=0
        for chapterIdinfo in needLoadChapterIdsinfo:
            countI+=1
            chapterId=chapterIdinfo[0]


            pri=dict(payDexTime="2016-03-23 20:28:46",defbook="1",chapterStatus="1",bookId=str(sourceBid),chapterIds=str(chapterId),lastModify="2016-03-12 13:46:56",
                marketId="M3910010",czip="0",vtv="9",payWay="2")
            bejson=dict(pub=pub,pri=pri)
            urldata = dict( json=bejson, call='113')
            url='http://101.251.204.195/asg/portal.do?'+str(urllib.urlencode(urldata))
            req = urllib2.Request(url)
            chapterLoadCont = urllib2.urlopen(req).read()
            chapterLoadContjson=json.loads(chapterLoadCont)
            chapterLoadUrl= chapterLoadContjson['pri']['url']
            # print chapterIdinfo+tuple([chapterLoadUrl])
            if chapterLoadUrl!='':
                chapterAllInfos+=[chapterIdinfo+tuple([chapterLoadUrl])]
            print '图书:%s正在解析章节:%s,图书共%s章节,这是第%s个章节,即图书解析完成了%s'%(sourceBid,chapterId,chapterNum,countI,countI/float(chapterNum))
        #
        # print chapterAllInfos
        #将订购成功的图书及章节信息插入到临时表public_db.con_own_tmpchapter
        if chapterAllInfos !=[]:
            insertTCCC_sql='INSERT INTO public_db.con_own_tmpchapter (chapter_id,chapter_name,price_type,chapter_rank,source_bid,chapter_loadurl) VALUES(%s,%s,%s,%s,%s,%s)'
            n=cursor.executemany(insertTCCC_sql,chapterAllInfos)
            conn.commit()

    else:
        print '该图书的章节内容及信息快看中不存在！'
        # """
        # 该函数用于订购咪咕图书sourceBid的章节cid,各个参数的含义大致如下:
        # sourceBid:咪咕的图书ID,对应我们数据表里面的source_bid;
        # cid:咪咕的图书sourceBid的章节ID,对应我们数据表里面的chapter_id;
        # name:登录咪咕的用户名;
        # passwd:登录咪咕的密码;
        # """

        # searchbid_sql='select DISTINCT book_id from ebook_con.con_book where source_bid=%s'%sourceBid
        # n=cursor.execute(searchbid_sql)
        # bid=[int(row[0]) for row in cursor.fetchall()][0]

        # MGneedChapterIdsinfo=[]
        # chapter_rank=0
        # for para in chapterList:
        #     chapter_rank+=1
        #     tomeName=para['tomeName']
        #     chapterName=para['chapterName']
        #     feeType=para['feeType']
        #     cid=para['cid']
        #     # print cid
        #     try:
        #         # needLoadChapterIds+=[(sourceBid,cid,chapterName,feeType,chapter_rank)]
        #         if cid not in notNeedCids:              
        #             name='13858113601'
        #             passwd='fjfjie'
        #             host = "http://wap.cmread.com"

        #             headers={
        #                 'Host':"wap.cmread.com",
        #                 'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
        #                 'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #                 'Connection':"keep-alive"
        #                 }
        #             logindata = dict(
        #                             uname=name,
        #                             passwd=passwd,
        #                             rememberUname="on",
        #                             redirect_uri='http://wap.cmread.com/r/'+str(sourceBid)+'/'+str(cid)+'.htm?'
        #                             )   

        #             login_url='https://wap.cmread.com/sso/oauth2/login?e_l=9&client_id=cmread-wap&response_type=token'

        #             req = urllib2.Request(login_url,urllib.urlencode(logindata),headers=headers)
        #             chapterPageCont = urllib2.urlopen(req,timeout=3).read()
        #             # print cont
        #             # 判断是否已经订购,并对未订购的章节进行订购操作
        #             if '阅读页' not in chapterPageCont:
        #                 # print chapterPageCont
        #                 form_action=re.findall('action="(/r/u/purchase\.jsp.*?)"',chapterPageCont)
        #                 form_action_url=host+form_action[0]
        #                 form_action_url = form_action_url.replace("&amp;","&")
        #                 data ={'order_type':"1",'pt':"1"}
        #                 req = urllib2.Request(form_action_url,urllib.urlencode(data),headers=headers)
        #                 chapterPageCont = urllib2.urlopen(req).read()
        #                 if '阅读页' in chapterPageCont:
        #                     print '图书sourceBid:%s,已成功订购章节cid:%s,即将下载!!!'%(sourceBid,cid)
        #                 else:
        #                     # print chapterPageCont
        #                     print '图书sourceBid:%s,章节cid:%s订购失败,即将下载!!!'%(sourceBid,cid)
        #                     chapterPageCont=''
        #             else:
        #                 print '图书sourceBid:%s,章节cid:%s已订购或为免费章节,即将下载!!!'%(sourceBid,cid)

        #             soup= bs4.BeautifulSoup(chapterPageCont,'lxml')
        #             # print soup.prettify()
        #             if chapterPageCont!='':

        #                 chapterCont=soup.findAll('div','content')[0].div
        #                 chapterCont=re.sub('<cmread num="\d+" type="page-split"></cmread>\n','',str(chapterCont))
        #                 chapterCont=re.sub('[^(。？！”\.)]</p>\n<p cmread="page-split" style="text-indent:0em;">','',str(chapterCont).decode('utf8'))

        #                 chapteralltext=''
        #                 chaptertexts=re.findall('>(.*?)</p>',str(chapterCont).decode('utf8'))
        #                 for chaptertext in chaptertexts:
        #                     chapteralltext+=str(chaptertext.replace('<p>',''))+'\n'
        #                 chapterpath=base_path+'/'+str(bid)+'/charpters/'
        #                 isExists=os.path.exists(chapterpath)
        #                 if not isExists:
        #                     os.makedirs(chapterpath)
        #                 f=open(chapterpath+str(cid)+'.txt','a+')
        #                 f.write(chapteralltext)
        #                 f.close()
        #                 MGneedChapterIdsinfo+=[(cid,chapterName,feeType,chapter_rank,sourceBid)]
        #     except Exception, e:
        #         print e
        #         time.sleep(1)

        # if MGneedChapterIdsinfo !=[]:
        #     insertTCCC_sql='INSERT INTO public_db.con_own_tmpchapter (chapter_id,chapter_name,price_type,chapter_rank,source_bid) VALUES(%s,%s,%s,%s,%s)'
        #     n=cursor.executemany(insertTCCC_sql,MGneedChapterIdsinfo)
        #     conn.commit()



    #411210585
    updateTCCC_sql="""update  public_db.con_own_tmpchapter  cc
                      JOIN (SELECT a.source_bid,a.book_id FROM ebook_con.con_book a,(SELECT source_bid FROM public_db.con_own_book) b WHERE a.source_bid = b.source_bid) bb
                      ON (cc.source_bid = bb.source_bid)
                      SET cc.book_id = bb.book_id"""
    n=cursor.execute(updateTCCC_sql)
    conn.commit()


def loadsChapterInfos(tmpChapterUrlInfos):
    bookLoadsUrl=tmpChapterUrlInfos[0]
    bid=tmpChapterUrlInfos[1]
    print '真在下载:%s'%bookLoadsUrl
    cid=re.findall('/\d-(\d+)_\d+\.zip',bookLoadsUrl)[0]
    loadspath=base_path+'/'+str(bid)+'/charpters/'+str(cid)+'.zip'
    isExists=os.path.exists(base_path+'/'+str(bid)+'/charpters/'+str(cid)+'.txt')
    if not isExists:
        try:
            urllib.urlretrieve(bookLoadsUrl,loadspath)
        except Exception,e:
            print e

def turnMGintoYW():
    turn_sql="""
                UPDATE ebook_con.con_book aa
                 JOIN(
                SELECT a.book_id from
                public_db.con_own_book a left join 
                ( select DISTINCT book_id isExistbid from ebook_con.con_chapter )b on a.book_id=b.isExistbid where b.isExistbid is not null
                )bb
                on (aa.book_id=bb.book_id)
                set aa.source_id=2
             """
    n=cursor.execute(turn_sql)
    conn.commit()

def main(sourceBID):
    tmpchapterurlinfos_sql='SELECT chapter_loadurl,book_id FROM public_db.con_own_tmpchapter WHERE chapter_loadurl<>"" and source_bid='+str(sourceBID)
    n=cursor.execute(tmpchapterurlinfos_sql)
    tmpChapterUrlInfos=[(row[0],row[1]) for row in cursor.fetchall()]
    if tmpChapterUrlInfos!=[]:
        bookid= tmpChapterUrlInfos[0][1]
        # print bookid
        # bookid=[row[1] for row in cursor.fetchall()][0]
        isExists=os.path.exists(base_path+'/'+str(bookid)+'/charpters/')
        if not isExists:
            os.makedirs(base_path+'/'+str(bookid)+'/charpters/')

        bookLoadsUrls=list(set(tmpChapterUrlInfos)-set(['']))

        try:
            # 用线程池进行快速订购bookLoadsUrls
            pool = ThreadPool(20)
            results = pool.map(loadsChapterInfos,tmpChapterUrlInfos)
            pool.close()
            pool.join()
        except Exception,e:
            print e


        if bookLoadsUrls!=[]:
            try:
                unzipcommand="unzip -o '"+base_path+'/'+str(bookid)+"/charpters/*.zip' -d "+base_path+"'/"+str(bookid)+"/charpters'"
                os.system(unzipcommand)
                rmzipcommand="rm "+base_path+'/'+str(bookid)+"/charpters/*.zip"
                os.system(rmzipcommand)
            except Exception, e:
                print '文件已经存在！'


        ###将爬到的图书章节详情从艾美阅读正式数据库临时表public_db.con_own_tmpchapter导入表ebook_con.con_chapter中
        insertCC_sql="""INSERT INTO ebook_con.con_chapter(book_id,source_bid,chapter_id,chapter_name,price_type,chapter_rank,source_id)
                                      SELECT aa.book_id,aa.source_bid,aa.chapter_id,aa.chapter_name,aa.price_type,aa.chapter_rank,%d from
                                        (SELECT DISTINCT a.* from public_db.con_own_tmpchapter a,ebook_con.con_book b WHERE a.source_bid=b.source_bid) aa
                                        left join ebook_con.con_chapter bb  on aa.source_bid=bb.source_bid where bb.book_id is null GROUP BY chapter_id """%sourceid
        # print insertCC_sql
        n=cursor.execute(insertCC_sql)
        conn.commit()
        #将爬去到的图书章节详情导入艾美阅读正式数据库表public_db.con_own_tmpchapter
        tr_TCCC_sql='DELETE FROM public_db.con_own_tmpchapter'
        n = cursor.execute(tr_TCCC_sql)
        conn.commit()




if __name__ == '__main__':
    global cursor,conn
    host="100.98.73.21"
    user="ebook"
    passwd="4titbrVcvnP6LSFA"
    db='public_db'
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
    cursor = conn.cursor()
    sourceBids=gainSBID()
    for sourceBid in sourceBids:
        try:
            # print sourceBid
            chapterIdList=resolveChapterInfos(sourceBid)
            main(sourceBid)
            print '图书:%s章节内容抓取并下载完成!'%sourceBid
        except Exception, e:
            print e
    turnMGintoYW()


