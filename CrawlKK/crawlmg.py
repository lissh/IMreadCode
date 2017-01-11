# -*- coding:utf-8 -*-      
import urllib2,re,urllib,requests,json
from requests import Request, Session
import bs4,MySQLdb,cookielib,random,os
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
# base_path='/opt/www/api/attachment/imread/bookcontent/4'
global headers

headers={
    'Host':"wap.cmread.com",
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
    'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Connection':"keep-alive"
    }




def resolveChapterInfos(sbid):
    """
    该函数用于抓取咪咕图书bid的章节信息,各个参数的含义大致如下:
    base_path:服务器存放图书的根路径；
    """
    try:
        print sbid
        chapterInfos=[]
        chapterInfo_url='http://wap.cmread.com/r/p/catalogdata.jsp?bid=%s&orderType=asc&page=1&pageSize=100000&vt=9'%str(sbid)
        # print chapterInfo_url
        req = urllib2.Request(chapterInfo_url)
        cont = urllib2.urlopen(req).read()
        # print cont
        jsoncont=json.loads(cont)
        chapterList=jsoncont['chapterList']
        chapter_rank=0
        for para in chapterList:
            chapter_rank+=1
            tomeName=para['tomeName']
            chapterName=para['chapterName']
            feeType=para['feeType']
            cid=para['cid']
            name='13858113601'
            passwd='fjfjie'
            # crawlMGBooks(bid,cid,name,passwd)
            chapterInfos+=[(sbid,cid,chapterName,feeType,chapter_rank)]



        insql='insert into public_db.con_own_tmpchapter (source_bid,chapter_id,chapter_name,price_type,chapter_rank) values (%s,%s,%s,%s,%s)'
        n=cursor.executemany(insql,chapterInfos)
        conn.commit()
        # print  chapterInfos
    except Exception , e:
        print e



def crawlMGBooks(bid,cid,name,passwd):
    """
    该函数用于订购咪咕图书bid的章节cid,各个参数的含义大致如下:
    bid:咪咕的图书ID,对应我们数据表里面的source_bid;
    cid:咪咕的图书bid的章节ID,对应我们数据表里面的chapter_id;
    name:登录咪咕的用户名;
    passwd:登录咪咕的密码;
    """
    host = "http://wap.cmread.com"
    logindata = dict(
                    uname=name,
                    passwd=passwd,
                    rememberUname="on",
                    redirect_uri='http://wap.cmread.com/r/'+str(bid)+'/'+str(cid)+'.htm?'
                    )   

    login_url='https://wap.cmread.com/sso/oauth2/login?e_l=9&client_id=cmread-wap&response_type=token'
    req = urllib2.Request(login_url,urllib.urlencode(logindata),headers=headers)
    chapterPageCont = urllib2.urlopen(req).read()
    # print cont
    # 判断是否已经订购,并对未订购的章节进行订购操作
    if '阅读页' not in chapterPageCont:
        form_action=re.findall('action="(/r/u/purchase\.jsp.*?)"',chapterPageCont)

        form_action_url=host+form_action[0]
        form_action_url = form_action_url.replace("&amp;","&")
        data ={'order_type':"1",'pt':"1"}
        req = urllib2.Request(form_action_url,urllib.urlencode(data),headers=headers)
        chapterPageCont = urllib2.urlopen(req).read()
        # req = urllib2.Request(login_url,urllib.urlencode(logindata),headers=headers)
        # chapterPageCont = urllib2.urlopen(req).read()
        print chapterPageCont
        print '图书bid:%s,已成功订购章节cid:%s!!!'%(bid,cid)
    else:
        print '图书bid:%s,章节cid:%s已订购或为免费章节!!!'%(bid,cid)

    soup= bs4.BeautifulSoup(chapterPageCont,'lxml')
    # print soup.prettify()
    chapterCont=soup.findAll('div','content')[0].div
    # print [str(chapterCont)]
    chapterCont=re.sub('<cmread num="\d+" type="page-split"></cmread>\n','',str(chapterCont))
    chapterCont=re.sub('[^(。？！”\.)]</p>\n<p cmread="page-split" style="text-indent:0em;">','',chapterCont.decode('utf8'))

    para=''
    chaptertexts=re.findall('>(.*?)</p>',chapterCont.decode('utf8'))
    for chaptertext in chaptertexts:
	    para+=str(chaptertext.replace('<p>',''))+'\n'
    print para


    f=open(base_path+'/'+str(cid)+'','a+')
    f.write(para)
    f.close()
    # # return True


       

if __name__ == '__main__':
    """
    该函数用于从数据表中获得需抓取图书内容的图书ID的列表bids,各个参数的含义大致如下:
    host:数据库地址
    user:登录数据库的用户名
    passwd:登录数据库的密码
    db:登录数据库仓库名
    """    
    # global cursor,conn
    # host="100.98.73.21"
    # user="ebook"
    # passwd="4titbrVcvnP6LSFA"
    # db='public_db'
    # conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
    # cursor = conn.cursor()

    # sql='select source_bid from public_db.con_own_book'
    # n=cursor.execute(sql)
    # sbids=[int(row[0]) for row in cursor.fetchall()]
    # # crawlMain(1)
    # for sbid in sbids:
    #     resolveChapterInfos(sbid)

    crawlMGBooks('600539117','600539165','13858113601','fjfjie')


