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
# base_path='/opt/www/ec_con'
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]


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
    IPPort=proxyip.vailProxyIPs(url)
    isSucessed =False
    trialNum=0
    # for IPPort in proxyips:
    #     print IPPort
    try:
            trialNum+=1
            if isSucessed ==False:    
                proxy_support = urllib2.ProxyHandler(IPPort)
                opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
                urllib2.install_opener(opener)

                
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
                opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
                urllib2.install_opener(opener)
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







if __name__ == '__main__':
    crawlMDB()







