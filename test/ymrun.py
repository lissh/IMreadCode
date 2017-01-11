# -*- coding: utf-8 -*-
__author__ = 'lish'
from IMOpenAPI import imxmlapi as imxml
import imdb,imcrawl,os,sys
import ConfigParser

global base_url,base_path,imreaddb
conf_path=os.path.split( os.path.realpath( sys.argv[0] ) )[0]+'/'
cf = ConfigParser.ConfigParser()
cf.read(conf_path+"imopenapi.conf")

base_url = cf.get("prefixurl", "base_url")
base_path = cf.get("prefixpath", "base_path")

db_port = cf.getint("db", "db_port")
db_user = cf.get("db", "db_user")
db_host = cf.get("db", "db_host")
db_pass = cf.get("db", "db_pass")
imreaddb=imdb.IMReadDB(db_host,db_port,db_user,db_pass)




def crawlAPI(mcpid):
    selectsql='SELECT api_type,api_url from ebook_con.con_mcp_api where mcp_id=%s'%mcpid
    results=imreaddb.selectdb(selectsql)
    apiurls={}
    for result in results:
        apiurls=dict(apiurls,**{result[0]:str(result[1])})

    yuemingapp=imxml.IMxmlAPI(apiurls)


    bids=yuemingapp.BookIds()
    selectsql='select source_bid from ebook_con.con_book where mcp_id=%s'%mcpid
    isOldSids=[]
    results=imreaddb.selectdb(selectsql)
    for result in results:
        isOldSids.append(str(result[0]))
    isNewSids=list(set(bids)-set(isOldSids))


    if isOldSids!=[]:
        imcrawl.renewbooks(yuemingapp,imreaddb,isOldSids,mcpid)
    if isNewSids!=[]:
        imcrawl.addbooks(yuemingapp,imreaddb,isNewSids,mcpid)

    updatesql="""UPDATE ebook_con.con_book a
                    JOIN (
                        SELECT book_id, min(chapter_id) f_chpater_id, max(chapter_id) l_chpater_id
                        FROM ebook_con.con_chapter GROUP BY book_id ) b
                    ON (a.book_id = b.book_id)
                    SET
                      first_chpater_id = b.f_chpater_id,
                      last_chapter_id=b.l_chpater_id
                    WHERE
                        a.source_id=2 and a.mcp_id=%s"""%mcpid
    imreaddb.updatedb(updatesql)

if __name__ == '__main__':
    crawlAPI(128)

