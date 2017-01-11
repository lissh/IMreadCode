# -*- coding: utf-8 -*-
import proxyip,cookielib
import urllib2,re,json,os
import urllib,random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

def gen_tel():
    number_chars_pre= '3456'
    number_chars = '0123456789'
    x = random.randint(0,len(number_chars_pre)-1)
    tel = '13%s' %  number_chars_pre[x]
    for i in xrange(0,8):
        x = random.randint(0,len(number_chars)-1)
        tel += number_chars[x]
    return tel

def gen_name():
    name_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    name = ''
    for i in xrange(0,5):
        x = random.randint(0,len(name_chars)-1)
        name += name_chars[x]
    return name_chars

def vote(tid):
    headers = {
                'Referer':'http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=index&vid=3&nav=1',
                'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
                        }
    check_url='http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=info&vid=3&tid='+str(tid)
    proxyIps=proxyip.vailProxyIPs(check_url)
    ipvotenum=0
    isSucessed=False
    for proxyIp in proxyIps:
        if isSucessed ==False :    
     
            #获取一个保存cookie的对象
            cj = cookielib.LWPCookieJar()
            #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
            cookie_support = urllib2.HTTPCookieProcessor(cj) 
            proxy_support = urllib2.ProxyHandler(proxyIp)
            opener = urllib2.build_opener(cookie_support,proxy_support,urllib2.HTTPHandler)
            # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)

            try:
                req = urllib2.Request(url=check_url,headers=headers)
                html_details = urllib2.urlopen(req,timeout=3).read()
            except Exception, e:
                html_details=''
                print e
                    
            current_ticket = re.findall('>([\d]+)</em>票',html_details)
            if current_ticket:
                current_ticket = current_ticket[0]
                print "当前票数：%s" % current_ticket
                # f=open(base_path+'/totalvote','w')
                # f.write('TID:'+str(tid)+'目前总票数为:'+str(current_ticket))
                # f.close()

                formhash = re.findall('formhash" value="([^"]+)"',html_details)
                if not formhash:
                    return isSucessed
                formhash = formhash[0]
                tomhash = re.findall('tomhash" value="([^"]+)"',html_details)
                if not tomhash:
                    return isSucessed
                tomhash = tomhash[0]

                vote_url = 'http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=save&tpxm=%s&tptel=%s&formhash=%s&tomhash=%s&vid=3&tid=%s&act=tpadd&userid=0' % (gen_name(),gen_tel(),formhash,tomhash,tid)
                # print vote_url
                try:
                    req = urllib2.Request(url=vote_url,headers=headers)
                    vote_details = urllib2.urlopen(req).read()
                    # print vote_details
                    result = json.loads(vote_details)
                except Exception, e:
                    result = dict(status=408,cj = 0)
                print result
                if result.get("status") == 200 and result.get("cj") == 0 and ipvotenum>5:
                    ipvotenum+=1
                    isSucessed =True
                    return isSucessed
                elif result.get("status") == 303:
                    isSucessed=False
                    # return isSucessed
                    print '该IP投票超过限制，今天不能再使用了！'
                elif result.get("status") == 304:
                    isSucessed =True
                    print '该选手今天票数达到限额！'
                elif result.get("status") == 408:
                    isSucessed =False
                    print '请求超时！！下次再试试'
            else:
                isSucessed=False
    print '投票结束，此次投票共计成功投取%s票！'%ipvotenum


if __name__ == '__main__':
    vote(1967)




