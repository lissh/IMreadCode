
# -*- coding: utf-8 -*-
__author__ = 'lish'

import urllib2,cookielib
import urllib,random
import re,json,os
from proxyip import *
import sys,time
import ConfigParser
import requests,MySQLdb
import sys,bs4
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/cont'



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


#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db) 
    cursor = conn.cursor() 
    return conn



def main():
    try:
        # proxys=vailProxyIPs('http://www.qiushibaike.com/hot/page/1')
        userAgent = getagent()
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        # proxy_support = urllib2.ProxyHandler(proxys[0])
        # opener = urllib2.build_opener(proxy_support,cookie_support,urllib2.HTTPHandler)
        opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        page = 1
        i=0
        j=0
        for page in range(1):
            print page
            url = 'http://www.qiushibaike.com/hot/page/' + str(page)
            headers = { 'User-Agent' : userAgent }
            try:
                request = urllib2.Request(url,headers = headers)
                response = urllib2.urlopen(request)
                content=response.read()
                soup=bs4.BeautifulSoup(content,'lxml')

                for articleblock in soup.findAll('div','article block untagged mb15'):

                    qiushi_tagid=re.findall('qiushi_tag_(\d+)',articleblock['id'])[0]
                    authorinfos=articleblock.findAll('img')[0]
                    authorname=authorinfos['alt']
                    content=articleblock.findAll('div','content')[0].text[2:-2]
                    authorpicurl=authorinfos['src']

                    authornaid=re.findall("http://pic\.qiushibaike\.com/system/avtnew/\d+/(\d+)/.*?",authorpicurl)[0]
                    try:
                        contpictures=articleblock.findAll('div','thumb')[0].findAll('img')
                        pictureurls=[tagcont['src'] for tagcont in contpictures]
                    except Exception,e:
                        pictureurls=[]

                    print qiushi_tagid,authorname,authornaid,authorpicurl
                    print content
                    print pictureurls

                    # print articleblock.prettify()

                #url = 'http://www.qiushibaike.com/hot/page/' + str(page)
                # infos5=re.findall('<div class="article.*?\n+.*?\n.*?\n<img src="(.*?)".*?\n</a>\n.*?\n<h2>(.*?)</h2>\n</a>\n</div>\n+.*?\n+(.*?)\n+.*?\n+</div>\n+.*?\n+.*?\n<img src="(.*?)"\salt="(.*?)"',content)
                # infos3=re.findall('<div class="article.*?\n+.*?\n.*?\n<img src="(.*?)".*?\n</a>\n.*?\n<h2>(.*?)</h2>\n</a>\n</div>\n+.*?\n+(.*?)\n+.*?\n+</div>',content)
                #
                # for info in infos5:
                #     i+=1
                #
                #     picture_path=base_path+'/p'+str(i)+'/picture'
                #     isExists=os.path.exists(picture_path)
                #     if not isExists:
                #         os.makedirs(picture_path)
                #
                #     content_path=base_path+'/p'+str(i)+'/content'
                #     isExists=os.path.exists(content_path)
                #     if not isExists:
                #         os.makedirs(content_path)
                #     # print len(info)
                #     # print "??"
                #     auter_picture_url=str(info[0])
                #     auther_name=str(info[1])
                #     cont=str(info[2])
                #     cont_picture_url=str(info[3])
                #     picture_title=str(info[4])
                #
                #     fobj=open(content_path+'/cont.txt','a+')
                #     fobj.write(auther_name+'\n'+cont)
                #
                #     auter_picture_path=picture_path+'/auther.jpg'
                #     auther_picture=urllib2.urlopen(auter_picture_url)
                #     fauter = open(auter_picture_path,'wb')
                #     fauter.write(auther_picture.read())
                #     fauter.close()
                #
                #     cont_picture_path=picture_path+'/content.jpg'
                #     fcont = open(cont_picture_path,'wb')
                #     #print cont_picture_url
                #     cont_picture= urllib2.urlopen(cont_picture_url)
                #     fcont.write(cont_picture.read())
                #     fcont.close()
                #
                # for info in infos3:
                #     j+=1
                #     picture_path=base_path+'/'+str(j)+'/picture'
                #     isExists=os.path.exists(picture_path)
                #     if not isExists:
                #         os.makedirs(picture_path)
                #
                #     content_path=base_path+'/'+str(j)+'/content'
                #     isExists=os.path.exists(content_path)
                #     if not isExists:
                #         os.makedirs(content_path)
                #
                #     fobj=open(content_path+'/cont.txt','a+')
                #
                #     auter_picture_url=str(info[0])
                #     auther_name=str(info[1])
                #     cont=str(info[2])
                #
                #     auter_picture_path=picture_path+'/auther.jpg'
                #     auther_picture=urllib2.urlopen(auter_picture_url)
                #     fauter = open(auter_picture_path,'wb')
                #     fauter.write(auther_picture.read())
                #     fauter.close()
                #
                #
                #     fobj.write(auther_name+'\n'+cont)

            #print infos[0]
            except urllib2.URLError, e:
                if hasattr(e,"code"):
                    print e.code
                if hasattr(e,"reason"):
                    print e.reason



    except Exception,e :
        print e
        return None

if __name__ == '__main__':
    host="121.199.32.105"
    user="yuexia"
    passwd="yuexia1991"
    conn=linkSQL(host,user,passwd,'hifun')
    # proxys=vailProxyIPs('http://www.qiushibaike.com/hot/page/1')
    # main()