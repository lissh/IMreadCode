# -*- coding: utf-8 -*-
import Queue
import threading
import time
import urllib2
import urllib,random
import re,json,os
import sys,time
import ConfigParser
import requests,MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]
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
        for i in range(jobs_num):
            print i
            if i%10==0:
                time.sleep(0.1)
            bid=bids[i]
            self.add_job(main,bid)

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
                do, args = self.work_queue.get(block=False)
                # if int(args[1])%100 ==0:
                #     #print 'sleep'
                #     time.sleep(2)
                #print args[1]
                do(args[0])
                self.work_queue.task_done()
            except Exception,e:
                print str(e)
                break



#print base_path

def crawl(content,type):
    try:
        if type=='bids':
            bids=re.findall('<bookid><!\[CDATA\[(\d+)\]\]></bookid>', content)
            return bids
        elif type=='info':
            info=[]
            info_re="<bookid><!\[CDATA\[(\d+)\]\]></bookid>\r\n<bookname><!\[CDATA\[(.*?)\]\]></bookname>\r\n<authorname><!\[CDATA\[(.*?)\]\]></authorname>\r\n<intro><!\[CDATA\[(.*?)\]\]></intro>\r\n<genre><!\[CDATA\[(.*?)\]\]></genre>\r\n<bookstatus><!\[CDATA\[(\d)\]\]></bookstatus>\r\n<keywords><!\[CDATA\[(.*?)\]\]></keywords>\r\n<coverpath><!\[CDATA\[(.*?)\]\]></coverpath>"
            infos=re.findall(info_re, content)
            for info in infos:
                info_content=''
                for infochild in info:
                    info_content+=infochild.replace('|','').replace('\n','')+'|'
                # finfo.write(info_content+'\n')
            return infos
        elif type=='index':
            index=[]
            index_bid=re.findall('<bookid><!\[CDATA\[(\d+)\]\]></bookid>', content)
            index_volumei=re.findall('<volumeid><!\[CDATA\[(\d+)\]\]></volumeid>', content)
            index_volname=re.findall('<volname><!\[CDATA\[(.*?)\]\]></volname>', content)
            index_conts=re.findall('<chapterid><!\[CDATA\[(\d+)\]\]></chapterid>\r\n<chaptername><!\[CDATA\[(.*?)\]\]></chaptername>', content)


            for index_cont in index_conts:
                index_content=index_cont[0]+'|'+index_cont[1].replace('|','')
                index+=[tuple(index_bid)+tuple(index_volumei)+tuple(index_volname)+index_cont]
                # findex.write(str(index_bid[0])+'|'+str(index_volumei[0])+'|'+str(index_volname[0]).replace('|','')+'|'+str(index_content)+'\n')
            return  index
    except Exception,e :
        print e

def main(bid):
        #print bid
        # #print bid


        url2 = 'http://www.qmcmw.com/api/shuqi_info.php?id='+str(bid)
        content2 = urllib2.urlopen(url2).read()
        # url3 = 'http://www.qmcmw.com/api/shuqi_chapter.php?id='+str(bid)
        # content3 = urllib2.urlopen(url3).read()
        info=crawl(content2,'info')
        return info
        # time.sleep(0.1)
        # index=crawl(content3,'index')
        

        # if content2!=None:
        #     #print '1'
        #     info=crawl(content2,'info')


        # url3 = 'http://www.qmcmw.com/api/shuqi_chapter.php?id='+str(bid)
        # content3 = urllib2.urlopen(url3).read()
        # if content3!=None:
        #     print '2'
        #     index=crawl(content3,'index')
        # else:
        #     continue


def gainbid():
    try:
        #print '2'
        global bids
        start = time.time()
        global findex ,finfo
        findex=open('index.txt','a+')
        finfo=open('info.txt','a+')


        url = 'http://www.qmcmw.com/api/shuqi_list.php?page=1'
        content1 = urllib2.urlopen(url).read()
        bids=crawl(content1,'bids')[0:50]
        print bids
        print len(bids)

        work_manager =  WorkManager(len(bids),10)
        work_manager.wait_allcomplete()

        findex.close()
        finfo.close()
        end = time.time()
        print "cost all time: %s" % (end-start) 
    except Exception,e :
        print e




if __name__ == '__main__':
    gainbid()
