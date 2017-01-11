# -*- coding: utf-8 -*-
# !/usr/bin/python
import os
import urllib2
import urllib
import cookielib
import re 
import sys
from bs4 import BeautifulSoup
'''
编码方式的设置,在中文使用时用到中文时的处理方式
'''
default_encoding = "utf-8"
if sys.getdefaultencoding() != default_encoding:
  reload(sys)
  sys.setdefaultencoding("utf-8")
def getHtml(url,data={}):
    if(data=={}):
        req=urllib2.Request(url)
    else:
        req=urllib2.Request(url,urllib.urlencode(data))
    html=urllib2.urlopen(req).read()
    return html


try:
    cookie = cookielib.CookieJar()
    cookieProc = urllib2.HTTPCookieProcessor(cookie)
except:
    raise
else:
     opener = urllib2.build_opener(cookieProc)
     opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
     urllib2.install_opener(opener)

auth_url='https://passport.jd.com/uc/loginService'
#auth_url = 'http://www.nowamagic.net/'
home_url='http://usergrade.jd.com/user/consume'
#home_url = 'http://www.nowamagic.net/librarys/nmra/';
url = "https://passport.jd.com/uc/login"
login=getHtml(url)
#print login 
loginSoup = BeautifulSoup(login,'html.parser')
#查找登陆参数中的uuid
uuid = loginSoup.find_all("form")[0].find_all("input")[0]['value']
print uuid
clrName=loginSoup.find_all("form")[0].find_all("input")[6]['name']
clrValue=loginSoup.find_all("form")[0].find_all("input")[6]['value']
'''这俩参数不是必须。。。。
eid=loginSoup.find_all("form")[0].find_all("input")[4]['value']
fp=loginSoup.find_all("form")[0].find_all("input")[5]['value']
'''
#下载验证码图片：
checkPicUrl = 'https:'+loginSoup.find_all("div",id="o-authcode")[0].find_all("img")[0]['src2']
print checkPicUrl
req = getHtml(checkPicUrl)
checkPic = open("checkPic.jpg","w")
checkPic.write(req)
checkPic.close()
#调用mac系统的预览(图像查看器)来打开图片文件
os.system('open /Applications/Preview.app/ checkPic.jpg')
checkCode = raw_input("请输入弹出图片中的验证码：") 
#登录URL
url = "http://passport.jd.com/uc/loginService"
# 登陆用户名和密码
postData = {
    'loginname':'18758879865',
    'nloginpwd':'723love112',
    'loginpwd':'723love112',
    # 'machineNet':'',
    # 'machineCpu':'',
    # 'machineDisk':'', 
    str(clrName):str(clrValue),
    'uuid':uuid,
    'authcode': checkCode
}
passport=getHtml(url,postData)
print passport
# 初始化一个CookieJar来处理Cookie
post_data=passport[0]

cookieJar=cookielib.CookieJar()
# 实例化一个全局opener
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
# 获取cookie
req=urllib2.Request(auth_url,post_data)
result = opener.open(req)
# 访问主页 自动带着cookie信息

result = opener.open('http://i.jd.com/user/info')
# 显示结果
# print result.read()
soup=BeautifulSoup(result,'html.parser')
# print soup
#昵称
nickName = soup.find_all("input", id="nickName")[0]["value"]
print "nickName:",
print nickName
