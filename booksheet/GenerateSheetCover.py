# -*- coding: utf-8 -*-
__author__ = 'lish'
import io,MySQLdb
#import ImageDraw
from PIL import Image,ImageDraw
try:
  # Python2
  from urllib2 import urlopen
except ImportError:
  # Python3
  from urllib.request import urlopen
import requests
import hashlib
import base64
import sys,os,time,uuid
reload(sys)
sys.setdefaultencoding('utf-8')
base_path='/opt/www/api/attachment/imread/booksheet/cover/'
# isExists=os.path.exists(base_path)
# if not isExists:
#     os.makedirs(base_path)



def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
    cursor = conn.cursor()
    return conn


def gaininfos(sheetid):
    try:
        host="rdsljqv187pt04s68726.mysql.rds.aliyuncs.com"
        user="crawl"
        passwd="vDwoiExZ26jYaMsyZokz"
        conn=linkSQL(host,user,passwd,'ebook_con')

        sql="""
        SELECT
  a.big_thumb
FROM
  con_book a,
  (
    SELECT
      content_id,sheet_id,create_time
    FROM
      con_booksheet_content
    WHERE
      content_type = 1
    AND sheet_id = """+str(sheetid)+""" order by id desc
  ) b
WHERE
  a.book_id = b.content_id order by b.create_time desc limit 3"""

        n = cursor.execute(sql)
        infos=[]
        for row in cursor.fetchall():

            infos.append(row[0])
        print infos

        return infos

    except Exception, e:
        print e





def mergepicture(sheetid):
    try:
        picurl=gaininfos(sheetid)
        #print picurl
        mxsize =600
        mysize =600

        toImage = Image.new('RGBA', (mxsize,mysize),'#e7e7e7')

        lowImage = Image.new('RGBA', (600, 80),'#ddd4c3')

        toImage.paste(lowImage,( 0, 520))

        i=0
        for url in  picurl[2::-1]:
            i+=1
            try:
              image_bytes = urlopen(url).read()
            except:
              continue
            data_stream = io.BytesIO(image_bytes)
            # open as a PIL image object
            fromImage = Image.open(data_stream)
            #fromImage = Image.open(url)

            fromImage_resized = fromImage.resize((180, 240), Image.ANTIALIAS)
            xsize,ysize=fromImage_resized.size
            #print xsize,xsize

            if i==3:

              x=135
              y=80

              fromImage_resized = fromImage.resize((330, 440), Image.ANTIALIAS)

            elif i==1:
              x=280
              y=160

              fromImage_resized = fromImage.resize((270, 360), Image.ANTIALIAS)

            elif i==2:
              x=50
              y=160

              fromImage_resized = fromImage.resize((270, 360), Image.ANTIALIAS)

            toImage.paste(fromImage_resized,( x, y))


        lists = os.listdir(base_path)
        #print lists
        for tt in lists:
            if sheetid in tt:
                print tt
                os.remove(base_path+tt)

        image_path=base_path+'cover180240_'+str(sheetid)+'_'+str(uuid.uuid1()).replace('-','')+'.jpg'
        toImage.save(image_path)


        image_url=str(image_path.replace('/opt/www/','http://static.imread.com/'))
        sql="update ebook_con.con_booksheet set image_url='"+image_url+"' where sheet_id="+str(sheetid)
        n=cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

        # host="192.168.0.34"
        # user="ebook"
        # passwd="ebook%$amRead"
        # conn=linkSQL(host,user,passwd,'ebook_con')



        print image_url

        release_cdn(image_url)

    except Exception, e:
      raise e

def release_cdn(image_url):

    passwd=hashlib.md5(hashlib.sha1('KEUswIa+Tc5/L').hexdigest()).hexdigest()
    url = 'http://push.dnion.com/cdnUrlPush.do'
    data = dict(
        username ='51ss',
        password = passwd,
        url = image_url,
        type='0'
    )
    r = requests.post(url,data=data)
    print r.headers
    print r.status_code




if __name__ == '__main__':
    #gaininfos()

    mergepicture(sys.argv[1])




