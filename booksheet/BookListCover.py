# -*- coding: utf-8 -*-

import io,MySQLdb
#import ImageDraw
from PIL import Image,ImageDraw
try:
  # Python2
  from urllib2 import urlopen
except ImportError:
  # Python3
  from urllib.request import urlopen
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
base_path='/opt/www/api/attachment/imread/booksheet/cover/'

def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db) 
    cursor = conn.cursor() 
    return conn


def gaininfos(sheetid):
    try:
        host="192.168.0.34"
        user="ebook"
        passwd="ebook%$amRead"
        conn=linkSQL(host,user,passwd,'ebook_con')
        sql="""
        SELECT
  a.big_thumb
FROM
  con_book a,
  (
    SELECT
      content_id,sheet_id
    FROM
      con_booksheet_content
    WHERE
      content_type = 1
    AND sheet_id = """+str(sheetid)+"""
  ) b
WHERE
  a.book_id = b.content_id"""

        n = cursor.execute(sql)
        infos=[]
        for row in cursor.fetchall():
            infos.append(row[0])
        #print infos

        return infos

    except Exception, e:
        print e





def mergepicture(sheetid):
    try:
        picurl=gaininfos(sheetid)
        print picurl
        mxsize =600
        mysize =600  

        toImage = Image.new('RGBA', (mxsize,mysize),'#e7e7e7')  

        lowImage = Image.new('RGBA', (600, 80),'#ddd4c3')

        toImage.paste(lowImage,( 0, 520)) 

        i=0
        for url in  picurl:
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
            print xsize,xsize

            if i==1:
              x=50
              y=160
              fromImage_resized = fromImage.resize((270, 360), Image.ANTIALIAS)

            elif i==2:
              x=280
              y=160
              fromImage_resized = fromImage.resize((270, 360), Image.ANTIALIAS)

            elif i==3:
              x=135
              y=80
              fromImage_resized = fromImage.resize((330, 440), Image.ANTIALIAS)

            toImage.paste(fromImage_resized,( x, y)) 

          
        toImage.save(base_path+'cover'+str(sheetid)+'.jpg') 

    except Exception, e:
      raise e





if __name__ == '__main__':
    #gaininfos()
    #cutpicture()
    mergepicture(124446)
    # circle_corder_image()

