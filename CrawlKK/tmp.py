# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2,re,urllib,json,time,bs4
import MySQLdb,random,os,StringIO,gzip
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
base_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]

# isExists=os.path.exists(base_path+u'/391275/charpters/412118793.txt')
# if not isExists:
#     print '???'

def test():
            pathlist = os.listdir(base_path)
            print pathlist
            checkHasendZIP = False
            # for filename in pathlist:
            #       if filename.endswith('zip'):
            #             checkHasendZIP  = True
            # if checkHasendZIP:
            #     # 解压zip文件
            #
            #
            #     # 替换错误或者带标记的字符
            #     sedcommand1="sed -i 's/kuaikanxiaoshuo/imreadorg/g' "+base_path+'/'+str(bookid)+"/charpters/*.txt"
            #     os.system(sedcommand1)
            #
            #     sedcommand2="sed -i 's/快看小说/艾美阅读/g' "+base_path+'/'+str(bookid)+"/charpters/*.txt"
            #     os.system(sedcommand2)


test()