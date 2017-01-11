
import requests,urllib2
import os,re,urllib,json,random,time,decimal,hashlib
import base64,sys
from xml.dom.minidom import parse
import xml.dom.minidom

import smtplib
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import threading

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
    def join(self):
        threading.Thread.join(self)
        return self._return

def visit_all():


    url = 'http://192.168.0.34:9090/api/book/introduce?bid=196790'
    # url = 'http://192.168.0.3:8004/cmread'
    content = urllib2.urlopen(urllib2.Request(url=url,headers = headers),timeout=5).read()
    r = requests.get(url)
    print r.text

def main():
    print ""
    threads = []
    for i in xrange(0,200):
        threads.append(ThreadWithReturnValue(target=visit_all))
    for t in threads:
        t.start()

if __name__ == '__main__':
    main()