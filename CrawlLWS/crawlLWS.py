# -*- coding: utf-8 -*-
__author__ = 'lish'
import bs4
import re,json,os,codecs,hashlib
import time,datetime
import urllib2,requests,MySQLdb
import StringIO, gzip
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# base_path='/opt/www/ec_con'
base_url='http://s.haohuojun.com/'
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
# print base_path


global headers
headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.8',
            };

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

def release_cdn(cdnfile,type):

    passwd=hashlib.md5(hashlib.sha1('KEUswIa+Tc5/L').hexdigest()).hexdigest()
    url = 'http://push.dnion.com/cdnUrlPush.do'
    data = dict(
        username ='51ss',
        password = passwd,
        url = cdnfile,
        type=str(type) #标识参数 url 为目录或 URL 取值：目录（type=0） URL （type=1）
    )
    r = requests.post(url,data=data)
    # print r.headers
    print  r.status_code


#该函数是用来解析个攻略的结构关联即相关的基本信息
def AnalyzeGuides(guide_id,isChange=False):
    try:
        # mycreated_at=''
        # if len(guide_id)==2 and isinstance(guide_id,basestring)==False:
        #     new_guide_id= tuple(guide_id)
        #     guide_id=new_guide_id[0]
        #     mycreated_at=new_guide_id[1]

        goods_ids=[]
        guide_id=str(guide_id)
        print 'guide_id:', guide_id
        guide_path=base_path+'/guides/'+str(guide_id)+'/img'
        isExists=os.path.exists(guide_path)
        if not isExists:
            os.makedirs(guide_path)
        guide_base_path=base_path+'/guides/'+str(guide_id)


        ###获取攻略详情页
        guidepage_url='http://api.liwushuo.com/v2/posts/'+str(guide_id)
        # print guidepage_url
        req = urllib2.Request(guidepage_url,headers=headers)
        guidepage_content = urllib2.urlopen(req).read()

        guidepage_bejsons=json.loads(guidepage_content)
        guidepage_data=guidepage_bejsons['data']




        guide_cover_image_url=guidepage_data['cover_image_url']
        #####获取攻略的封面图片链接并下载
        cover_image_path=guide_path+'/cover'+str(guide_id)+'.jpg'
        # isExists=os.path.exists(cover_image_path)
        # if not isExists:
            # os.makedirs(cover_image_path)
            # print cover_image_url
        cover_content= urllib2.urlopen(guide_cover_image_url)
        fec = open(cover_image_path,'wb')
        fec.write(cover_content.read())
        fec.close()


        guide_content_html =guidepage_data['content_html']
        #######获取攻略页的基本信息
        check_guide_id=guidepage_data['id']
        if str(check_guide_id)==str(guide_id):

            comments_count=guidepage_data['comments_count']
            liked=guidepage_data['liked']
            likes_count=guidepage_data['likes_count']
            created_at=guidepage_data['created_at']
            share_msg=guidepage_data['share_msg'].replace('礼物说','好货君')
            # shares_count=guidepage_data['shares_count']
            short_title=guidepage_data['short_title']
            status=guidepage_data['status']
            template=guidepage_data['template']
            title=guidepage_data['title']
            updated_at=guidepage_data['updated_at']
            guide_cover_url=base_url+'guides/'+str(guide_id)+'/img/cover'+str(guide_id)+'.jpg'

            guidescontent_path=base_path+'/guides/guidescontent'

            soup=bs4.BeautifulSoup(guide_content_html,"html.parser")
            # print soup.prettify()
            if soup.findAll('div','like-hert-widget')!=[]:
                i=0
                for para1 in soup.findAll('div','like-hert-widget'):
                    ####获取攻略对应的商品ID
                    goods_id=str(para1['data-goods-id'])
                    goods_ids+=[str(goods_id)]
                    i+=1
                    guides_content=guide_id+'|'+str(goods_id)+'|'+str(i)
                    # print guides_content
                    fec=codecs.open(guidescontent_path,'a+','utf-8')
                    fec.write(guides_content+'\n')
                    fec.close()
            elif soup.findAll('div','item-info')!=[]:
                try:
                    j=0
                    for para1 in soup.findAll('div','item-info'):
                        ####获取攻略对应的商品ID
                        goods_id=str(para1['data-id'])
                        goods_ids+=[str(goods_id)]
                        j+=1
                        guides_content=guide_id+'|'+str(goods_id)+'|'+str(j)
                        # print guides_content
                        fec=codecs.open(guidescontent_path,'a+','utf-8')
                        fec.write(guides_content+'\n')
                        fec.close()
                    # print goods_ids

                except Exception, e:
                    print '攻略的商品ID列表获取失败!!!!!!'
                    print  e


            if goods_ids!=[]:
                realcreated_at=created_at
                # print realcreated_at,created_at,mycreated_at
                infos=str(comments_count)+'|'+str(guide_id)+'|'+str(liked)+'|'+str(likes_count)+'|'+str(realcreated_at)+'|'+str(share_msg)+'|'+str(short_title)+'|'+str(status)+'|'+str(template)+'|'+str(title)+'|'+str(updated_at)+'|'+str(guide_cover_url)
                if isChange==False :
                    infos_path=base_path+'/guides/infos'
                    # print infos
                    fi=open(infos_path,'a+')
                    fi.write(infos+'\n')
                    fi.close()
                    return goods_ids
                else:
                    return goods_ids,infos.split('|')
            else:
                goods_ids=[]
                return goods_ids


    except Exception, e:
        print e
        goods_ids=[]
        return goods_ids




#为了保证攻略HTML文件的标准统一性，我们单独对攻略HTML文件进行处理，待攻略基本信息和相关商品如数据库后，再调用该函数，根据数据库的信息生产标准格式的攻略HTML文件
def creatGuidesHtml(guideids):
    host="100.98.73.21"
    user="commerce"
    passwd="Vd9ZcDSoo8eHCAVfcUYQ"
    conn=linkSQL(host,user,passwd,'ec_con')
    for guideid in guideids:
        # print guideid
        section_cont=''
        ssql="""
            SELECT aa.bannernum,  bb.*
            FROM (  SELECT  goods_id,  count(DISTINCT banner_url) bannernum
                    FROM  con_goods_banner  GROUP BY  goods_id) aa,
                 (  SELECT  b.rn,  a.goods_id,  a.goods_name, a.goods_brief,  a.goods_price
                    FROM  con_goods a,
                        ( SELECT content_id, rn FROM  public_db.tmp_con_guide_content  WHERE  guide_id = '"""+str(guideid)+"""' ORDER BY rn) b
                    WHERE a.goods_id = b.content_id) bb
            WHERE aa.goods_id = bb.goods_id ORDER BY bb.rn
        """
        n = cursor.execute(ssql)
        goods_num=0
        for row in cursor.fetchall():
            # print row
            img_num=row[0]
            # goods_num=row[1]
            goods_num+=1
            goodsid=row[2]
            goodsname=row[3]
            goodsbrief=row[4]
            goodsprice=row[5]

            banners_sql = 'select DISTINCT banner_url from ec_con.con_goods_banner where goods_id='+str(goodsid)
            n = cursor.execute(banners_sql)
            bannerurls=[row[0] for row in cursor.fetchall()]
            img_cont=''
            imglog=0
            while imglog < img_num and imglog<=5:
                img_cont+='<img src="http://m.haohuojun.com/src/img/detailImg.png" data-src="'+str(bannerurls[imglog])+'" >'
                imglog+=1

            section_cont+="""
                            <section class="m-introBK" >
                                <h2 class="title" >
                                    <span class="number" >"""+str(goods_num)+"""</span>
                                    <span >"""+str(goodsname)+"""</span>
                                </h2>
                                <p class="brief" >"""+str(goodsbrief)+"""</p>
                                <div class="j_imgsWrap imgsWrap">
                                    <a href="haohuojun:///content?type=1&amp;content_id="""+str(goodsid)+"""" class="f-clearfix">
                                    """+img_cont+"""
                                    </a>
                                    <div class="swipeNav"></div>
                                </div>
                                <div class="bar f-clearfix" >
                                    <span class="price f-fl" >￥"""+str(float(goodsprice)/100)+"""</span>
                                    <a href="haohuojun:///content?type=1&amp;content_id="""+str(goodsid)+"""" class="u-btn f-fr" >查看详情</a>
                                </div>
                            </section>
                                        """

        html_guide_content="""
                            <!DOCTYPE html>
                                <html>
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no" />
                                        <title>好货君攻略详情</title>
                                        <link rel="stylesheet" type="text/css" href="http://m.haohuojun.com/src/css/temp.css">
                                    </head>
                                    <body>
                                        <div >
                                            """+str(section_cont)+"""
                                        </div>
                                        <script src="http://m.haohuojun.com/src/js/modules/swipe.js" type="text/javascript" charset="utf-8"></script>
                                        <script src="http://m.haohuojun.com/src/js/template.js" type="text/javascript" charset="utf-8"></script>
                                    </body>
                                </html>
                                """
        # print html_guide_content
        if "section" in html_guide_content:
            path=base_path+'/guides/html/'+str(guideid)+'.html'
            # print path
            f=open(path,'w')
            f.write(html_guide_content)
            f.close()
    release_cdn(base_url+'guides/html',0)



#该函数是用来解析个商品的结构关联即相关的基本信息
def AnalyzeGoods(goods_id):
    try:
        goods=str(goods_id)
        print '正在处理goods_id:',goods_id
        goods_path =base_path+'/goods/'+str(goods_id)+'/img'
            #print html_base_path
        isExists=os.path.exists(goods_path)
        if not isExists:
            os.makedirs(goods_path)

        ##商品详情页接口
        goods_url='http://api.liwushuo.com/v2/items/'+str(goods_id)
        req = urllib2.Request(goods_url,headers=headers)
        goods_page_content = urllib2.urlopen(req,timeout=3).read()

        goodspage_bejson=json.loads(goods_page_content)
        goodspage_data=goodspage_bejson['data']

        check_goodid=goodspage_data['id']
        if str(check_goodid)==str(goods_id):
            ###商品bannar图下载
            goodsbanner_urls =goodspage_data['image_urls']
            i=1
            for goodsbanner_url in goodsbanner_urls:
                try:
                    goodsbanner_path=goods_path+'/bannar'+str(i)+'.jpg'

                    goodsbanner_cont= urllib2.urlopen(goodsbanner_url,timeout=3).read()
                    fgb = open(goodsbanner_path,'wb')
                    fgb.write(goodsbanner_cont)
                    fgb.close()
                    fgbu = open(base_path+'/goods/bannarurl','a+')
                    fgbu.write(str(goods_id)+'|'+base_url+'goods/'+str(goods_id)+'/img/bannar'+str(i)+'.jpg\n')
                    fgbu.close()
                    i+=1
                except Exception, e:
                    print e

            #####商品基本信息
            category_id=goodspage_data['category_id']
            comments_count=goodspage_data['comments_count']
            cover_image_url=base_url+'goods/'+str(goods_id)+'/img/bannar1.jpg'
            created_at=goodspage_data['created_at']
            description=goodspage_data['description'].replace('\n','<br>').replace('|','&')
            favorited=goodspage_data['favorited']
            favorites_count=goodspage_data['favorites_count']
            liked=goodspage_data['liked']
            likes_count=goodspage_data['likes_count']
            name=goodspage_data['name'].replace('\n','<br>').replace('|','&')
            price=goodspage_data['price']
            purchase_id=goodspage_data['purchase_id']
            purchase_status=goodspage_data['purchase_status']
            purchase_type=goodspage_data['purchase_type']
            purchase_url=goodspage_data['purchase_url']
            shares_count=goodspage_data['shares_count']
            updated_at=goodspage_data['updated_at']
            source_type=goodspage_data['source']['type']
            subcategory_id=goodspage_data['subcategory_id']




            ###获取商品的html内容并生成文件
            goodsdetail_oldhtml= goodspage_data['detail_html']
            soup=bs4.BeautifulSoup(goodsdetail_oldhtml,'lxml')
            goodsdetail_htmlbody=soup.body.findAll('div','detail-container')[0]
            i=0
            j=0
            for body_imgurl in goodsdetail_htmlbody.findAll('img'):
                i+=1
                good_img_url= body_imgurl['src']
                if good_img_url!='':
                    ####商品详情页的图片下载
                    good_img_path=goods_path+'/'+str(i)+'.jpg'
                    isExists=os.path.exists(good_img_path)
                    if not isExists:
                        try:
                            # print good_img_url
                            good_img= urllib2.urlopen(good_img_url,timeout=3)
                            f = open(good_img_path,'wb')
                            f.write(good_img.read())
                            f.close()
                        except Exception, e:
                            if j<len(goodsbanner_urls):
                                j+=1
                                good_img_url=goodsbanner_urls[j-1]
                                good_img= urllib2.urlopen(good_img_url,timeout=3)
                                f = open(good_img_path,'wb')
                                f.write(good_img.read())
                                f.close()
                                print '图片链接地址无效！已使用banner 图替代'
                            else:
                                print '图片链接地址无效！已没有多余图片替代！！',good_img_url

                    body_imgurl['data-src']=base_url+'goods/'+str(goods_id)+'/img/'+str(i)+'.jpg'
                    body_imgurl['src']="http://m.haohuojun.com/src/img/detailImg.png"

            goodsdetail_htmlbodyscript='<script src="http://m.haohuojun.com/src/js/template.js" type="text/javascript" charset="utf-8"></script>'
            goodsdetail_htmlbodyscript=bs4.BeautifulSoup(goodsdetail_htmlbodyscript,'lxml')
            goodsdetail_htmlbodyscript= goodsdetail_htmlbodyscript.head.script

            goodsdetail_html='<!DOCTYPE html><html><head><meta charset="utf-8"/>    <meta content="webkit" name="renderer"/>    <meta content="telephone=no" name="format-detection"/>    <meta content="IE=Edge" http-equiv="X-UA-Compatible"/>    <meta content="yes" name="apple-mobile-web-app-capable"/>    <meta content="black" name="apple-mobile-web-app-status-bar-style"/>    <meta content="width=device-width, user-scalable=no,maximum-scale=1.0,initial-scale=1" id="vp" name="viewport"/>    <title>   商品详情  </title>    <link href="http://m.haohuojun.com/src/css/temp.css" rel="stylesheet" type="text/css"/></head><body></body></html>'
            goodsdetail_html=bs4.BeautifulSoup(goodsdetail_html,'lxml')

            goodsdetail_html.body.append(goodsdetail_htmlbody)
            goodsdetail_html.body.append(goodsdetail_htmlbodyscript)
            # print goodsdetail_html.prettify()

            goodsdetail_htmlcont=str(goodsdetail_html).replace('\n','').replace('\r','').replace('|','&')
            html_path=base_path+'/goods/html/'+str(goods_id)+'.html'
            fh=open(html_path,'w')
            fh.write(goodsdetail_htmlcont)
            fh.close()

            infos=str(category_id)+'|'+str(comments_count)+'|'+str(cover_image_url)+'|'+str(created_at)+'|'+str(description)+'|'+str(favorited)+'|'+str(favorites_count)+'|'+str(goods_id)+'|'+str(liked)+'|'+str(likes_count)+'|'+str(name)+'|'+str(price)+'|'+str(purchase_id)+'|'+str(purchase_status)+'|'+str(purchase_type)+'|'+str(purchase_url)+'|'+str(shares_count)+'|'+str(source_type)+'|'+str(subcategory_id)+'|'+str(updated_at)
            # print infos
            ####将商品信息写入info文件中
            infos_path=base_path+'/goods/infos'
            fi=open(infos_path,'a+')
            fi.write(infos+'\n')
            fi.close()
            return infos.split('|')
    except Exception, e:
        print e


#该函数是用来解析个专题结构关联即相关的基本信息,对应的是数据库和服务器上的topic（专题）相关的数据
def AnalyzeTopic(topic_id,location):
    try:

        topicsinfos_path=base_path+'/topics/infos'
        topicscontent_path=base_path+'/topics/topicscontent'
        guide_ids=[]
        i=0
        for offset in range(0,10,10):
                # print offset
                topic_url='http://api.liwushuo.com/v2/collections/'+str(topic_id)+'/posts?gender=1&generation=1&limit=10&offset='+str(offset)
                # print collection_url
                topic_content=requests.get(topic_url,timeout=3).text

                topicpage_bejson=json.loads(topic_content)
                topicpage_date=topicpage_bejson['data']

                ####下载专题封面图片
                cover_image_url=topicpage_date['cover_image_url']
                cover_image_path=base_path+'/topics/img/topic_'+str(location)+'_'+str(topic_id)+'.jpg'
                isExists=os.path.exists(cover_image_path)
                if not isExists:
                    cover_content= urllib2.urlopen(cover_image_url)
                    ftc = open(cover_image_path,'wb')
                    ftc.write(cover_content.read())
                    ftc.close()

                ###专题信息
                posts_count=topicpage_date['posts_count']
                status=topicpage_date['status']
                subtitle=topicpage_date['subtitle'].replace('\n','<br>').replace('|','&')
                title=topicpage_date['title'].replace('\n','<br>').replace('|','&')
                updated_at=topicpage_date['updated_at']
                check_topicid=topicpage_date['id']
                cover_image_url=base_url+'topics/img/topic_'+str(location)+'_'+str(topic_id)+'.jpg'
                # print subtitle

                if '话题' not in  title and str(topic_id) == str(check_topicid):
                    collection_infos_content=str(topic_id)+'|'+str(title)+'|'+str(posts_count)+'|'+str(subtitle)+'|'+str(status)+'|'+str(cover_image_url)+'|'+str(updated_at)+'|'+str(location)
                    fti=codecs.open(topicsinfos_path,'a+','utf-8')
                    fti.write(collection_infos_content+'\n')
                    fti.close()


                    ####专题对应的攻略列表
                    topicpage_data_posts=topicpage_date['posts']
                    guide_ids=[]
                    for topicpage_data_post in topicpage_data_posts:


                        guide_id= topicpage_data_post['id']
                        guide_ids+=[str(guide_id)]
                        i+=1
                        topic_content=str(topic_id)+'|'+str(guide_id)+'|'+str(i)
                        ftc=codecs.open(topicscontent_path,'a+','utf-8')
                        ftc.write(topic_content+'\n')
                        ftc.close()

                        print '专题ID:'+str(topic_id)+'-攻略ID:'+str(guide_id)
        return  guide_ids
    except Exception, e:
        raise e



#这个类是用来解析礼物说分类页面（selectionpage），这里我们根据页面的特征，一共将其分为了三个区块：
#分别为block1:长方形banner部分
#block2:正方形banner部分
#block3:除block1，block2意外其它的部分，主要也是一些攻略专题等的混合长图，这个为了避免爬取过量的数据，我们给了他一个默认的周期参数即tday=30(前三十天更新或者发布过的)
class crawlSelectionGuides(object):

    def dealBlock1(self):
        print '处理精选页面中的长方形专题中的攻略...'
        topics_path=base_path+'/topics/img'
        block1_url='http://api.liwushuo.com/v2/banners?'
        block1_content = requests.get(block1_url,timeout=3).text
        block1page_bejson=json.loads(block1_content)
        block1_databanners=block1page_bejson['data']['banners']


        for block1_databanner in block1_databanners:
            topic_id=block1_databanner['target_id']

            selection_block1_guides=AnalyzeTopic(str(topic_id),1)
            # print selection_block1_guides
            selection_block1_imgurl=block1_databanner['image_url']
            selection_block1_coverpath=topics_path+'/topic_1_'+str(topic_id)+'.jpg'
            isExistsTopic=os.path.exists(selection_block1_coverpath)
            if not isExistsTopic:
                selection_block1_covercont= urllib2.urlopen(selection_block1_imgurl)
                fb = open(selection_block1_coverpath,'wb')
                fb.write(selection_block1_covercont.read())
                fb.close()

        return selection_block1_guides

    def dealBlock2(self):
        ###正方形的专题接口不同，单独处理
        print '处理精选页面中的正方形专题中的攻略...'
        topics_path=base_path+'/topics/img'
        block2_url='http://api.liwushuo.com/v2/secondary_banners?gender=1&generation=1'
        block2_content=requests.get(block2_url,timeout=3).text
        block2page_bejson=json.loads(block2_content)
        block2page_data2rybanners=block2page_bejson['data']['secondary_banners']

        for block2page_data2rybanner in block2page_data2rybanners:
            target_url=block2page_data2rybanner['target_url']
            if 'type=topic' in str(target_url):
                topic_id=re.findall('type=topic\&topic_id=(\d+)',target_url)[0]
                selection_block2_guides=AnalyzeTopic(topic_id,2)
                selection_block2_imgurl=block2page_data2rybanner['image_url']
                selection_block2_coverpath=topics_path+'/topic_2_'+str(topic_id)+'.jpg'
                isExistsTopic=os.path.exists(selection_block2_coverpath)
                if not isExistsTopic:
                    selection_block2_covercont= urllib2.urlopen(selection_block2_imgurl)
                    fb = open(selection_block2_coverpath,'wb')
                    fb.write(selection_block2_covercont.read())
                    fb.close()
        return selection_block2_guides


    def dealBlock3(self,tdays=200):
        print '处理精选页面中的攻略中...'
        selection_block3_guides=[]
        for offset in range(0,int(tdays)*20,20):#20-1000
            block3_url='http://api.liwushuo.com/v2/channels/100/items?ad=2&gender=1&generation=1&limit=20&offset='+str(offset)
            block3_content = requests.get(block3_url,timeout=3).text
            block3page_bejson=json.loads(block3_content)
            block3page_dataitems=block3page_bejson['data']['items']
            # print block3page_data
            if block3page_dataitems!=[]:
                for block3page_dataitem in block3page_dataitems:
                    #print '???'
                    # print selection_guide_para
                    guide_id=block3page_dataitem['id']
                    created_at=block3page_dataitem['created_at']

                    DaysAgo = (datetime.datetime.now() - datetime.timedelta(days = tdays))
                    timeStamp = int(time.mktime(DaysAgo.timetuple()))
                    # print int(flogtime),timeStamp,DaysAgo

                    if int(created_at)>=timeStamp:

                        guide_path=base_path+'/guides/'+str(guide_id)+'/img'
                        isExists=os.path.exists(guide_path)
                        if not isExists:
                            os.makedirs(guide_path)

                        selection_block3_guides+=[str(guide_id)]

                        block3_coverurl=block3page_dataitem['cover_image_url']
                        block3_coverpath=guide_path+'/cover_'+str(guide_id)+'.jpg'
                        isExistsTopic=os.path.exists(block3_coverpath)
                        if not isExistsTopic:
                            block3_covercont= urllib2.urlopen(block3_coverurl)
                            fb = open(block3_coverpath,'wb')
                            fb.write(block3_covercont.read())
                            fb.close()
                    else:
                        break
            else:
                break
        print
        return selection_block3_guides

    def gainAllGuide(self):
        main=crawlSelectionGuides()
        selection_block1_guides=main.dealBlock1()
        selection_block2_guides=main.dealBlock2()
        selection_block3_guides=main.dealBlock3()
        selection_guide_ids=selection_block1_guides+selection_block2_guides+selection_block3_guides
        # print selection_guide_ids
        return selection_guide_ids

#这个函数是用来解析礼物说热门页面（popularpage），这里我总页就是一个商品的展示柜。
def crawlPopularGoodss(tdays=100):
    try:
        popular_goodsids=[]
        for offset in range(0,int(tdays)*50,50):
            pop_url='http://api.liwushuo.com/v2/items?gender=1&generation=1&limit=50&offset='+str(offset)
            pop_content=requests.get(pop_url,timeout=3).text
            poppage_bejson=json.loads(pop_content)
            poppage_dataitems=poppage_bejson['data']['items']
            # print poppage_dataitems

            if poppage_dataitems!=[]:
                for poppage_dataitem in poppage_dataitems:
                    goods_id=poppage_dataitem['data']['id']
                    popular_goodsids+=[str(goods_id)]
            else:
                break
        # print popular_goodsids
        return popular_goodsids
    except Exception, e:
        raise e


#这个类是用来解析礼物说分类页面（classpage），这里我们根据页面的特征，一共将其分为了两个区块：
#分别为block1:专题banner部分包含查看全部里面的全部类荣，这个为了避免爬取过量的数据，我们给了他一个默认的周期参赛即tday=10(前十天更新或者发布过的专题)。
#block2:除专题部分以外的其它部分（即主题－频道（items-channels），例如：品类－礼物，穿搭，美食......）
class crawlClassGuides(object):

    def dealBlock1(self,tdays=10):
        #获取分类页专题集的攻略ID
        block1_guideids=[]
        for offset in range(0,int(tdays)*10,10):
            block1_url='http://api.liwushuo.com/v2/collections?limit=10&offset='+str(offset)
            block1_content=requests.get(block1_url,timeout=3).text
            block1page_bejson=json.loads(block1_content)
            block1page_datacollections=block1page_bejson['data']['collections']
            # print block1page_datacollections
            if block1page_datacollections!=[]:
                for block1page_datacollection in block1page_datacollections:
                    topic_id=block1page_datacollection['id']
                    created_at=block1page_datacollection['created_at']

                    DaysAgo = (datetime.datetime.now() - datetime.timedelta(days = tdays))
                    timeStamp = int(time.mktime(DaysAgo.timetuple()))
                    block1_guideids+=AnalyzeTopic(topic_id,3)
                    # if int(created_at)>int(timeStamp):
                    #     block1_guideids+=AnalyzeTopic(topic_id,3)
                    # else:
                    #     break

        return block1_guideids


    def dealBlock2(self,tdays=10):

        #获取分类页分组－频道的攻略ID
        # groups_infos_path=base_path+'/items/groupsinfos' #风格|品类|对象|场合
        items_infos_path=base_path+'/items/itemsinfos'
        items_content_path=base_path+'/items/itemscontent'

        block2_url='http://api.liwushuo.com/v2/channel_groups/all'
        block2_content=requests.get(block2_url,timeout=3).text
        block2page_bejson=json.loads(block2_content)
        block2page_data_channelgroups=block2page_bejson['data']['channel_groups']
        # print block2page_data_channelgroups

        block2_guide_ids=[]
        for block2page_data_channelgroup in block2page_data_channelgroups:
            block2page_data_channelgroup_channels=block2page_data_channelgroup['channels']
            channel_groups_id=block2page_data_channelgroup['id']

            # channel_group_name=block2page_data_channelgroup['name']
            # channel_group_status=block2page_data_channelgroup['status']
            # print channel_group_id,channel_group_name
            # group_infos_content=channel_group_id+'|'+channel_group_name+'|'+channel_group_status
            # fgi=codecs.open(items_infos_path,'a+','utf-8')
            # fgi.write(group_infos_content+'\n')
            # fgi.close()
            # print block2page_data_channelgroup_channels

            for block2page_data_channelgroup_channel in block2page_data_channelgroup_channels:
                channel_cover_image_url=block2page_data_channelgroup_channel['cover_image_url']
                channel_icon_url=block2page_data_channelgroup_channel['icon_url']
                channel_id=block2page_data_channelgroup_channel['id']
                channel_items_count=block2page_data_channelgroup_channel['items_count']
                channel_name=block2page_data_channelgroup_channel['name']
                channel_status=block2page_data_channelgroup_channel['status']

                # channel_icon_path=base_path+'/items/img/item'+str(channel_id)+'_icon.jpg'
                # isExists=os.path.exists(channel_icon_path)
                # if not isExists:
                #     channel_icon= urllib2.urlopen(channel_icon_url)
                #     fcicon = open(channel_icon_path,'wb')
                #     fcicon.write(channel_icon.read())
                #     fcicon.close()


                channel_icon_url=base_url+'items/img/item'+str(channel_id)+'_icon.jpg'
                channel_infos_content=str(channel_groups_id)+'|'+str(channel_id)+'|'+str(channel_name)+'|'+str(channel_items_count)+'|'+str(channel_status)+'|'+str(channel_icon_url)
                fci=codecs.open(items_infos_path,'w','utf-8')
                fci.write(channel_infos_content+'\n')
                fci.close()

                location=0
                for offset in range(0,int(tdays)*10,10):
                    channel_url='http://api.liwushuo.com/v2/channels/'+str(channel_id)+'/items?limit=10&offset='+str(offset)
                    channel_content=requests.get(channel_url,timeout=3).text
                    channelpage_bejson=json.loads(channel_content)
                    channelpage_dataitems=channelpage_bejson['data']['items']


                    if  channelpage_dataitems !=[]:

                        for channelpage_dataitem in channelpage_dataitems:
                            block2_guideid=channelpage_dataitem['id']
                            block2_guide_ids+=[str(block2_guideid)]
                            location+=1
                            item_infos_content=str(channel_id)+'|'+str(block2_guideid)+'|'+str(location)
                            fti=codecs.open(items_content_path,'a+','utf-8')
                            fti.write(item_infos_content+'\n')
                            fti.close()

        return block2_guide_ids


    def dealBlock3(self):
        # http://api.liwushuo.com/v2/columns/17?limit=20&offset=0
        # http://api.liwushuo.com/v2/columns?limit=11&offset=0
        #获取分类页分组－频道的攻略ID
        # groups_infos_path=base_path+'/items/groupsinfos' #风格|品类|对象|场合
        columns_infos_path=base_path+'/columns/columnsinfos'
        columns_content_path=base_path+'/columns/columnscontent'
        # print(columns_content_path)


        columns_url='http://api.liwushuo.com/v2/columns?limit=11&offset=0'
        columns_contents=requests.get(columns_url,timeout=3).text
        bejson=json.loads(columns_contents)
        f=open(columns_infos_path,'w+')
        for column in  bejson['data']['columns']:
            title= column['title']
            cover_image_url= column['cover_image_url']
            description= column['description']
            id= column['id']
            subtitle= column['subtitle']

            f.writelines(str(title)+'|'+str(cover_image_url)+'|'+str(description)+'|'+str(id)+'|'+str(subtitle)+'\n')
        f.close()




    def gainAllGuide(self):
        block1_guides=self.dealBlock1()
        block2_guides=self.dealBlock2()
        guide_ids=list(set(block1_guides+block2_guides))
        return guide_ids







def clearInfosFile():
    try:
        print 'clearing the content of files!'

        fgiude=open(base_path+'/guides/infos','r+')
        fgiude.truncate()
        fgiude.close()

        fguidescont=open(base_path+'/guides/guidescontent','r+')
        fguidescont.truncate()
        fguidescont.close()


        fgoods=open(base_path+'/goods/infos','r+')
        fgoods.truncate()
        fgoods.close()

        fgbu = open(base_path+'/goods/bannarurl','r+')
        fgbu.truncate()
        fgbu.close()

        fti = open(base_path+'/collections/infos','r+')
        fti.truncate()
        fti.close()

        fte = open(base_path+'/collections/collectionscontent','r+')
        fte.truncate()
        fte.close()

        fti = open(base_path+'/items/itemsinfos','r+')
        fti.truncate()
        fti.close()

        fte = open(base_path+'/items/itemscontent','r+')
        fte.truncate()
        fte.close()

        fte = open(base_path+'/topics/infos','r+')
        fte.truncate()
        fte.close()

        fte = open(base_path+'/topics/topicscontent','r+')
        fte.truncate()
        fte.close()
        print 'cleared!'
    except Exception, e:
        print '初次运行，文件还未生成，无需清空'


def main():
    try:

        # clearInfosFile()

        # selectguides=crawlSelectionGuides()
        # selectguides.dealBlock3(1)
        # Selectinguides=selectguides.gainAllGuide()
        # # print Selectinguides
        classguides=crawlClassGuides()
        classguides.dealBlock2(1)
        # classguides.dealBlock2()
        # classguides.dealBlock3()
        # Classguides=classguides.gainAllGuide()
        # # print Classguides
        # crawlPopularGoodss(1)

        # AnalyzeTopic('311',3)

        # AnalyzeGoods('1002919')
        # release_cdn(base_url+'goods/html/1002918.html',1)
        # AnalyzeGuides('1044070')
        # creatGuidesHtml(['17'])
        # release_cdn(base_url+'guides/html',0)

    except Exception,e :
        print e
        raise e



if __name__ == '__main__':
    main()
