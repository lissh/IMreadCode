# -*- coding: utf-8 -*-
import urllib2,bs4
import urllib,random
import re,os,time
import sys,cookielib
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]




def searchKDL():
    proxyIps=[]
    for page in range(1,2):
            try:

                url = 'http://www.kuaidaili.com/proxylist/'+str(page)
                req = urllib2.Request(url=url)
                resp = urllib2.urlopen(req,timeout=3)
                content=resp.read()
                resp.close()
                # print content

                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[0]
                for para in table.findAll('tr')[1::]:
                    Ip=para.findAll('td',{"data-title":"IP"})[0].text
                    Port=para.findAll('td',{"data-title":"PORT"})[0].text
                    Type=para.findAll('td',{"data-title":"类型"})[0].text
                    respSpeed=para.findAll('td',{"data-title":"响应速度"})[0].text
                    # finalConfirmTime=para.findAll('td',{"data-title":"最后验证时间"})[0].text
                    # isGetPost=para.findAll('td',{"data-title":"get/post支持"})[0].text

                    resptime=respSpeed.decode('utf-8').replace('秒','')
                    # print resptime
                    if float(resptime)<=1:
                        proxyIp = dict(http=str(Ip)+':'+str(Port))
                        proxyIps+=[proxyIp]

            except Exception, e:
                print e
    random.shuffle(proxyIps)
    return proxyIps



def searchXCDL():
    proxyIps=[]
    try:
        headers={
        'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNhYmE3YTkwZTU3MGY5M2Y1Y2EzZGU2MmUzZDRmZTk0BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUNkaHhOcE1YU0ZBbUJmTWFZOWQ5dFpzVmR0eDRjWHhMbDBIdDAvYzYzTkE9BjsARg%3D%3D--c22f95ab162070455aec9192c3d98fd10c7ac3a6; CNZZDATA1256960793=1481263062-1468312557-%7C1471510806',
        'Host':'www.xicidaili.com',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
                }
        homeurl=['http://www.xicidaili.com/nn','http://www.xicidaili.com/nt']
        random.shuffle(homeurl)
        url = homeurl[1]
        print url

        req = urllib2.Request(url=url,headers=headers)
        content = urllib2.urlopen(req).read()
        soup=bs4.BeautifulSoup(content,'lxml')
        # print soup.prettify()
        # table=soup.findAll('tr')[0]
        for para in soup.findAll('tr')[1::]:
            ip= para.findAll('td')[1].text
            port= para.findAll('td')[2].text
            speed= para.findAll('td')[6]
            linktime= para.findAll('td')[7]

            if 'bar_inner fast' in str(speed) and  'bar_inner fast' in str(linktime):
                proxyIp = dict(http=str(ip)+':'+str(port))
                proxyIps+=[proxyIp]


        random.shuffle(proxyIps)
        return proxyIps

    except Exception, e:
        print e
        return proxyIps
        print '代理IP情页没有解析成功！'


def search66IP():
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:

            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8'
                        };

                url = 'http://www.66ip.cn/areaindex_'+str(random.randint(2,34))+'/1.html'#+str(page)
                req = urllib2.Request(url=url,headers=headers)
                resp = urllib2.urlopen(req,timeout=6)
                content=resp.read()
                resp.close()
                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[2]
                # print table

                for para in table.findAll('tr')[1::]:
                    Ip=para.findAll('td')[0].text
                    Port=para.findAll('td')[1].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]
                isSucessed=True
            except Exception, e:
                print e
                trialNum+=1
                time.sleep(3)
                isSucessed=False
                print '代理IP情页没有解析成功，正在进行第%s次尝试！'%str(trialNum)
    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps

def searchIP3366():
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:

            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8'
                        };

                url = 'http://www.ip3366.net/free/?stype=2'
                req = urllib2.Request(url=url,headers=headers)
                resp = urllib2.urlopen(req,timeout=6)
                content=resp.read()
                resp.close()
                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[0]
                # print table

                for para in table.tbody.findAll('tr'):
                    Ip=para.findAll('td')[0].text
                    Port=para.findAll('td')[1].text
                    isHttps=para.findAll('td')[3].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]
                isSucessed=True
            except Exception, e:
                print e
                time.sleep(1)
                trialNum+=1
                isSucessed=False
                print '代理IP情页没有解析成功，正在进行第%s次尝试！'%str(trialNum)
    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps

def searchIPHai():
    #http://www.iphai.com/free/ng
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:
            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8'
                        };

                url = 'http://www.iphai.com/free/ng'#+str(page)
                req = urllib2.Request(url=url,headers=headers)
                resp = urllib2.urlopen(req,timeout=6)
                content=resp.read()
                resp.close()
                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[0]
                # print table
                for para in table.findAll('tr')[1::]:
                    Ip=para.findAll('td')[0].text.replace('\r\n','').replace(' ','')
                    Port=para.findAll('td')[1].text.replace('\r\n','').replace(' ','')
                    isHttps=para.findAll('td')[3].text.replace('\r\n','').replace(' ','')
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]
                isSucessed=True
            except Exception, e:
                print e
                time.sleep(1)
                trialNum+=1
                isSucessed=False
                print '代理IP情页没有解析成功，正在进行第%s次尝试！'%str(trialNum)
    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps


def testPortIPs(PortIPs,check_url):
    headers={
        'Cookie':'PHPSESSID=9urm0n1esa6hmbvvde2t5ik2l3; dss=cc; think_language=zh-CN; Hm_lvt_8eee4cacb173e36099ceadd434aa2376=1471070799,1471490756; Hm_lpvt_8eee4cacb173e36099ceadd434aa2376=1471513503; bfd_s=20006308.30381759.1471513498353; tmc=6.20006308.64977349.1471513498357.1471513503624.1471513503692; tma=20006308.56317870.1468485740234.1471070799856.1471490756709.4; tmd=47.20006308.56317870.1468485740234.; bfd_g=90a3ae96921da3320000244a000843aa5721afa3; ishot=1; Hm_lpvt_b4af7caa752f754cfcb3a1f9f1e06fc0=1471513672; Hm_lvt_b4af7caa752f754cfcb3a1f9f1e06fc0=1471513672; Hm_lvt_9b96bf5cbf23320dcd3d189a595440e3=1471510576,1471511190,1471511200,1471513673; Hm_lpvt_9b96bf5cbf23320dcd3d189a595440e3=1471513673',
        'Host':'www.meidebi.com',
        'Referer':'http://www.meidebi.com/mao',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
    }
    vailnum=0
    passIps=[]
    for PortIP in PortIPs:
        try:
            proxy_support = urllib2.ProxyHandler(PortIP)
            opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)

            req = urllib2.Request(url=check_url,headers=headers)
            resp=urllib2.urlopen(req,timeout=3)
            # html_details = resp.read()
            # print html_details
            status=resp.getcode()

            if status==200:
                vailnum+=1
                passIps+=[PortIP]
                print '代理IP地址%s,通过测试!!!'%str(PortIP)
                return passIps
            # if vailnum==3:
            #     return passIps

        except Exception, e:
            print '代理IP地址%s,无法ping通核验的网页!!'%str(PortIP)
    return passIps




def vailProxyIPs(test_url):
    ips=[]
    passips=[]
    # while ips==[]:
    #     flog=random.randint(1,2)
    #     if flog==1:
    #         ips=searchKDL()
    #     elif flog==2:
    #         ips=searchIPHai()
    ips=searchXCDL()
    print ips
    passips=testPortIPs(ips,test_url)
    print passips




if __name__ == '__main__':
    # test_url='http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=info&vid=3&tid=1967'
    test_url="http://m.meidebi.com/"
    vailproxyips=vailProxyIPs(test_url)

    # vailproxyips=searchKDL()
    # print vailproxyips






