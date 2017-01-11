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
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:
            
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
                for para in table.findAll('tr')[1::]:
                    Ip=para.findAll('td',{"data-title":"IP"})[0].text
                    Port=para.findAll('td',{"data-title":"PORT"})[0].text
                    Type=para.findAll('td',{"data-title":"类型"})[0].text
                    respSpeed=para.findAll('td',{"data-title":"响应速度"})[0].text
                    finalConfirmTime=para.findAll('td',{"data-title":"最后验证时间"})[0].text
                    isGetPost=para.findAll('td',{"data-title":"get/post支持"})[0].text
                    proxyIp = dict(http=str(Ip)+':'+str(Port))
                    proxyIps+=[proxyIp]


                isSucessed=True
            except Exception, e:
                print e
                trialNum+=1
                time.sleep(1)
                isSucessed=False
                print '代理IP情页没有解析成功，正在进行第%s次尝试！'%str(trialNum)
    random.shuffle(proxyIps)
    return proxyIps



def searchXCDL():
    UserAgent=getagent()
    proxyIps=[]
    try:
        # headers={
        #         'User-Agent': UserAgent,
        #         "Host":"www.xicidaili.com"

        #         };
        homeurl=['http://www.xicidaili.com/nn','http://www.xicidaili.com/nt']
        random.shuffle(homeurl)
        url = homeurl[1]
        print url

        req = urllib2.Request(url=url)
        content = urllib2.urlopen(req).read()
        # print content
        proxy_contents= re.findall('<td.*?/></td>\n\s+<td>(.*?)</td>\n\s+<td>(.*?)</td>',content)
        # print proxy_contents
        vailnum=0
        for proxy_content in proxy_contents:
            proxyIp = dict(http=str(proxy_content[0])+':'+str(proxy_content[1]))

            proxyIps+=[proxyIp]
        random.shuffle(proxyIps)
        return proxyIps

    except Exception, e:
        print e
        return proxyIps
        print '代理IP情页没有解析成功！'


def search66IP():
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:
            
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
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:
            
            try:
                headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': UserAgent,
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
    UserAgent=getagent()
    proxyIps=[]
    for page in range(1,2):
        isSucessed =False
        trialNum=0
        while isSucessed ==False and trialNum<=3:
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
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'Host':'www.meidebi.com'
                        };
    vailnum=0
    passIps=[]
    for PortIP in PortIPs:

        try:
            proxy_support = urllib2.ProxyHandler(PortIP)
            opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)

            req = urllib2.Request(url=check_url,headers=headers)
            resp=urllib2.urlopen(req,timeout=5)
            html_details = resp.read()
            # print html_details
            status=resp.getcode()
            resp.close()
            if status==200:
                vailnum+=1
                isSucessed=True
                passIps+=[PortIP]
                print '代理IP地址%s,通过测试!!!'%str(PortIP)
                # return passIps
            else:
                isSucessed=False

            if vailnum==3:
                return passIps

        except Exception, e:
            print '代理IP地址%s,无法ping通核验的网页!!'%str(PortIP)
    return passIps




def vailProxyIPs(test_url):
    ips=[]
    while ips==[]:
        flog=random.randint(1,2)
        if flog==1:
            ips=searchKDL()
        elif flog==2:
            ips=searchIPHai()
    vailIPs=testPortIPs(ips,test_url)
    return vailIPs



if __name__ == '__main__':
    # test_url='http://baby.ctdsb.net/plugin.php?id=tom_mengbao&mod=info&vid=3&tid=1967'
    test_url="http://www.meidebi.com/mao_n/"
    vailproxyips=vailProxyIPs(test_url)
    print vailproxyips






