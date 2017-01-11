# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2,re,urllib,requests
from requests import Request, Session
import bs4,MySQLdb,cookielib,random,os,json
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
# base_path='/opt/www/api/attachment/imread/bookcontent/4'
global headers



headers={
'Host': 'client.cmread.com',
'terminalUniqueId': 'A25D1429-026C-4DFD-8E2D-8F3BA998BD77',
'x-cmread-login-type': '3',
'MagazineVersion': '3.0',
# 'Accept': '*/*',
'X-Channel-Code': 'M8030001',
'ClientHash': 'zRRsUS9d/XAxVceWnkoTVw==',
'User-Agent': 'CMRead/7495 CFNetwork/758.5.3 Darwin/15.6.0 Paros/3.2.13',
'Cookie': 'JSESSIONID=C56F284B438AF603DEA3C1812958D323; Path=/cmread/; HttpOnly',
'x-apptype': '4',
'APIVersion': '1.0.0',
'isSupportGuest': '1',
'feeType': '1',
# 'IMSI': '',
'miguVersionFlag': '1',
# 'macAddress': '',
'x-cmread-visit-ft-id': '90440193038',
# 'Accept-Language': 'zh-cn',
# 'x-model': 'iPhone6,2',
# 'random': '1285327241',
'x-cmread-msisdn': '13858113601',
'user-id': 'f72f2fcc586433309a6aff5dbe9f3ac2',
# 'x-up-bear-type': 'WLAN',
'Connection': 'keep-alive',
# 'Content-Type': 'application/xml',
'osType': '2',
# 'Encoding-Type': 'gzip',
# 'x-osVersion': 'iPhone OS 9.3.4',
# 'x-brand': 'Apple',
'Action': 'getChapterInfo2',
# 'cltk': 'GNIOebuVfcfR22uZPnZvqtgOeU71ktXrV4oTr/emEIXOPKeLUyvOw2o81XWGUSYu',
# 'Proxy-Connection': 'keep-alive',
'Client-Agent': 'CMREAD_iPhone_Appstore_WH_V6.2.0_160812/640*960/Viva_MEB',
'x-sourceid': '204001'
        }



def orderMGBooks(bid,cid):

    chaptercont_url='http://client.cmread.com/cmread/portalapi?formatType=3&contentId=%s&fetchRemaining=1&chapterId=%s&offset=0&chargeOrAd=1&isSupportRTF=1'%(bid,cid)
    req = urllib2.Request(chaptercont_url,headers=headers)
    chaptercont = urllib2.urlopen(req).read()
    # print chaptercont
    if 'pageOrder' not in chaptercont:
        # print chaptercont
        # print '?1'
        productid=re.findall('<productID>(\d+)</productID>',chaptercont)[0]
        headers['Action']='subscribeContent2'

        order_url='http://client.cmread.com/cmread/portalapi?pageOrder=0&fetchRemaining=1&contentId=%s&chapterId=%s&productId=%s&formatType=3'%(bid,cid,productid)
        req = urllib2.Request(order_url,headers=headers)
        chaptercont = urllib2.urlopen(req).read()

    soup= bs4.BeautifulSoup(chaptercont,'lxml')
    try:
        FirstParagraph =soup.findAll('content')[0]
        for ParagraphCont in FirstParagraph.findAll('p'):
            print ParagraphCont.text
    except:
        # 按本的第一部分内容和按章的不一样，故区别开来
        FirstParagraph=re.findall('<content>(.*?)</content>',chaptercont)[0]
        FirstParagraphConts=re.findall('<p>(.*?)</p>',FirstParagraph)
        for FirstParagraphCont in FirstParagraphConts:
            print FirstParagraphCont

    OtherParagraph=soup.findAll('pagelist')[0]
    for paracont in OtherParagraph.findAll('p'):
        print paracont.text





bid='372302122'
cid='372302130'
orderMGBooks(bid,cid)