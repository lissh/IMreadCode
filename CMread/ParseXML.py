# -*- coding:utf-8 -*-
__author__ = 'lish'

import bs4,re,urllib2,os,MySQLdb,random,requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ParseXML(object):

    def __init__(self):
        _headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Host':'wap.cmread.com',
                'Pragma':'no-cache',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
                }
        self.headers=_headers

    def XMLBs4(self,url,taginfos):
        req = urllib2.Request(url,headers=self.headers)
        xml_details = urllib2.urlopen(req).read()
        xml_details=xml_details.decode("utf-8").replace('~','')
        # print xml_details
        # if 'body' in xml_details:
            # print xml_details
            # xml_bady_detail=re.findall('<body>[^~]+</body>',xml_details)[0]
            # print xml_details
            # soup= bs4.BeautifulSoup(xml_details,'lxml')
        # else:
            # print xml_details
            # soup= bs4.BeautifulSoup(xml_details,'lxml')
            # print soup
        soup= bs4.BeautifulSoup(xml_details,'lxml')
        # print taginfos.keys()
        if 'taglocationmark' in taginfos.keys():
            tagname=taginfos['tagname']
            taglocationmark=taginfos['taglocationmark']
            tagre=taginfos['tagre']

            result=[]
            for para in soup.findAll(tagname,taglocationmark):
                tagReValue=tagre[0]
                tagReCont=tagre[1]

                tagresult=para[tagReValue]
                ReResult=re.findall(tagReCont,str(tagresult))
                if ReResult!=[]:
                    result+=ReResult
        else:
            tagname=taginfos['tagname']
            tagre=taginfos['tagre']

            result=[]
            for para in soup.findAll(tagname):
                tagReValue=tagre[0]
                tagReCont=tagre[1]
                try:
                    tagresult=para[tagReValue]
                    ReResult=re.findall(tagReCont,str(tagresult))
                    if ReResult!=[]:
                        result+=ReResult
                except Exception,e:
                    isSucess=True
                    # print '无效链接！'

        return result

    # def XMLJson(self):

class autoRenewBooks(object):

    def __init__(self):

        # self.host="192.168.0.34"
        # self.user="ebook"
        # self.passwd="ebook%$amRead"

        # self.host="100.98.73.21"
        self.host="rdsljqv187pt04s68726.mysql.rds.aliyuncs.com"
        self.user="ebook"
        self.passwd="4titbrVcvnP6LSFA"
        self.db='ebook_con'

    #链接数据库MySQL
    def linkSQL(self):
        self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset="utf8")
        self.cursor = self.conn.cursor()


    def RenewCategoryBooks(self,category_books,category_id,):
        update_book_url="http://readapi.imread.com/api/book/update?source_bid="
        nsql='select source_bid from con_book where source_bid in '+str(tuple(category_books))
        # print category_books
        n = self.cursor.execute(nsql.replace(',)',')'))
        nbids=[]
        for row in self.cursor.fetchall():
            nbids.append(str(row[0]))
        #print nbids,'hap'

        new_books=list(set(category_books)-set(nbids))
        for new_book in new_books:
            url=update_book_url+str(new_book)
            r = requests.get(url,timeout=5)
            print r
        bids=[]
        bidslist=[]
        i=0
        sql='select DISTINCT book_id from con_book where source_bid in '+str(tuple(category_books)).replace(',)',')')
        # print sql

        n = self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            bidslist.append(str(row[0]))
        bidslist = list(set(bidslist))
        random.shuffle(bidslist)

        # print bidslist

        # for bid in bidslist:
        #     i+=1
        #     bids.append(tuple([str(bid)]+[str(i)]))
        # desql="delete from ebook_con.con_category_content where category_id='"+str(category_id)+"' and content_type='1'"

        ##留4，5，6三个位置用于测试第三方书城，不更新
        if category_id in (121,131):
            isExistID_sql='select content_id from ebook_con.con_category_content where category_location  in (4,5,6) and category_id=' +str(category_id)
            n = self.cursor.execute(isExistID_sql)
            isExistID=[str(row[0]) for row in self.cursor.fetchall()]
            # print  isExistID_sql ,isExistID
            bidslist=list(set(bidslist)-set(isExistID))
            for bid in bidslist:
                i+=1
                if i >=4:
                    j=i+3
                else:
                    j=i
                #print j
                bids.append(tuple([str(bid)]+[str(j)]))
            # print bids
            desql="delete from ebook_con.con_category_content where category_id='"+str(category_id)+"' and content_type='1' and category_location not in (4,5,6)"
            # print desql
        else:
            for bid in bidslist:
                i+=1
                bids.append(tuple([str(bid)]+[str(i)]))
            desql="delete from ebook_con.con_category_content where category_id='"+str(category_id)+"' and content_type='1'"

        n = self.cursor.execute(desql)
        self.conn.commit()
        insql="insert into ebook_con.con_category_content(category_id,content_id,content_type,category_location,font_color) values('"+str(category_id)+"',%s,'1',%s,'333333')"
        # print bids,insql
        if len(bids)==1:
            print 'ok'
            n = self.cursor.execute(insql,bids[0])
            self.conn.commit()
        elif len(bids)==0:
            print 'Has not extracted bids !!!'
        else:
            n = self.cursor.executemany(insql,bids)
            self.conn.commit()



if __name__ == '__main__':
    headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Host':'wap.cmread.com',
                'Pragma':'no-cache',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    app=ParseXML(headers)

    url='http://wap.cmread.com/r/p/hbxs.jsp?'
    taginfos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=398177621')}
    bids=app.XMLbs4(url,taginfos)
    print bids,'???'