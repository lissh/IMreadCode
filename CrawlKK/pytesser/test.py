# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2,re,urllib,requests
from requests import Request, Session
import bs4,MySQLdb,cookielib,random,os,time
from PIL import Image
from PIL import ImageEnhance
from pytesser import *
import subprocess
from StringIO import StringIO
import util,errors
import Queue
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
# base_path='/opt/www/api/attachment/imread/bookcontent/4'
global headers

headers={
    'Host':"wap.cmread.com",
    'User-Agent':"Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Borwser/{randomstr}",
    'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Connection':"keep-alive"
    }
def genRandomStr(l):
    low_chars = 'abcdefghijklmnopqrstuvwxyz'
    low_number_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    # all_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    # number_chars = '0123456789'
    outStr = ''
    x = random.randint(0,len(low_chars)-1)
    outStr += low_chars[x]
    for i in xrange(1,l):
        x = random.randint(0,len(low_number_chars)-1)
        outStr += low_number_chars[x]
    return outStr

def cmBase64encode(inputStr):
    base64EncodeChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    outStr = ''
    i = 0
    l = 0
    c1 = c2 = c3 = ''
    l = len(inputStr)
    while (i<l):
        c1 = ord(inputStr[i])
        i += 1
        if(i==l):
            outStr += base64EncodeChars[c1 >> 2]
            outStr += base64EncodeChars[(c1 & 0x3) << 4]
            outStr += "=="
            break
        c2 = ord(inputStr[i])
        i += 1
        if(i==l):
            outStr += base64EncodeChars[c1 >> 2]
            outStr += base64EncodeChars[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
            outStr += base64EncodeChars[(c2 & 0xF) << 2];
            outStr += "=="
            break
        c3 = ord(inputStr[i])
        outStr += base64EncodeChars[c1 >> 2];
        outStr += base64EncodeChars[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)];
        outStr += base64EncodeChars[((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6)];
        outStr += base64EncodeChars[c3 & 0x3F];
        i += 1
    return outStr

#注册并签到
def register():
            isRegister='False'
            username=genRandomStr(10)
            #检测用户名是否存在
            url = 'http://www.cmread.com/www/NiceNameAjax?username='+username+'&e_cm=cmusername'
            headers = {'Referer': 'http://www.cmread.com/www/','User-Agent':'Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'}
            r = requests.get(url,headers=headers)
            if(r.text.find('value="1"')>0):
                print 'username is exists!'
                isRegister==False
            else:
                password = genRandomStr(6)
                cmPassWordEncode = cmBase64encode(password)
                cmpicValidate = ""
                url = 'http://www.cmread.com/www/userspace/users/vc.jsp'
                headers['Referer'] = 'http://www.cmread.com/www/register'
                r = requests.get(url,headers=headers)
                if(not r.status_code == 200): return None
                cookies = r.cookies
                im = Image.open(StringIO(r.content))
                im = im.convert('L')
                brightness = ImageEnhance.Brightness(im)
                im = brightness.enhance(1.5)
                cmpicValidate = image_to_string(im)
                cmpicValidate = cmpicValidate.strip()
                print cmpicValidate
                postdata = {"passWordEncode":"","username":username,"cmrepassWord":password,"cmpicValidate":cmpicValidate,"checkbox":"checkbox","cmPassWordEncode":cmPassWordEncode}
                url = 'http://www.cmread.com/regUserRegister'
                headers['Referer'] = 'http://www.cmread.com/www/register'
                # postdata['redirect_uri']= "http://wap.cmread.com/hbc/a/si?ln=23019_352012__0_&t1=16905&cm=00000000&purl=%2Fhbc%2Fp%2Fqiandao.jsp%3Ft1%3D16905%26cm%3D00000000&vt=3"
                r = requests.post(url,data = postdata,headers = headers,cookies = cookies,allow_redirects=False)
                location = r.headers.get('location','')
                if(location=='http://www.cmread.com/goSetSecurityQuestionPage'):
                    print username,password
                    crawlMG(username,password)
                    return  {"username":username,"password":password}

def crawlMG(name,passwd):
        """
        该函数用于抓取咪咕图书bid的章节cid内容,各个参数的含义大致如下:
        base_path:服务器存放图书的根路径;
        bid:咪咕的图书ID,对应我们数据表里面的source_bid;
        cid:咪咕的图书bid的章节ID,对应我们数据表里面的chapter_id;
        name:登录咪咕的用户名;
        passwd:登录咪咕的密码;
        """
        # bid=crawlinfos[0]
        # cid=crawlinfos[1]
        # name=crawlinfos[2]
        # passwd=crawlinfos[3]
        bid='362580989'
        cid='362580999'
    # isOrder=False
    # while isOrder==False:
        host = "http://wap.cmread.com"
        logindata = dict(
                        uname=name,
                        passwd=passwd,
                        rememberUname="on",
                        redirect_uri='http://wap.cmread.com/r/'+str(bid)+'/'+str(cid)+'.htm?'
                        )

        login_url='https://wap.cmread.com/sso/oauth2/login?e_l=9&client_id=cmread-wap&response_type=token'
        headers["User-Agent"] = headers["User-Agent"].replace("{randomstr}",genRandomStr(4)+" 1.0")
        req = urllib2.Request(login_url,urllib.urlencode(logindata),headers=headers)
        cont = urllib2.urlopen(req).read()

        # pic_rul='http://wap.cmread.com'+re.findall('<img src="(/r/vs/avi[^/]+)" alt=""',cont)[0].replace('&amp;','&')
        # print pic_rul
        # r = requests.get(pic_rul,headers=headers)
        # if(not r.status_code == 200): return None
        # cookies = r.cookies
        # im = Image.open(StringIO(r.content))
        # im = im.convert('L')
        # brightness = ImageEnhance.Brightness(im)
        # im = brightness.enhance(1.5)
        # cmpicValidate = image_to_string(im)
        # cmpicValidate = cmpicValidate.strip()
        # print cmpicValidate
        #判断是否已经订购,并对未订购的章节进行订购操作
        isSuccessful=False
        if '阅读页' not in cont and '本书已经下架' not in cont:
            # print name,passwd
            soup=bs4.BeautifulSoup(cont,'lxml')
            verifyCode=soup.findAll('input',{'name':'verifyCode'})[0].get('value')
            form_action=soup.findAll('form')[0].get('action')
            print verifyCode,form_action

            form_action_url=host+form_action[0]
            form_action_url = form_action_url.replace("&amp;","&")
            data ={'order_type':"1",'pt':"1",'verifyCode':str(verifyCode)}

            req = urllib2.Request(form_action_url,urllib.urlencode(data))
            cont = urllib2.urlopen(req).read()
            print cont
            if '阅读页' in cont:
                isOrder=True
                print name,passwd
                print '图书bid:%s,已成功订购章节cid:%s!!!'%(bid,cid)
                isSuccessful= True
            else:
                isOrder=False
                # print cont
                print isOrder
        elif '本书已经下架' in cont:
            print '图书bid:%s,已下架!!!'%bid
            isSuccessful=False
        elif '阅读页' in cont:
            print '图书bid:%s,章节cid:%s已订购或为免费章节!!!'%(bid,cid)
            isSuccessful= True
        print cont

if __name__ == '__main__':
    # crawlMG('13858113601','fjfjie')
    print ('13858113601','fjfjie')+()