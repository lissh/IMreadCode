# -*- coding: utf-8 -*-
__author__ = 'lish'
import jieba
import re,json,os
import sys,time
import MySQLdb
import string
import pandas as pd
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]


def gainBookInfos():
    binfos_sql="select book_id,book_tag,book_name,book_brief,class_name from ebook_con.con_book where book_status=1 limit 100"
    n=cursor.execute(binfos_sql)
    booktagslist=[row[1] for row in cursor.fetchall()]
    cutcont=[]
    for booktags in booktagslist[2:3]:
        jieba_result =jieba.cut(booktags)
        cutcont+=[" ".join(jieba_result)]
        words_cut= " ".join(jieba_result).split(' ')
        print " ".join(jieba_result)
        word_lists = filter(lambda x: (not (len(x) <=1)),words_cut)
        counts=Counter(word_lists).most_common(500)
        for count in counts:
            print count[0],count[1]

    # print cutcont
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(cutcont))
    word = vectorizer.get_feature_names()  #所有文本的关键字
    weight = tfidf.toarray()

    # print  weight
    for i in range(len(weight)):
        print u"-------这里输出第",i,u"类文本的词语tf-idf权重------"
        for j in range(len(word)):
            print word[j],weight[i][j]




if __name__ == '__main__':
    global cursor,conn
    host="192.168.0.34"
    user="ebook"
    passwd="ebook%$amRead"
    db='ebook_con'
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
    cursor = conn.cursor()
    gainBookInfos()