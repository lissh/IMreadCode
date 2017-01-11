# -*- coding: utf-8 -*-
import urllib2,bs4
import urllib,random
import re,os,time
import sys,cookielib
reload(sys)
sys.setdefaultencoding('utf-8')
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


def searchKDL():
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': UserAgent,
                        'Accept-Language': 'zh-CN,zh;q=0.8'
                        };

                url = 'http://www.kuaidaili.com/proxylist/'#+str(page)
                req = urllib2.Request(url=url,headers=headers)
                resp = urllib2.urlopen(req,timeout=6)
                content=resp.read()
                resp.close()
                # print content
                
                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[0]
                for para in table.findAll('tr')[1:20]:
                    Ip=para.findAll('td',{"data-title":"IP"})[0].text
                    Port=para.findAll('td',{"data-title":"PORT"})[0].text
                    Type=para.findAll('td',{"data-title":"类型"})[0].text
                    respSpeed=para.findAll('td',{"data-title":"响应速度"})[0].text
                    finalConfirmTime=para.findAll('td',{"data-title":"最后验证时间"})[0].text
                    isGetPost=para.findAll('td',{"data-title":"get/post支持"})[0].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]

            except Exception, e:
                print e

    random.shuffle(proxyIps)
    return proxyIps



def searchXCDL():
    UserAgent=getagent()
    proxyIps=[]

    try:
        headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                'Accept-Language': 'zh-CN,zh;q=0.8',
                "Host":"www.xicidaili.com",
                "Upgrade-Insecure-Requests":"1",
                "Pragma":"no-cache",
                "Cache-Control":"no-cache",
                "Connection":"keep-alive",
                "Cookie":"_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWFkYzRiMWNjOWNhOWU2NjE2MGE2YzA3YmJkMGFhM2FkBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXpmSDh6MWhpUkw0NE43dDI4VGpyNEx2b1Jwa1FZRkt3bytxOWZJc3o1MlE9BjsARg%3D%3D--1661bfd1b62b95f4f1f37af1786dc266acca614a; CNZZDATA1256960793=1481263062-1468312557-%7C1468474796"
                };
        homeurl=['http://www.xicidaili.com/nn','http://www.xicidaili.com/nt']
        random.shuffle(homeurl)
        url = homeurl[0]
        # print url

        req = urllib2.Request(url=url,headers=headers)
        content = urllib2.urlopen(req).read()
        # print content
        proxy_contents= re.findall('<td.*?/></td>\n\s+<td>(.*?)</td>\n\s+<td>(.*?)</td>',content)
        # print proxy_contents
        vailnum=0
        for proxy_content in proxy_contents[0:20]:
            proxyIp = dict(http=str(proxy_content[0])+':'+str(proxy_content[1]))

            proxyIps+=[proxyIp]
        random.shuffle(proxyIps)
    except Exception, e:
        print e
        print '代理IP情页没有解析成功！'

    random.shuffle(proxyIps)
    return proxyIps


def search66IP():
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': UserAgent,
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

                for para in table.findAll('tr')[1:20]:
                    Ip=para.findAll('td')[0].text
                    Port=para.findAll('td')[1].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]

            except Exception, e:
                print e

    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps

def searchIP3366():
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': UserAgent,
                        'Accept-Language': 'zh-CN,zh;q=0.8'
                        };

                url = 'http://www.ip3366.net/free/?stype=2'#+str(page)
                req = urllib2.Request(url=url,headers=headers)
                resp = urllib2.urlopen(req,timeout=6)
                content=resp.read()
                resp.close()
                soup=bs4.BeautifulSoup(content,'lxml')
                table=soup.findAll('table')[0]
                # print table
                for para in table.tbody.findAll('tr')[0:20]:
                    Ip=para.findAll('td')[0].text
                    Port=para.findAll('td')[1].text
                    isHttps=para.findAll('td')[3].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]
            except Exception, e:
                print e
    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps

def searchIPHai():
    #http://www.iphai.com/free/ng
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):

            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': UserAgent,
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
                for para in table.findAll('tr')[1:20]:
                    Ip=para.findAll('td')[0].text.replace('\r\n','').replace(' ','')
                    Port=para.findAll('td')[1].text.replace('\r\n','').replace(' ','')
                    isHttps=para.findAll('td')[3].text.replace('\r\n','').replace(' ','')
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]
            except Exception, e:
                print e
    random.shuffle(proxyIps)
    # print proxyIps
    return proxyIps


def testPortIPs(PortIPs,check_url):
    vailnum=0
    passIps=[]
    for PortIP in PortIPs:
        try:
            #获取一个保存cookie的对象
            cj = cookielib.LWPCookieJar()
            #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
            cookie_support = urllib2.HTTPCookieProcessor(cj) 
            proxy_support = urllib2.ProxyHandler(PortIP)
            opener = urllib2.build_opener(cookie_support,proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)

            req = urllib2.Request(url=check_url)
            resp=urllib2.urlopen(req,timeout=3)
            html_details = resp.read()
            status=resp.getcode()
            resp.close()
            if status==200:
                vailnum+=1
                passIps+=[PortIP]
                print '代理IP地址%s,通过测试!!!'%str(PortIP)

            if vailnum==10:
                return passIps

        except Exception, e:
            print '代理IP地址%s,无法ping通核验的网页!!'%str(PortIP)
    return passIps





def vailProxyIPs(test_url):
    timeM=int(time.strftime("%M", time.localtime()))
    isSucessed=False
    while isSucessed==False:
        if 0<=timeM<5 or 25<=timeM<30 or 45<=timeM<50:
            ips=searchIPHai()
        elif 5<=timeM<15 or 30<=timeM<35 or 50<=timeM<55:
            ips=search66IP()
        elif 15<=timeM<20 or 35<=timeM<40 or 55<=timeM<60:
            ips=searchKDL()
        elif 20<=timeM<=25 or 40<=timeM<45:
            ips=searchXCDL()

        vailIPs=testPortIPs(ips,test_url)
        if vailIPs==[]:
            timeM+=12
            isSucessed=False
        elif timeM>=60:
            print '未能获得有效果代理IP，休息一会，下次再试！'
            return vailIPs
        else:
            isSucessed=True
            return vailIPs



if __name__ == '__main__':
    test_url='http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=info&vid=3&tid=1967'
    vailproxyips=vailProxyIPs(test_url)
    print vailproxyips






