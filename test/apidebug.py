# -*- coding: utf-8 -*-
__author__ = 'lish'
from IMOpenAPI import imxmlapi as imxml
from IMOpenAPI import imjsonapi as imjson
import imdb
import json,sys,os
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


def testAPI(mcpid,conttype,apitype):

    #####获得指定MCP的apiurls字典
    selectsql='SELECT api_type,api_url from ebook_con.con_mcp_api where mcp_id=%s'%mcpid
    results=imreaddb.selectdb(selectsql)
    apiurls={}
    for result in results:
        apiurls=dict(apiurls,**{result[0]:str(result[1])})



    
    #####判读MCP选择的接口类型，接口内容类型：1:xml  2:json
    if int(conttype)==1:
        app=imxml.IMxmlAPI(apiurls)
    elif int(conttype)==2:
        app=imjson.IMJsonAPI(apiurls)


    #####测试接口,接口类型：1:分类列表 2:图书列表 3:图书信息 4:章节列表  5:章节内容
    if int(apitype)==1:
        try:
            categorysinfos=app.BookCategorys()
            if categorysinfos!={}:
                ###查已经存在的分类信息，剔除
                selectsql='SELECT mcp_class_id from ebook_con.con_mcp_class where mcp_id=%s'%mcpid
                results=imreaddb.selectdb(selectsql)
                isExistCategorys=[int(result[0]) for result in results]
                categoryinfos=[]
                for key,value in categorysinfos.items():
                    if int(key) not in  isExistCategorys:
                        categoryinfos.append((int(mcpid),int(key),value))
                if categoryinfos!=[]:
                    insertsql='INSERT ebook_con.con_mcp_class (mcp_id,mcp_class_id,mcp_class_name) values (%s,%s,%s)'
                    imreaddb.insertdb(insertsql,categoryinfos)

                updatesql='UPDATE ebook_con.con_mcp_api SET api_status=1 where mcp_id=%s and api_type=%s'%(mcpid,apitype)
                imreaddb.insertdb(updatesql)

                return 0,'大官人,审核成功了!'
            else:
                return 301,'分类接口内容获取为空,接口返回内容格式不标准!'
        except Exception, e:
            return 401,'接口格式或者接口数据类型选择有误!\n(接口格式:www.xxx.xxx/xx/xx?xother=xxx)'

    elif int(apitype)==2:
        try:
            bids=app.BookIds()
            print bids
            if bids!=[]:
                bid=bids[0]
                updatesql='UPDATE ebook_con.con_mcp_api SET api_status=1, result_data=\'{"source_bid":%s}\' where mcp_id=%s and api_type=%s'%(bid,mcpid,apitype)
                imreaddb.insertdb(updatesql)
                return 0,'大官人,审核成功了!'
            else:
                return 302,'审核失败:图书列表接口内容获取为空，接口返回内容格式不标准!'
        except Exception, e:
            return 401,'接口格式或者接口数据类型选择有误!\n(接口格式:www.xxx.xxx/xx/xx?xother=xxx)'

    elif int(apitype)==3:###需要知道参数sbid
        try:
            ##获取sid内容
            selectsql='SELECT result_data from ebook_con.con_mcp_api where mcp_id=%s and api_type=2'%mcpid
            results=imreaddb.selectdb(selectsql)
            result_data=json.loads(results[0][0])
            sbid=result_data['source_bid']
            ###测试接口
            bookinfos=app.BookInfos(sbid,mcpid)
            if len(bookinfos.keys())>1:###如果接口获取失败则返回值是{'mcpid':mcpid}，故用次方法判读接口获取是否成功
                updatesql='UPDATE ebook_con.con_mcp_api SET api_status=1 where mcp_id=%s and api_type=%s'%(mcpid,apitype)
                imreaddb.insertdb(updatesql)
                return 0,'大官人,审核成功了!'
            else:
                return 303,'图书信息接口内容获取为空，接口返回内容格式不标准!'
        except Exception, e:
            return 401,'接口格式或者接口数据类型选择有误!\n(接口格式:www.xxx.xxx/xx/xx?xbid=%s&xother=xxx)'

    elif int(apitype)==4:###需要知道参数sbid
        try:    
            ##获取sid内容
            selectsql='SELECT result_data from ebook_con.con_mcp_api where mcp_id=%s and api_type=2'%mcpid
            results=imreaddb.selectdb(selectsql)
            result_data=json.loads(results[0][0])
            sbid=result_data['source_bid']
            ###测试接口
            cidsinfos=app.BookChaptersinfos(sbid)
            if cidsinfos!=[]:
                cid=cidsinfos[0]['chapter_id']
                updatesql='UPDATE ebook_con.con_mcp_api SET api_status=1, result_data=\'{"source_bid":%s,"chapter_id":%s}\' where mcp_id=%s and api_type=%s'%(sbid,cid,mcpid,apitype)
                imreaddb.insertdb(updatesql)
                return 0,'大官人,审核成功了!'
            else:
                return 304,'章节信息接口内容获取为空，接口返回内容格式不标准!'
        except Exception, e:
            return 401,'接口格式或者接口数据类型选择有误!\n(接口格式:www.xxx.xxx/xx/xx?xbid=%s&xother=xxx)'
   
    elif int(apitype)==5:###需要知道参数sbid和cid
        try:
            ###获取含有bid,cid的result_data内容
            selectsql='SELECT result_data from ebook_con.con_mcp_api where mcp_id=%s and api_type=4'%mcpid
            results=imreaddb.selectdb(selectsql)
            ###string转json

            result_data=json.loads(results[0][0])
            wordsize=app.BookChapterCont(result_data)
            if wordsize!=0:
                updatesql='UPDATE ebook_con.con_mcp_api SET api_status=1 where mcp_id=%s and api_type=%s'%(mcpid,apitype)
                imreaddb.insertdb(updatesql)
                return 0,'大官人,审核成功了!'
            else:
                return 305,'章节内容接口内容获取为空，接口返回内容格式不标准!'
        except Exception, e:
            return 401,'接口格式或者接口数据类型选择有误!\n(接口格式:www.xxx.xxx/xx/xx?xbid=%s&xcid=%s&xother=xxx)'


if __name__ == '__main__':
    try:
        mcpid=sys.argv[1]
        conttype=sys.argv[2]
        apitype=sys.argv[3]
        result=testAPI(mcpid,conttype,apitype)
        print json.dumps({"error_code":result[0],"msg":result[1]})
    except Exception, e:
        print json.dumps({"error_code":101,"msg":"脚本有误,请及时联系平台提供方!"})
    








