# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup 
import time,datetime,random
import urllib2,requests,MySQLdb,urllib
import StringIO, gzip,os,re
from urllib2 import urlopen
import proxyip
import sys
reload(sys)
sys.setdefaultencoding('utf8')
base_url='http://static.imread.com/ec_con'
base_path='/opt/www/ec_con'
# base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]


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


def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read()    
    return data2   

#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db) 
    cursor = conn.cursor() 
    return conn

def insertDB(goodsinfos):
    ###将爬去到的商品详情导入好货君正式数据库public_db.tmp_con_goods_homepage
    tr_homepage_sql='TRUNCATE TABLE public_db.tmp_con_goods_homepage'
    n = cursor.execute(tr_homepage_sql)

    guideinfos_sql="""
                    INSERT INTO public_db.tmp_con_goods_homepage (goods_id,goods_name,image_url, goods_brief,goods_price,source_gid,source_id,content_path,sale_url)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
    n = cursor.executemany(guideinfos_sql,list(set(goodsinfos)))
    conn.commit()

    ###将public_db.tmp_con_goods_homepage数据导入好货君正式数据库ec_con.con_goods和ec_con.con_category_content
    TmptoVolCG_sql="""
                INSERT INTO ec_con.con_goods (goods_id,goods_name,goods_type,image_url,goods_brief,goods_price,source_gid,source_id,goods_status,image_type,content_path,sale_url,source_url,initial_uv) 
                    SELECT  nnn.goods_id,nnn.goods_name,2,nnn.image_url,nnn.goods_brief,nnn.goods_price,nnn.source_gid,2,0,1,nnn.content_path,nnn.sale_url,concat('https://detail.tmall.com/item.htm?id=',nnn.source_gid),600+ceil(rand()*300)
                        FROM
                            public_db.tmp_con_goods_homepage nnn,
                            (
                                SELECT
                                    mm.goods_id
                                FROM
                                    (SELECT n.goods_id flognull,m.goods_id FROM public_db.tmp_con_goods_homepage m LEFT JOIN ec_con.con_goods n ON m.goods_id = n.goods_id) mm
                                WHERE
                                    mm.flognull IS NULL
                            ) mmm
                        WHERE
                            mmm.goods_id = nnn.goods_id
                """
    n = cursor.execute(TmptoVolCG_sql)
    conn.commit()

    
    categoryid=102121232
    #######获取已经存在的位置序号，从而保证新增数据跟原有数据位置的一致性
    LocationNums_sql='SELECT DISTINCT category_location from ec_con.con_category_content where category_id='+str(categoryid)+' and category_location is not null ;'
    n = cursor.execute(LocationNums_sql)
    LocationNums=[]
    for row in cursor.fetchall():
        LocationNums.append(int(row[0]))

    #####获取新增的商品列表,并生成由category_id,content_id,content_type,status,category_location组成的元祖为元素的newCCCInfos列表
    newGoodsid_sql="""
                            select
                                goods_id
                            FROM
                                ec_con.con_goods
                            WHERE
                                goods_type = 2 and goods_status=1
                                and goods_id not in (SELECT content_id from ec_con.con_category_content where category_id="""+str(categoryid)+' )'
                    
    n = cursor.execute(newGoodsid_sql)
    newCCCInfos=[]


    for row in cursor.fetchall():
        locationI=0
        #跳过已经存在的位置序号category_location
        while  locationI<100000:
            locationI+=1
            if  locationI not in LocationNums:
                newCCCInfos.append(tuple([categoryid,int(row[0]),15,1,locationI]))
                LocationNums.append(locationI)
                locationI=100000 

    # print newCCCInfos
    #将newCCCInfos列表的数据插入到con_category_content表
    VolCGtoVolCCC_sql="INSERT INTO  ec_con.con_category_content( category_id,content_id,content_type,status,category_location) value (%s,%s,%s,%s,%s) "
    n = cursor.executemany(VolCGtoVolCCC_sql,newCCCInfos)
    conn.commit()


    ###每天晚上八点将下线的数据及服务器文件清理掉
    h_value=time.strftime('%H',time.localtime(time.time()))

    if str(h_value)=='20':
        gainClearids_sql="""
                SELECT b.content_id from 
                (select * from ec_con.con_goods where goods_type=2 and goods_status=0) a,
                (SELECT * from ec_con.con_category_content where status=0 and category_id="""+str(categoryid)+""")b
                where a.goods_id =b.content_id
                """
        content_ids=[]
        n = cursor.execute(gainClearids_sql)
        for row in cursor.fetchall():
            content_ids.append(int(row[0]))

        add_sql=str(tuple(content_ids)).replace(',)',')')

        clearCCC_sql="delete from ec_con.con_category_content where status=0 and category_id="+str(categoryid)+" and content_id in "+add_sql
        n = cursor.execute(clearCCC_sql)
        conn.commit()

        today= datetime.date.today()
        NdaysAgo=today - datetime.timedelta(days=7)
        # print NdaysAgo.strftime('%Y%m%d')

        clearCG_sql='delete from ec_con.con_goods where goods_type=2 and  goods_status=0 and create_time < '+str(NdaysAgo.strftime('%Y%m%d'))
        n = cursor.execute(clearCG_sql)
        conn.commit()

def clearInvaildGids():
    select_sql='SELECT goods_id,sale_url from ec_con.con_goods where goods_type=2 and goods_status=1'
    n=cursor.execute(select_sql)
    goods_ids=[]
    for row in cursor.fetchall():
        sale_url=row[1]
        goods_id=row[0]
        # print sale_url
        if sale_url!='':
            try:
                sale_url='http://shop.m.taobao.com/shop/coupon.htm?'+re.findall('(seller.*?=\d+)',sale_url)[0]+'&'+re.findall('(activity.*?=[^&]+)',sale_url)[0]


                headers={
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
                                'Accept-Language': 'zh-CN,zh;q=0.8',
                                'Host':'shop.m.taobao.com',
                                'Upgrade-Insecure-Requests':'1'
                                                }
                opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
                urllib2.install_opener(opener)
                sale_req = urllib2.Request(sale_url,headers=headers)
                sale_html_details = urllib2.urlopen(sale_req,timeout=3).read()
            except Exception, e:
                sale_html_details='该优惠券不存在或者已经过期！'

            if '该优惠券不存在或者已经过期！' in sale_html_details:
                goods_ids.append(str(goods_id))
    # print goods_ids
    if goods_ids!=[]:
        add_sql=str(tuple(goods_ids)).replace(',)',')')
        update_sql='UPDATE ec_con.con_goods set goods_status=0 where goods_type=2 and goods_id in '+add_sql
        n=cursor.execute(update_sql)
        conn.commit()


def crawlMDB():
    global proxy_support,UserAgent
    UserAgent=getagent()
    headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': UserAgent,
            'Accept-Language': 'zh-CN,zh;q=0.8',
                                        };
    html_details=''
    url='http://www.meidebi.com/fenlei/0-mao-tmall-0'
    # proxyips=proxyip.vailProxyIPs(url)
    isSucessed =False
    trialNum=0
    # for IPPort in proxyips:
    #     print IPPort
    try:
            trialNum+=1
            if isSucessed ==False:    
                # proxy_support = urllib2.ProxyHandler(IPPort)
                # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
                # urllib2.install_opener(opener)

                
                req = urllib2.Request(url=url,headers=headers)
                html_details = urllib2.urlopen(req,timeout=3).read()
                
                if '直达链接' in html_details:
                    isSucessed=True
                    print '成功在第%s次解析免费猫详情页！'%str(trialNum)
                else:
                    isSucessed=False
 
    except Exception, e:
            isSucessed=False
            print '解析免费猫详情页失败，正在进行第%s次尝试！'%str(trialNum)

    # print html_details
######用BeautifulSoup解析      
    soup=BeautifulSoup(html_details,'html.parser')
    # print soup
    goodsinfos=[]
    for goods_infos in soup.findAll('li','item clearfix')[0:10]:
        goods_id=re.findall('m-(\d+)\.html',goods_infos.findAll('a',target="_blank")[0].get('href'))[0] #商品ID
        goods_url='http://www.meidebi.com'+goods_infos.findAll('a',target="_blank")[0].get('href')
        # print goods_url
        # goods_url='http://www.meidebi.com/m-1206444.html'
        isSucessed=False
        trialNum=0
        while isSucessed==False and trialNum<=10:
            trialNum+=1
            try:
                headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'User-Agent': UserAgent,
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            # 'Cookie':'PHPSESSID=36uidon5aqe59mfaqbt95i1j92; user_region_id=think%3A%7B%22parent_id%22%3A%224%22%2C%22region_id%22%3A%2237%22%7D; think_language=zh-CN; bfdtoken=d6bb3469f7856ac8326e49b1c6fe0217; Hm_lvt_8eee4cacb173e36099ceadd434aa2376=1464858705; Hm_lpvt_8eee4cacb173e36099ceadd434aa2376=1464860233; bfd_s=20006308.61486136.1464858792291; tmc=4.20006308.24672909.1464858792294.1464860233241.1464860233328; tma=20006308.24672909.1464858792294.1464858792294.1464858792294.1; tmd=4.20006308.24672909.1464858792294.; bfd_g=90a3ae96921da3320000244a000843aa5721afa3; amvid=3d783ca452709b6915601e7fcc87080a',
                            'Host':'www.meidebi.com',
                            'Upgrade-Insecure-Requests':'1',
                                            };
                # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
                # urllib2.install_opener(opener)
                goods_req = urllib2.Request(goods_url,headers=headers)
                goods_html_details = urllib2.urlopen(goods_req,timeout=3).read()
                isSucessed=True
                print '商品详情页在第%s次解析成功了！！'%str(trialNum)
            except Exception, e:
                isSucessed=False
                goods_html_details=''
                print '商品详情页没有解析成功，正在进行第%s次尝试！'%str(trialNum)

        soup2=BeautifulSoup(goods_html_details,'html.parser')
        goods_path =base_path+'/homepage/cover'

        # print soup2.prettify()
        ####解析商品的基本信息
        try:
            goods_tmid=re.findall('id=(\d+)',soup2.findAll('a','mdb-button mdb-button-orange mdb-button-large out-link')[0].get('href')) #商品淘宝ID
        except Exception, e:
            goods_tmid=[]
        # print goods_tmid
        if goods_tmid!=[]:
            goods_tmid=goods_tmid[0]
            goods_name= soup2.findAll('h2','d-title')[0].text #商品名称
            goods_price= str(float(soup2.findAll('span','price-finally')[0].text.replace('￥','').replace(' ',''))*100)  #商品价格
            goods_cover_url=soup2.findAll('div','pic')[0].img.get('src')  #商品封面下载链接

            goods_brief=''
            sale_url=''
            for para in  soup2.findAll('div','info-view info-desc'):
                para2=para.findAll('div','_content')[0]
                for para3 in  para2.descendants:
                    if '<p' not in str(para3) and '<span' not in str(para3) and '<a' not in str(para3) and '<img' not in str(para3):
                        goods_brief+=str(para3)
                    elif '<p' not in str(para3) and '<a' in str(para3):
                        sale_url=para3.get('href')

            goods_brief=str(goods_brief).replace('\n\n','').replace('<br/> ','').replace('  ','').replace('\n\r\n','')

            # print goods_cover_url
            image_url=base_url+'/homepage/cover/cover'+str(goods_id)+'.jpg' #商品图片链接地址
            content_path=base_url+'/homepage/html/'+str(goods_id)+'.html'  #商品HTML文件链接地址
            ####将单个的商品信息放在一个元组infos_tuple中，并添加到商品详情列表中goodsinfos
            infos_tuple=(goods_id,goods_name,image_url,goods_brief,goods_price,goods_tmid,'2',content_path,sale_url)
                            
            #####将源图片下载并保存在本地服务器制定地址上
            isSucessed=False
            trialNum=0
            while isSucessed==False and trialNum<7:
                    trialNum+=1
                    try:
                        # print goods_cover_url
                        # print goods_path+'/cover'+str(goods_id)+'.jpg'
                        cover_content= urllib2.urlopen(goods_cover_url)
                        fec = open(goods_path+'/cover'+str(goods_id)+'.jpg','wb')  
                        fec.write(cover_content.read())  
                        fec.close()
                        isSucessed=True
                        print '图片在第%s次尝试中成功下载了！'%str(trialNum)
                    except Exception, e:
                        time.sleep(2)
                        isSucessed=False
                        print '图片下载失败，正在尝试进行第%s次图片下载！'%str(trialNum)
            if isSucessed==True:
                goodsinfos.append(infos_tuple)                


    # print goodsinfos
    insertDB(goodsinfos)




if __name__ == '__main__':
    host="100.98.73.21"
    user="commerce"
    passwd="Vd9ZcDSoo8eHCAVfcUYQ"
    conn=linkSQL(host,user,passwd,'public_db')
    crawlMDB()
    clearInvaildGids()






