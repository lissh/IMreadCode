# -*- coding: utf-8 -*-
__author__ = 'lish'
import time,datetime
import urllib2,cookielib,socket
import urllib,random
import re,json,os
import sys,time
import requests,MySQLdb
import crawlLWS as lws
import dealLWSdb as lwsdb
from multiprocessing.dummy import Pool as ThreadPool
import sys
reload(sys)
sys.setdefaultencoding('utf8')
requests.packages.urllib3.disable_warnings()

base_url='http://s.haohuojun.com/'

def linkSQL(host,user,passwd,db):
    global cursor,conn
    conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
    cursor = conn.cursor()
    return conn




def checkGuideids(guideids):

    ssql=str(tuple(guideids)).replace(',)',')')
    sql="select guide_id from ec_con.con_guide where guide_id in "+str(ssql)

    n = cursor.execute(sql)
    checkguideids=[]
    for row in cursor.fetchall():
        checkguideid=str(row[0])
        # print checkguideid
    	checkguideids.append(checkguideid)
        # print checkguideid
        #获取旧的攻略信息
        check_sql='select guide_title,guide_brief,guide_short_title from ec_con.con_guide where guide_id ='+str(checkguideid)
        n = cursor.execute(check_sql)
        old_infos=list(cursor.fetchall()[0])
        # print old_infos,'???'
        guideinfos=lws.AnalyzeGuides(checkguideid,True)
        # print guideinfos,'????????????ß'
        #获取新的攻略信息并与旧信息对比
        #comments_count,guide_id,liked,likes_count,realcreated_at,share_msg,short_title,status,template,title,updated_at,guide_cover_url,guide_html_content
        if len(guideinfos)==2 and old_infos !=[]:
            new_infos=guideinfos[1]
            # print 'new_infos'
            new_checkinfos=[new_infos[9],new_infos[5],new_infos[6]]

            if old_infos!=new_checkinfos:
                #更新攻略信息
                new_checkinfos=new_checkinfos+[checkguideid]
                renew_sql='update ec_con.con_guide set guide_title="%s",guide_brief="%s",guide_short_title="%s",modify_time=now() where guide_id =%s ;' % tuple(new_checkinfos)
                # print renew_sql
                n = cursor.execute(renew_sql)
                conn.commit()
                #推送价格更新消息!
                os.system("./ec_message/message -t 2 --guide "+str(checkguideid))
            else:
                #更新攻略创建和修改时间
                realcreated_at=new_infos[4]
                renew_sql="update ec_con.con_guide set create_time=from_unixtime("+str(realcreated_at)+",'%Y-%m-%d %H:%i:%s'),modify_time=now() where guide_id ="+str(checkguideid)
                # print renew_sql
                n = cursor.execute(renew_sql)
                conn.commit()

    return checkguideids


def checkGoodsids(goodids):
    # print goodids
    ssql=str(tuple(goodids)).replace(',)',')')
    sql="select goods_id from ec_con.con_goods where goods_id in "+str(ssql)
    # print sql
    n = cursor.execute(sql)
    checkgoodsids=[]
    for row in cursor.fetchall():
        checkgoodsid=str(row[0])
        checkgoodsids.append(checkgoodsid)

        #获取已存在商品的旧价格
        check_sql='select goods_price from ec_con.con_goods where goods_id ='+str(checkgoodsid)
        n = cursor.execute(check_sql)
        oldprice=int(cursor.fetchall()[0][0])
        #获取已存在商品的新价格
        # print checkgoodsid
        goodsinfos=lws.AnalyzeGoods(checkgoodsid)
        # print goodsinfos
        newprice=int(float(goodsinfos[11])*100)
        #判断新旧价格是否一直，从而判断是否需要更新
        if newprice<oldprice:
            #更新价格
            renew_sql="update ec_con.con_goods set goods_price="+str(newprice)+" where goods_id ="+str(checkgoodsid)
            n = cursor.execute(renew_sql)
            conn.commit()
            #推送价格更新消息！
            os.system("./ec_message/message -t 1 --goods "+str(checkgoodsid)+" --price "+str(newprice)+" --oldPrice "+str(oldprice))
        elif newprice>oldprice:
            renew_sql="update ec_con.con_goods set goods_price="+str(newprice)+" where goods_id ="+str(checkgoodsid)
            n = cursor.execute(renew_sql)
            conn.commit()

    return checkgoodsids


class InsertCCC(object):

    def PopPage(self,category_id,content_type,content_ids):
        """
            改函数用于更新热门下的商品:
        """
        # 删除下线的记录
        dec_sql="delete from ec_con.con_category_content where category_id="+str(category_id)+' and content_type='+str(content_type)+' and status=0'
        n = cursor.execute(dec_sql)
        conn.commit()
        # 得到已经添加过了的的记录
        isExistCids_sql='select content_id from ec_con.con_category_content where category_id='+str(category_id)+' and content_type=1'
        n = cursor.execute(isExistCids_sql)
        isExistCids=[int(row[0]) for row in cursor.fetchall()]

        # 获取对应category_id和content_type下已经存在了的排序号category_location
        contents=[]
        gainRanks_sql='select DISTINCT category_location from ec_con.con_category_content where category_id='+str(category_id)+' and content_type='+str(content_type)
        n = cursor.execute(gainRanks_sql)
        locationRanks=[int(row[0]) for row in cursor.fetchall()]

        # 将插入的数据解析为以元祖为单位组成的列表
        for content_id in list(set(content_ids)):
            if int(content_id) not in isExistCids:
                locationI=0
                while locationI<10000:
                    locationI+=1
                    if locationI not in locationRanks:
                        content_id=str(int(content_id))
                        contents+=[tuple([category_id,content_id,content_type,locationI])]
                        locationRanks.append(locationI)
                        locationI=10000
        # 插入新的记录
        insert_sql="INSERT INTO ec_con.con_category_content (category_id,content_id,content_type,category_location,status) values (%s,%s,%s,%s,1) "
        n = cursor.executemany(insert_sql,contents)
        conn.commit()

    def ClassPage(self,categoryid,content_type,status=0,Ndays=1):
        """
        改函数用于更新专题下的攻略:
        categoryid:con_category中的category_id,同时也是对应着con_category_content中的con_category中的category_id的内容,这里的category_id代表的是某页面的区块位置;
        Ndays:表示更新N天前到当前时间的数据到对应的页面区块中;
        status:表示更新到con_category_content内容表中的数据的默认状态,1为上线，0为下线;
        """
        # Today=time.strftime('%Y%m%d',time.localtime())
        Today=datetime.date.today()
        NdaysAgo=Today - datetime.timedelta(days=Ndays)
        # print NdaysAgo
        if categoryid==102121244:
            locationI=0
            del_sql= 'delete from ec_con.con_category_content where category_id='+str(categoryid)+' and content_type='+str(content_type)
            n = cursor.execute(del_sql)
            conn.commit()
            Goodsids_sql="select guide_id from ec_con.con_guide where   create_time >"+str(NdaysAgo).replace('-','')+" order by create_time "
            n = cursor.execute(Goodsids_sql)

        elif categoryid==102121250:
            ###区块102121250，也就是发现里面的看看买什么模块
            CCClocations_sql='SELECT max(category_location) from ec_con.con_category_content where content_type='+str(content_type)
            n = cursor.execute(CCClocations_sql)
            locationI=int(cursor.fetchall()[0][0])

            TCCCids_sql="""
                            select topic_id from ec_con.con_topic a LEFT join
                            (SELECT * from ec_con.con_category_content where content_type=3)b on a.topic_id=b.content_id
                            where b.content_id is null and a.create_time >"""+str(NdaysAgo).replace('-','')
            n = cursor.execute(TCCCids_sql)

        CCCinfos=[]
        for row in cursor.fetchall():
            locationI+=1
            CCCinfos.append(tuple([categoryid,int(row[0]),content_type,locationI,status]))

        if CCCinfos!=[]:
            insert_sql="INSERT INTO ec_con.con_category_content (category_id,content_id,content_type,category_location,status) values (%s,%s,%s,%s,%s) "
            n = cursor.executemany(insert_sql,CCCinfos)
            conn.commit()

def crawlGoods(id):
    lws.AnalyzeGoods(id)


def main():

    lws.clearInfosFile()
    iccc=InsertCCC()
    goodsAllIds=[]



    #精选页面第三个模块的攻略
    Selection= lws.crawlSelectionGuides()
    selectionguidesblock3guideids=Selection.dealBlock3(1)
    #分类页面第一个模块的攻略
    Class=lws.crawlClassGuides()
    classguideblock1guideids=Class.dealBlock1(1)
    #分类页面第二个模块的攻略
    classguideblock2guideids=Class.dealBlock2(1)

    print selectionguidesblock3guideids,'?'
    print classguideblock1guideids,'??'
    print classguideblock2guideids,'???'

    guideAllIds=selectionguidesblock3guideids+classguideblock1guideids+classguideblock2guideids

    checkGuideAllIds=checkGuideids(guideAllIds)
    updateGuideAllIds=list(set(guideAllIds) - set(checkGuideAllIds))
    for updateGuideAllId in updateGuideAllIds:
            goodsAllIds+=lws.AnalyzeGuides(updateGuideAllId)
    #更新热门页面
    popularGoodsids=lws.crawlPopularGoodss(1)
    goodsAllIds=goodsAllIds+popularGoodsids

    print goodsAllIds
    goodsAllIds=list(set(goodsAllIds))
    if goodsAllIds!=[]:
        checkGoodsAllIds=checkGoodsids(goodsAllIds)
        updategoodsAllIds=list(set(goodsAllIds)-set(checkGoodsAllIds))
        for updategoodsAllId in updategoodsAllIds:
            lws.AnalyzeGoods(updategoodsAllId)
        # pool = ThreadPool(5)
        # results = pool.map(crawlGoods,updategoodsAllIds)
        # pool.close()
        # pool.join()

    # # 抓取的数据入库
    # lwsdb.main()
    # # 攻略生成并刷新cdn
    # lws.creatGuidesHtml(guideAllIds)
    # lws.release_cdn(base_url+'guides/html',0)
    # lws.release_cdn(base_url+'goods/html',0)
    # # 处理区块102121235:热门
    # iccc.PopPage(102121235,1,popularGoodsids)
    # # 处理区块102121250:发现-攻略
    # iccc.ClassPage(102121250,3,1)
    # # 处理区块102121244:发现-专题
    # iccc.ClassPage(102121244,2,1,7)


if __name__ == '__main__':
    # global conn,cursor
    # host="100.98.73.21"
    # user="commerce"
    # passwd="Vd9ZcDSoo8eHCAVfcUYQ"
    # conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db='ec_con')
    # cursor = conn.cursor()
    main()





