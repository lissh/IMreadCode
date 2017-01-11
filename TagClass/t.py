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

#print base_path
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
        for i in range(jobs_num):            
            bid=bids[i][0]
            self.add_job(compilingcontent,bid,i)
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
                global compilingcontents,book_id,book_counts
                do, args = self.work_queue.get(block=False)
                compilingcontent=''
                # if int(args[1])%100 ==0:
                #     #print 'sleep'
                #     time.sleep(2)
                if args[1]%50==0:
                    time.sleep(0.1)
                #print args[0]
                compilingcontent=do(args[0])[0]
                book_id=do(args[0])[1]
                #print book_id
                jieba_book =jieba.cut(compilingcontent)
                book_cut= " ".join(jieba_book).split(' ')

                stopwords=[line.replace('\n','').decode("gbk")   for line in open('stopwords.txt').readlines()]  
                book_lists = filter(lambda x: (not (len(x) <=1)),book_cut)
                book_counts=Counter(book_lists).most_common(1000)

                for book_tag in book_counts:
                    #print book_id,book_tag
                    
                    if book_tag not in stopwords and book_tag!=():
                        books_tag.append(str(book_id)+'|'+str(book_tag[0])+'|'+str(book_tag[1]))

                #         fbtags.write(str(book_id)+'|'+str(book_tag[0])+str(book_tag[1])+'\n')
                #print jieba_book


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


def jiebacut(compilingcontents):
    jieba.load_userdict("dict.txt")
    #print compilingcontents

    jieba_result =jieba.cut(compilingcontents)
    #print result
    words_cut= " ".join(jieba_result).split(' ')
    # print word_sets[7]

    word_lists = filter(lambda x: (not (len(x) <=1)),words_cut)
    counts=Counter(word_lists).most_common(1000)
    return counts





def compilingcontent(bid='380129107'):
    try:
        #bid='364771267'
        #print bid
        url_work = 'http://wap.cmread.com/r/p/viewdata.jsp?bid='+str(bid)+'&vt=9'
        work_content = urllib2.urlopen(url_work).read()
        work_point=re.findall('"showName":"(.*?)", "category":"(.*?)",.*?"desc":"(.*?)"', work_content)
        #print work_point[0]
        #print '1'
        if len(work_point)>=1:
            book_name=work_point[0][0]
            book_category=work_point[0][1]
            book_desc=work_point[0][2]
        else:
            book_name=''
            book_category=''
            book_desc=''
        #print book_name

        #"showName":"三国吕布逆转人生", "category":"历史",..."desc":"
        #man_bzzb=crawlbids(content)
        url_directory='http://wap.cmread.com/r/p/catalogdata.jsp?bid='+str(bid)+'&orderType=asc&page=1&pageSize=20&vt=9'
        directory_content = urllib2.urlopen(url_directory).read()
        directory_points=re.findall('"cid":"(\d+)", "chapterName":"(.*?)","tomeName":"(.*?)","feeType":', directory_content)
        book_content=''
        #print '2'
        # 获取张姐内容        
        # book_content=''
        #print directory_points
        for directory_point in directory_points:
            #cid=directory_point[0]
            if len(directory_point)<=2:
                chapterName=''
                tomeName='' 
            else:
                #print '2'
                chapterName=directory_point[1]
                tomeName=directory_point[2]

            book_content+=chapterName+tomeName 
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
        compilingcontents=book_name+';'+book_category+';'+book_desc+'\n'
        return compilingcontents,bid

    except Exception,e :
        print bid, e
        return None

def loadsql(class_id):
    try:
        host="192.168.0.34"
        user="ebook"
        passwd="ebook%$amRead"
        conn=linkSQL(host,user,passwd,'ebook_con')

        sql_bids="select source_bid ,class_name from con_book where book_status=1 and class_id="+str(class_id)+" limit 3000"
        bids=[]
        #class_name=''
        n = cursor.execute(sql_bids)
        for row in cursor.fetchall():
            bids.append(row)
            #class_name=str(row[1])
        #print bids
        return bids

    except Exception,e :
        print e
        return None


def work(class_id):
    try:
        global bids,compilingcontents,fbtags,books_tag
        books_tag=[]
        fbtags = open(base_path+"/books_tags.txt", 'a')
        fbtags.truncate()

        compilingcontents=''
        bids=loadsql(class_id)
        class_name=loadsql(class_id)[0][1]
        #print class_name

        #print bids
        length=len(bids)
        print length
        work_manager =  WorkManager(length,100)
        work_manager.wait_allcomplete()
        #print compilingcontents

        tagcounts=jiebacut(compilingcontents)

        stopwords=[line.replace('\n','').decode("gbk")   for line in open('stopwords.txt').readlines()]  
        
        fobj = open(base_path+"/nstopwords"+"_"+class_name+".txt", 'a')
        fobj.truncate()
        tags=[]
        for tagcount in tagcounts:

            if tagcount[0] not in stopwords:
                tags+=[tagcount[0]]

                fobj.write(str(tagcount[0])+','+str(tagcount[1])+'\n')
                #print tagcount[0],tagcount[1]

        for book_tag in books_tag:
            flog_tag=book_tag.split('|')[1]
                    #print book_id,book_tag
            if flog_tag in tags:
                fbtags.write(book_tag+'\n')

    except Exception,e :
        print e
        return None


if __name__ == '__main__':
    print '???'
    # work()
    # for class_id in range(1,2):
    #     print class_id
    #     start = time.time()
    #     work(class_id)
    #     end = time.time()
    #     print "cost all time: %s" % (end-start)



