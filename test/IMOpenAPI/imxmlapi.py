# -*- coding: utf-8 -*-
__author__ = 'lish'
import os,time,random,re,datetime
import xml.dom.minidom
import urllib2,urllib
import ConfigParser
import sys,string,os
reload(sys)
sys.setdefaultencoding('utf-8')
conf_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/'
cf = ConfigParser.ConfigParser()
cf.read(conf_path+"imopenapi.conf")

base_url = cf.get("prefixurl", "base_url")
base_path = cf.get("prefixpath", "base_path")
#####测试接口,接口类型：1:分类列表 2:图书列表 3:图书信息 4:章节列表  5:章节内容
test_apiurls={1:cf.get("test_apiurls", "1"),2:cf.get("test_apiurls", "2"),3:cf.get("test_apiurls", "3"),4:cf.get("test_apiurls", "4"),5:cf.get("test_apiurls", "5")}

class IMxmlAPI(object):

    def __init__(self,apiurls):
        self.APIurls=apiurls

    def BookCategorys(self):
        url=self.APIurls[1]
        req = urllib2.Request(url)
        content =urllib2.urlopen(req).read()
        DOMTree = xml.dom.minidom.parseString(content)
        bidsdata = DOMTree.documentElement.getElementsByTagName('category')
        bids=[]
        bookcategorys={}
        for biddata in bidsdata:
            categoryid=biddata.getElementsByTagName('cate_id')[0].childNodes[0].data
            categoryname=biddata.getElementsByTagName('cate_name')[0].childNodes[0].data
            bookcategorys=dict(bookcategorys,**{str(categoryid):str(categoryname)})
        # print bookcategorys
        return bookcategorys     

    def BookIds(self):
        url=self.APIurls[2]
        req = urllib2.Request(url)
        content =urllib2.urlopen(req).read()
        DOMTree = xml.dom.minidom.parseString(content)
        bidsdata = DOMTree.documentElement.getElementsByTagName('bookid')
        bids=[]
        for biddata in bidsdata:
            bids.append(biddata.childNodes[0].data)
        return bids
 

    def BookInfos(self,source_bid,mcpid):
        sbid=source_bid
        url=self.APIurls[3]%sbid
        para=dict(id=sbid)
        req = urllib2.Request(url,urllib.urlencode(para))
        content =urllib2.urlopen(req).read()
        DOMTree = xml.dom.minidom.parseString(content)
        bookinfo = DOMTree.documentElement
        keys=['bookid','bookname','authorname','brief','classid','classname','bookstatus','keywords','coverpath','price','pricetype','serialize_status','chaptercount','freechaptercount','wordcount','score','lastupdatetime']
        keyconts={'mcpid':mcpid}
        for key in keys:
            if bookinfo.getElementsByTagName(key)!=[]:
                keycont=bookinfo.getElementsByTagName(key)[0].childNodes[0].data.replace(']','')
                if  keycont!='':
                    if key in ('classid','bookid','bookstatus','price','pricetype','serialize_status','chaptercount','freechaptercount'):
                        keycont=int(keycont)
                    elif key=='lastupdatetime':
                        timeArray= time.localtime(float(keycont))
                        otherStyleTime= time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
                        keycont=otherStyleTime
                    elif key=='wordcount':
                        keycont=str(float(keycont)/1000)+'万'  
                    else:
                        keycont=str(keycont)
                keyconts=dict(keyconts,**{str(key):keycont})
        return keyconts


    def BookChaptersinfos(self,source_bid,book_id=0):
        sbid=source_bid
        url=self.APIurls[4]%sbid
        para=dict(id=sbid)
        req = urllib2.Request(url,urllib.urlencode(para))
        content =urllib2.urlopen(req).read()
        DOMTree = xml.dom.minidom.parseString(content)
        chapterinfo = DOMTree.documentElement
        # print chapterinfo
        volumes = chapterinfo.getElementsByTagName("volume")
        chapterinfos=[]
        chapterrank=0
        for volume in volumes:
            # vid=volume.getElementsByTagName('volumeid')[0].childNodes[0].data #卷ID
            vname=volume.getElementsByTagName('volname')[0].childNodes[0].data #卷名
            if vname==None:
                vname=''
            if '篇' in vname:
                try:
                    vname=re.findall(u'([\u4e00-\u9fa5]+篇)',str(vname).decode('utf8'))[0]+' '
                except Exception, e:
                    vname=re.findall(u'(篇[\u4e00-\u9fa5]+)',str(vname).decode('utf8'))[0]+' '
            elif '卷' in vname:
                try:
                    vname=re.findall(u'([\u4e00-\u9fa5]+卷)',str(vname).decode('utf8'))[0]+' '
                except Exception, e:
                    vname=re.findall(u'(卷[\u4e00-\u9fa5]+)',str(vname).decode('utf8'))[0]+' '
            elif '集' in vname:
                vname=re.findall(u'([\u4e00-\u9fa5]+集)',str(vname).decode('utf8'))[0]+' '
            elif '册' in vname:
                vname=re.findall(u'([\u4e00-\u9fa5]+册)',str(vname).decode('utf8'))[0]+' '
            else:
                vname=''
            # print vname

            chapters = volume.getElementsByTagName("chapters")[0].getElementsByTagName("chapter")
            for chapter in chapters:
                chapterrank+=1
                chapterid=chapter.getElementsByTagName('chapterid')[0].childNodes[0].data
                chaptername=chapter.getElementsByTagName('chaptername')[0].childNodes[0].data
                pricetype=chapter.getElementsByTagName('pricetype')[0].childNodes[0].data
                updatetime=chapter.getElementsByTagName('update_time')[0].childNodes[0].data
                timeArray= time.localtime(float(updatetime))
                #该章节更新的时间
                MyStyleTime= time.strftime("%Y-%m-%d %H:%M:%S",timeArray)##用作判断更新时间
                #昨天的时间
                now_time = datetime.datetime.now()
                yes_time = now_time + datetime.timedelta(days=-1)
                YesTime=yes_time.strftime("%Y-%m-%d %H:%M:%S")
                if book_id!=0:
                    if MyStyleTime>YesTime:
                        chapterinfos.append({'source_bid':int(sbid),'book_id':int(book_id),'chapter_id':int(chapterid),'chapter_name':str(vname+chaptername),'price_type':int(pricetype),'chapter_rank':int(chapterrank)})
                else:
                    chapterinfos.append({'source_bid':int(sbid),'chapter_id':int(chapterid),'chapter_name':str(vname+chaptername),'price_type':int(pricetype),'chapter_rank':int(chapterrank)})
    
        # print chapterinfos
        return chapterinfos

    def BookChapterCont(self,chapterinfos):
       
        sbid=chapterinfos['source_bid']
        cid=chapterinfos['chapter_id']
        
        url=self.APIurls[5]%(sbid,cid)
        para=dict(id=sbid,cid=cid)
        try:
            content = urllib2.urlopen(urllib2.Request(url,urllib.urlencode(para)),timeout=3).read().replace('<![CDATA[','').replace(']]>','')
            DOMTree = xml.dom.minidom.parseString(str(content))
            contentinfo = DOMTree.documentElement
            contents=contentinfo.getElementsByTagName('chaptercont')
            cont=''
            for content in contents:
                cont+=content.childNodes[0].data+'\n'
            if cont!='':
                wordscount=len(cont.replace('\n',''))
            if len(chapterinfos)==3:

                bid=chapterinfos['bookid']
                print '正在处理图书SID:%s,BID:%s的章节CID:%s'%(sbid,bid,cid) 
                chaptercontpath=base_path+'%s/charpters/%s.txt'%(bid,cid)

                fw=open(chaptercontpath,'w')                   
                fw.write(cont)
                fw.close()
            return (cid,wordscount)
        except Exception,e:
            return 0







if __name__ == '__main__':
    mcpid=128
    app=IMxmlAPI(test_apiurls)
    # bookinfos=app.BookInfos(1920,mcpid)
    bookinfos=app.BookChapterIds(1920,46465)
    # bookinfos=app.BookChapterCont({'bookid': 128, 'chapterid': 193971, 'chapterrank': 184, 'sourcebid': 1920, 'chaptername': '\xe7\xac\xac\xe4\xb8\x80\xe7\x99\xbe\xe5\x85\xab\xe5\x8d\x81\xe4\xb8\x89\xe7\xab\xa0\xef\xbc\x9a\xe7\xbc\x94\xe9\x80\xa0\xe6\x96\xb0\xe7\xa7\xa9\xe5\xba\x8f', 'pricetype': 2})
    print str(tuple(bookinfos[0].keys())).replace("'",'')
    print bookinfos[0].values()
    print bookinfos[0].items()
