# -*- coding: utf-8 -*-
import Queue
import threading
import urllib2
import jieba
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import MySQLdb
import pandas as pd
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

print base_path
class WorkManager(object):
    def __init__(self, work_num=1000,thread_num=2):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)

    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))
    def __init_work_queue(self, jobs_num):
        #print jobs_num
        #compilingcontents[i]=''
        for i in range(jobs_num):
            
            bid=bids[i]
            self.add_job(compilingcontent,bid,i)
            #print compilingcontent
            #compilingcontents+=compilingcontent

    def add_job(self, func, *args):
        #print args
        self.work_queue.put((func, list(args)))

    def check_queue(self):
        return self.work_queue.qsize()

    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                global compilingcontents
                do, args = self.work_queue.get(block=False)
                compilingcontent=''
                # if int(args[1])%100 ==0:
                #     #print 'sleep'
                #     time.sleep(2)
                if args[1]%50==0:
                    time.sleep(0.1)
                #print args[0]
                compilingcontent=do(args[0])
                compilingcontents+=compilingcontent
                #print compilingcontent
                #return compilingcontent
                #

                self.work_queue.task_done()
            except Exception,e:
                print str(e)
                break



#链接数据库MySQL
def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset="utf8") 
    cursor = conn.cursor() 
    return conn
#print base_path

def CrawlDetails(content,nid=None):
    try:
        if nid==None:
            bids=re.findall('/r/(\d+)/index', content)
        else:
            bids=re.findall('/r/(\d+)/index.*?nid='+str(nid), content)
        return bids
    except Exception,e :
        print e
        return None
def jiebacut(compilingcontents):
    jieba.load_userdict("dict.txt")
    # stopwords=[line.strip() for line in open('stopwords.txt').readlines()]  
    # #print stopwords,compilingcontents
    # #print stopwords[1:50]
    # stopwords=['谢楠']



    jieba_result =jieba.cut(compilingcontents)
    #print result
    words_cut= " ".join(jieba_result).split(' ')
    # print word_sets[7]


    # print u'程序处理中，请等待...'
    # word_sets=[]
    # jiebas=jieba.cut_for_search(compilingcontents) #jieba.cut_for_search() 结巴分词搜索引擎模式     
    # fenci_key=" ".join(list(set(jiebas)-set(stopwords))) #使用join链接字符串输出
    # word_sets=fenci_key.strip().split(' ')  #将数据添加到list1列表  




    word_lists = filter(lambda x: (not (len(x) <=1)),words_cut)
    counts=Counter(word_lists).most_common(500)
    return counts
    #print word_list
    # for count in counts:
    #     print count[0]
    #     if len(count[0])<=1:
    #         continue
    #     print count
        #print dic.keys()
        #if word_list in dic.keys():





def compilingcontent(bid='380129107'):
    try:
        #bid='364771267'
        #print bid
        url_work = 'http://wap.cmread.com/r/p/viewdata.jsp?bid='+bid+'&vt=9'
        work_content = urllib2.urlopen(url_work).read()
        work_point=re.findall('"showName":"(.*?)", "category":"(.*?)",.*?"desc":"(.*?)"', work_content)

        book_name=work_point[0][0]
        book_category=work_point[0][1]
        book_desc=work_point[0][2]

        #"showName":"三国吕布逆转人生", "category":"历史",..."desc":"
        #man_bzzb=crawlbids(content)
        url_directory='http://wap.cmread.com/r/p/catalogdata.jsp?bid='+bid+'&orderType=asc&page=1&pageSize=20&vt=9'
        directory_content = urllib2.urlopen(url_directory).read()
        directory_points=re.findall('{"cid":"(\d+)", "chapterName":"(.*?)".*?feeType":', directory_content)
        book_content=''

        # 获取张姐内容        
        # book_content=''
        for directory_point in directory_points:
            #cid=directory_point[0]
            if len(directory_point)==1:
                chapterName=''
            else:
                chapterName=directory_point[1]
            book_content+=chapterName 
        #     print cid,chapterName
        #     #book_content+=chapterName
        #     url_charpter='http://wap.cmread.com/r/'+bid+'/'+cid+'/index.htm?page=1&vt=9&cm=M2040002'
        #     charpter_content = urllib2.urlopen(url_charpter).read()
        #     print charpter_content,url_charpter
        #     charpter_point=re.findall('{"content":"(.*?)",\s+"name":"', charpter_content.replace('\n',''))
        #     print '2',charpter_point
        #     if charpter_point!=[]:
        #         charpter_content=charpter_point[0].replace('<br/>','').replace('&nbsp;','')
        #     book_content+='\n'+chapterName+'\n'+charpter_content
        #jieba.load_userdict("user.dict")    
        compilingcontent=book_name+'\n'+book_category+'\n'+book_desc
        #print book_name
        #cuttest(jiebatags)
        #print book_name
        return compilingcontent

    except Exception,e :
        print bid, e
        return None

def loadsql(class_id):
    try:
        host="192.168.0.34"
        user="ebook"
        passwd="ebook%$amRead"
        conn=linkSQL(host,user,passwd,'ebook_con')

        sql_bids="select source_bid  from con_book where book_status=1 and class_id="+str(class_id)+" limit 3000"
        bids=[]
        n = cursor.execute(sql_bids)
        for row in cursor.fetchall():
            bids.append(str(row[0]))
        return bids

    except Exception,e :
        print e
        return None


def work(class_id):
    try:
        global bids,compilingcontents
        compilingcontents=''
        bids=loadsql(class_id)
        #print bids
        length=len(bids)
        work_manager =  WorkManager(length,50)
        work_manager.wait_allcomplete()
        #print compilingcontents

        # compilingcontents=''
        # for bid in bids:
        #     compilingcontents+=compilingcontent(bid)

        #print compilingcontents
        tagcounts=jiebacut(compilingcontents)
        line=open('stopwords.txt').readlines()
        #print line

        stopwords=[line.replace('\n','').decode("gbk")   for line in open('stopwords.txt').readlines()]  
        
        fobj = open(base_path+"/nstopwords"+"_"+time.strftime("%Y%m%d")+".txt", 'a')
        fobj.truncate()

        for tagcount in tagcounts:

            if tagcount[0] not in stopwords:

                fobj.write(str(tagcount[0])+','+str(tagcount[1])+'\n')
                print tagcount[0],tagcount[1]



    except Exception,e :
        print e
        return None


if __name__ == '__main__':
    # work()
    for class_id in range(2,10):
        print class_id
        start = time.time()
        work(class_id)
        end = time.time()
        print "cost all time: %s" % (end-start)



