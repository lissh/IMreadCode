# -*- coding: utf-8 -*-
__author__ = 'lish'
import time,random,re,json
import urllib2,urllib,datetime
import ConfigParser
import sys,os,json
reload(sys)
reload(sys)
sys.setdefaultencoding('utf-8')
conf_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/'
cf = ConfigParser.ConfigParser()
cf.read(conf_path+"imopenapi.conf")

base_url = cf.get("prefixurl", "base_url")
base_path = cf.get("prefixpath", "base_path")

#####测试接口,接口类型：1:分类列表 2:图书列表 3:图书信息 4:章节列表  5:章节内容
test_apiurls={1:cf.get("test_apiurls", "1"),2:cf.get("test_apiurls", "2"),3:cf.get("test_apiurls", "3"),4:cf.get("test_apiurls", "4"),5:cf.get("test_apiurls", "5")}






class IMJsonAPI(object):
    def __init__(self,apiurls):
        self.APIurls=apiurls

    def BookCategorys(self):
        url=self.APIurls[1]
        req = urllib2.Request(url)
        content =urllib2.urlopen(req).read()

        bejson=json.loads(str(content))
        bookcategorys={}
        for apidata in bejson['data']:
            categoryid= apidata['categoryid']
            categoryname= apidata['categoryname']
            bookcategorys=dict(bookcategorys,**{str(categoryid):str(categoryname)})
        return bookcategorys 

    def BookIds(self):
        url=self.APIurls[2]
        req = urllib2.Request(url)
        content =urllib2.urlopen(req).read()

        bejson=json.loads(str(content))
        bids=[]
        for apidata in bejson['data']:
            bids.append(apidata['bookid'])
        return bids


    def BookInfos(self,source_bid,mcpid):
        sbid=source_bid
        url=self.APIurls[3]%sbid
        para=dict(id=sbid)
        req = urllib2.Request(url,urllib.urlencode(para))
        content =urllib2.urlopen(req).read()
        # content='{"error_code": 0,"data": [{"bookid": "776","bookname": "衰哥成长记","authorname": "苍龙雄心","brief": "风尘大陆……意向不到的变化。","classid": "23","classname": "玄幻奇幻","bookstatus": "1","keywords": "苍龙雄心,热血,衰神","coverpath": " http://www.xx.xx.jpg","pritce": "500","pricetype": "2","serialize_status": "0","chaptercount": "90","freechaptercount": "20","wordcount": "1.3万字","score": "4.3","lastupdatetime": "1434782898"}]}'
        bejson=json.loads(content)
        apidatas=bejson['data']
        if not isinstance(apidatas,dict):
            apidatas=apidatas[0]
        # print apidatas,'??1'
        keys=['bookid','bookname','authorname','brief','classid','classname','bookstatus','keywords','coverpath','price','pricetype','serialize_status','chaptercount','freechaptercount','wordcount','score','lastupdatetime']
        keyconts={'mcpid':mcpid}

        for key in keys:
            keycont=apidatas[key]
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
        # content='{"error_code": 0,"data": [{"bookid": "776","chapterid": "45218","chaptername": "第一章 楚家楚焰","volumeid": "0","volumename": "第一篇","pricetype": "0","createtime": "1434782898"}]}'
        bejson=json.loads(content)
        apidatas=bejson['data']

        chapterrank=0
        bookchapterinfos=[]
        for apidata in apidatas:
            if book_id!=0:
                keyconts={'source_bid':int(sbid),'book_id':int(book_id)}
            else:
                keyconts={'source_bid':int(sbid)} 
            chapterrank+=1
            chapterid=apidata['chapterid']
            pricetype=apidata['pricetype']
            chaptername=apidata['chaptername']

            ##处理卷名
            volumename=apidata['volumename']
            if volumename=='' or volumename==None:
                volumename=''
            if '篇' in volumename:
                try:
                    volumename=re.findall(u'([\u4e00-\u9fa5]+篇)',str(volumename).decode('utf8'))[0]+' '
                except Exception, e:
                    volumename=re.findall(u'(篇[\u4e00-\u9fa5]+)',str(volumename).decode('utf8'))[0]+' '
            elif '卷' in volumename:
                try:
                    volumename=re.findall(u'([\u4e00-\u9fa5]+卷)',str(volumename).decode('utf8'))[0]+' '
                except Exception, e:
                    volumename=re.findall(u'(卷[\u4e00-\u9fa5]+)',str(volumename).decode('utf8'))[0]+' '
            elif '集' in volumename:
                volumename=re.findall(u'([\u4e00-\u9fa5]+集)',str(volumename).decode('utf8'))[0]+' '
            elif '册' in volumename:
                volumename=re.findall(u'([\u4e00-\u9fa5]+册)',str(volumename).decode('utf8'))[0]+' '
            else:
                volumename=''
            ##处理卷名更新时间
            updatetime=apidata['updatetime']
            timeArray= time.localtime(float(updatetime))
            #该章节更新的时间
            MyStyleTime= time.strftime("%Y-%m-%d %H:%M:%S",timeArray)##用作判断更新时间
            #昨天的时间
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            YesTime=yes_time.strftime("%Y-%m-%d %H:%M:%S")
            if book_id!=0:
                if MyStyleTime>YesTime:
                    bookchapterinfos.append({'source_bid':int(sbid),'book_id':int(book_id),'chapter_id':int(chapterid),'chapter_name':str(volumename+chaptername),'price_type':int(pricetype),'chapter_rank':int(chapterrank)})
            else:
                bookchapterinfos.append({'source_bid':int(sbid),'chapter_id':int(chapterid),'chapter_name':str(volumename+chaptername),'price_type':int(pricetype),'chapter_rank':int(chapterrank)})
        return bookchapterinfos

    def BookChapterCont(self,chapterinfos):
        sbid=chapterinfos['source_bid']
        cid=chapterinfos['chapter_id']
        url=self.APIurls[5]%(sbid,cid)

        para=dict(id=sbid,cid=cid)
        content = urllib2.urlopen(urllib2.Request(url,urllib.urlencode(para)),timeout=5).read().replace('<![CDATA[','').replace(']]>','')
        bejson=json.loads(content)

        apidatas=bejson['data']
        if not isinstance(apidatas,dict):
            apidatas=apidatas[0]
        cont=apidatas['chaptercont']
        wordscount=len((cont.replace('\n','')).encode("gbk").decode("gbk"))
        if len(chapterinfos)==3:            
            bid=chapterinfos['bookid']
            chapterpath=base_path+'%s/charpters/%s.txt'%(bid,cid)
            fw=open(chapterpath,'w')
            fw.write(cont)
            fw.close()

        return wordscount

if __name__ == '__main__':
    mcpid=128
    app=IMJsonAPI(test_apiurls)
    # bookinfos=app.BookInfos(1920,mcpid)
    bookinfos=app.BookChapterIds(1920,46465)
    # bookinfos=app.BookChapterCont({'bookid': 128, 'chapterid': 193971, 'chapterrank': 184, 'sourcebid': 1920, 'chaptername': '\xe7\xac\xac\xe4\xb8\x80\xe7\x99\xbe\xe5\x85\xab\xe5\x8d\x81\xe4\xb8\x89\xe7\xab\xa0\xef\xbc\x9a\xe7\xbc\x94\xe9\x80\xa0\xe6\x96\xb0\xe7\xa7\xa9\xe5\xba\x8f', 'pricetype': 2})
    print str(tuple(bookinfos[0].keys())).replace("'",'')
    print bookinfos[0].values()
    print bookinfos[0].items()
