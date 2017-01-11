# -*- coding: utf-8 -*-
__author__ = 'lish'
import sys,time
import MySQLdb,os
import sys
reload(sys)
sys.setdefaultencoding('gbk')

base_path='/opt/www/ec_con'




class updateTmpTable(object):
    def cleartmptable(self):
        #清空临时表tmp_con_goods和tmp_con_guide
        tr_tmp_goodsinfos_sql='TRUNCATE TABLE public_db.tmp_con_goods'
        tr_tmp_goodsbanners_sql='TRUNCATE TABLE public_db.tmp_con_goods_banner'
        tr_tmp_guideinfos_sql='TRUNCATE TABLE public_db.tmp_con_guide'
        tr_tmp_guidecontents_sql='TRUNCATE TABLE public_db.tmp_con_guide_content'
        tr_tmp_topicinfos_sql='TRUNCATE TABLE public_db.tmp_con_topic'
        tr_tmp_topiccontents_sql='TRUNCATE TABLE public_db.tmp_con_topic_content'
        tr_tmp_iteminfos_sql='TRUNCATE TABLE public_db.tmp_con_item'
        tr_tmp_itemcontents_sql='TRUNCATE TABLE public_db.tmp_con_item_content'

        n = cursor.execute(tr_tmp_goodsinfos_sql)
        n = cursor.execute(tr_tmp_goodsbanners_sql)

        n = cursor.execute(tr_tmp_guideinfos_sql)
        n = cursor.execute(tr_tmp_guidecontents_sql)
        n = cursor.execute(tr_tmp_topicinfos_sql)
        n = cursor.execute(tr_tmp_topiccontents_sql)
        n = cursor.execute(tr_tmp_iteminfos_sql)
        n = cursor.execute(tr_tmp_itemcontents_sql)
    def updatetmptable(self):
        fguideinfos=open(base_path+'/guides/infos','r')
        infos_guide=fguideinfos.readlines()
        fguidecontents=open(base_path+'/guides/guidescontent','r')
        contents_guide=fguidecontents.readlines()


        fgoodsinfos=open(base_path+'/goods/infos','r')
        infos_goods=fgoodsinfos.readlines()
        fgoodsbannars=open(base_path+'/goods/bannarurl','r')
        urls_goodsbannars=fgoodsbannars.readlines()


        ftopicinfos=open(base_path+'/topics/infos','r')
        infos_topic=ftopicinfos.readlines()
        ftopiccontents=open(base_path+'/topics/topicscontent','r')
        contents_topic=ftopiccontents.readlines()


        fiteminfos=open(base_path+'/items/itemsinfos','r')
        infos_item=fiteminfos.readlines()
        fitemcontents=open(base_path+'/items/itemscontent','r')
        contents_item=fitemcontents.readlines()
        # print contents_item


        guideinfos=[]
        guidecontents=[]
        goodsinfos=[]
        goodsbannarsurls=[]

        topicinfos=[]
        topiccontents=[]

        iteminfos=[]
        itemcontents=[]



        i=0
        for guideinfo in infos_guide:
            guideinfos.append(tuple(guideinfo[0:-1].split('|')))
        for guidecontent in contents_guide:
            guidecontents.append(tuple(guidecontent[0:-1].split('|')))


        for goodsinfo in infos_goods:
            goodsinfos.append(tuple(goodsinfo[0:-1].split('|')))
            # print goodsinfo
        for goodsbannarsurl in urls_goodsbannars:
            goodsbannarsurls.append(tuple(goodsbannarsurl[0:-1].split('|')))

        for topicinfo in infos_topic:
            topicinfos.append(tuple(topicinfo[0:-1].split('|')))
        for topiccontent in contents_topic:
            topiccontents.append(tuple(topiccontent[0:-1].split('|')))

        for iteminfo in infos_item:
            iteminfos.append(tuple(iteminfo[0:-1].split('|')))
        for itemcontent in contents_item:
            itemcontents.append(tuple(itemcontent[0:-1].split('|')))

        goodsinfos_sql="""
                    INSERT INTO public_db.tmp_con_goods (
                                category_id,
                                comments_count,
                                cover_image_url,
                                created_at,
                                description,
                                favorited,
                                favorites_count,
                                id,
                                liked,
                                likes_count,
                                name,
                                price,
                                purchase_id,
                                purchase_status,
                                purchase_type,
                                purchase_url,
                                shares_count,
                                type,
                                subcategory_id,
                                updated_at

                                                    )
                    VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        # n = cursor.execute(insql,binfos)
                        # conn.commit()
        goodsbannarsurls_sql="""
                    INSERT INTO public_db.tmp_con_goods_banner (
                        goods_id,
                        banner_url
                    )
                    VALUES
                        (%s,%s)"""




        guideinfos_sql="""
                    INSERT INTO public_db.tmp_con_guide (
                        comments_count,
                        idd,
                        liked,
                        likes_count,
                        created_at,
                        share_msg,
                        short_title,
                        STATUS,
                        template,
                        title,
                        updated_at,
                        cover_url

                    )
                    VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        guidecontents_sql="""
                    INSERT INTO public_db.tmp_con_guide_content (
                        guide_id,
                        content_id,
                        rn
                    )
                    VALUES
                        (%s,%s,%s)"""


        topicinfos_sql="""
                    INSERT INTO public_db.tmp_con_topic (
                        topic_id,
                        topic_name,
                        posts_count,
                        subtitle,
                        status,
                        cover_image_url,
                        updated_at,
                        location_style
                    )
                    VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s)"""
        topiccontents_sql="""
                    INSERT INTO public_db.tmp_con_topic_content (
                        topic_id,
                        content_id,
                        content_location
                    )
                    VALUES
                        (%s,%s,%s)"""


        iteminfos_sql="""
                    INSERT INTO public_db.tmp_con_item (
                        group_id,
                        item_id,
                        item_name,
                        content_count,
                        item_status,
                        icon_url
                    )
                    VALUES
                        (%s,%s,%s,%s,%s,%s)"""
        itemcontents_sql="""
                    INSERT INTO public_db.tmp_con_item_content (
                        item_id,
                        content_id,
                        content_location
                    )
                    VALUES
                        (%s,%s,%s)"""
        # print list(set(goodsinfos))[0]

        n = cursor.executemany(goodsinfos_sql,list(set(goodsinfos)))
        conn.commit()
        n = cursor.executemany(goodsbannarsurls_sql,list(set(goodsbannarsurls)))
        conn.commit()
        n = cursor.executemany(guideinfos_sql,list(set(guideinfos)))
        conn.commit()
        n = cursor.executemany(guidecontents_sql,list(set(guidecontents)))
        conn.commit()

        n = cursor.executemany(topicinfos_sql,list(set(topicinfos)))
        conn.commit()
        n = cursor.executemany(topiccontents_sql,list(set(topiccontents)))
        conn.commit()


        n = cursor.executemany(iteminfos_sql,list(set(iteminfos)))
        conn.commit()
        n = cursor.executemany(itemcontents_sql,list(set(itemcontents)))
        conn.commit()

    def updatealltmptable(self):
        self.cleartmptable()
        self.updatetmptable()




class updateOfficeTable(object):


    def updateguide(self):
        guideinfos_sql="""
                            INSERT INTO ec_con.con_guide (
                                guide_id,
                                guide_status,
                                guide_title,
                                image_url,
                                guide_brief,
                                guide_short_title,
                                content_cnt,
                                initial_uv,
                                guide_path
                                #create_time
                            ) SELECT DISTINCT
                                aa.idd,
                                1,
                                aa.title,
                                aa.cover_url,
                                aa.share_msg,
                                aa.short_title,
                                aa.comments_count,
                                (200+ceil(rand()*300))initial_uv,
                                concat('http://s.haohuojun.com/guides/html/',aa.idd,'.html')
                                #from_unixtime(aa.max_timevalue,'%Y-%m-%d %H:%i:%s')
                            FROM
                                (
                                    SELECT DISTINCT
                                        a.*
                                        #case when a.updated_at> a.created_at then a.updated_at when a.created_at is null then '' else a.created_at end as max_timevalue
                                    FROM
                                        public_db.tmp_con_guide a
                                    LEFT JOIN ec_con.con_guide b ON a.idd = b.guide_id
                                    WHERE
                                        b.guide_id IS NULL
                                    GROUP BY a.idd
                                ) aa
                            """

        guidecontents_sql="""
                            INSERT INTO ec_con.con_guide_content (guide_id, content_id, rn)
                            SELECT DISTINCT
                                aa.guide_id,
                                aa.content_id,
                                aa.rn
                            FROM
                                (
                                    SELECT
                                        a.*
                                    FROM
                                        public_db.tmp_con_guide_content a
                                    LEFT JOIN ec_con.con_guide_content b ON a.guide_id = b.guide_id
                                    WHERE
                                        b.guide_id IS NULL
                                ) aa
                            """
        n = cursor.execute(guideinfos_sql)
        conn.commit()
        n = cursor.execute(guidecontents_sql)
        conn.commit()



    def updategoods(self):

        goodsinfos_sql="""
                            INSERT INTO ec_con.con_goods (
                                goods_id,
                                goods_name,
                                image_url,
                                image_style,
                                goods_brief,
                                goods_price,
                                goods_old_price,
                                source_gid,
                                source_id,
                                goods_status,
                                goods_type,
                                category_id,
                                initial_uv,
                                content_path
                            ) SELECT DISTINCT
                                aa.id,
                                aa.`name`,
                                aa.cover_image_url,
                                1,
                                aa.description,
                                aa.price * 100,
                                aa.price * 100,
                                aa.purchase_id,
                                aa.purchase_type,
                                1,
                                1,
                                aa.subcategory_id,
                                (200+ceil(rand()*300))initial_uv,
                                concat('http://s.haohuojun.com/goods/html/',aa.id,'.html')
                            FROM
                                (
                                    SELECT
                                        a.*
                                    FROM
                                        public_db.tmp_con_goods a
                                    LEFT JOIN ec_con.con_goods b ON a.id = b.goods_id
                                    WHERE
                                        b.goods_id IS NULL
                                    group by id
                                ) aa
                            """
        goodsbanners_sql="""
                            INSERT INTO ec_con.con_goods_banner(goods_id,banner_url)
                            SELECT
                            a.goods_id,
                            a.banner_url
                            FROM
                            public_db.tmp_con_goods_banner a
                            LEFT join
                            ec_con.con_goods_banner  b on a.banner_url=b.banner_url  where b.goods_id is NULL
                            """

        n = cursor.execute(goodsinfos_sql)
        conn.commit()
        n = cursor.execute(goodsbanners_sql)
        conn.commit()


    def updatetopic(self):

        topicinfos_sql="""
                            INSERT INTO ec_con.con_topic (
                                topic_name,
                                content_count,
                                image_url,
                                topic_desc,
                                topic_status,
                                image_style,
                                initial_uv,
                                source_tid,
                                source_type
                            ) SELECT DISTINCT
                                aa.topic_name,
                                aa.posts_count,
                                aa.cover_image_url,
                                aa.subtitle,
                                1,
                                aa.location_style,
                                CEILING(rand()*100) as initial_uv,
                                aa.topic_id,
                                1
                            FROM
                                (
                                    SELECT
                                        a.*
                                    FROM
                                        public_db.tmp_con_topic a
                                    LEFT JOIN ec_con.con_topic b ON a.topic_id = b.source_tid
                                    WHERE
                                        b.topic_id IS NULL
                                ) aa
                            GROUP BY
                                topic_id
                            """

        topiccontents_sql="""
                            INSERT INTO ec_con.con_topic_content (
                                topic_id,
                                content_id,
                                content_location
                            ) SELECT a.* FROM
                                    (
                                        SELECT
                                            a.topic_id,
                                            b.content_id,
                                            b.content_location
                                        FROM
                                            ec_con.con_topic a,
                                            public_db.tmp_con_topic_content b
                                        WHERE
                                            a.source_tid = b.topic_id
                                    ) a
                                LEFT JOIN ec_con.con_topic_content b ON a.content_id = b.content_id
                                WHERE
                                    b.content_id IS NULL
                             """
        n = cursor.execute(topicinfos_sql)
        conn.commit()
        n = cursor.execute(topiccontents_sql)
        conn.commit()




    def updateitems(self):
        #
        itemsids_sql='SELECT DISTINCT item_id from public_db.tmp_con_item_content'
        n = cursor.execute(itemsids_sql)
        itemsids=[int(row[0]) for row in cursor.fetchall()]
        itemscontents=[]
        for itemsid in itemsids:
            # print itemsid
            CCClocations_sql='SELECT category_location from ec_con.con_category_content where category_id='+str(itemsid)

            n = cursor.execute(CCClocations_sql)
            CCClocations=[int(row[0]) for row in cursor.fetchall()]
            ICCCids_sql="""
                                SELECT a.content_id from
                                (SELECT DISTINCT content_id from public_db.tmp_con_item_content where item_id="""+str(itemsid)+""")a
                                left join (
                                SELECT content_id from ec_con.con_category_content where category_id="""+str(itemsid)+""")b on a.content_id=b.content_id where b.content_id is null
                            """
            n = cursor.execute(ICCCids_sql)

            for row in cursor.fetchall():
                CCCI=0
                while CCCI<100000:
                    CCCI+=1
                    if CCCI not in CCClocations:
                        itemscontents+=[(itemsid,int(row[0]),CCCI)]
                        CCCI=100000
        if itemscontents!=[]:
            itemscontents_sql="INSERT INTO ec_con.con_category_content (category_id,content_id,content_type,category_location,status)VALUES(%s,%s,2,%s,1)"
            n = cursor.executemany(itemscontents_sql,itemscontents)
            conn.commit()


    def updateallofficetable(self):
        self.updateguide()
        self.updategoods()
        self.updatetopic()
        self.updateitems()


class clearLWSdb(object):
    """清理掉数据库中过期的礼物说商品，攻略和专题的信息表和关联表中的数据，我们这里认为商品等的存续期为三个月，及三个月以前产生的统统清理掉"""

    def removeServerDate(self,typename,gids):
        for gid in gids:
            rm_file_ord='rm -rf /opt/www/ec_con/'+str(typename)+'/'+str(gid)
            rm_document_ord='rm -rf /opt/www/ec_con/'+str(typename)+'/html/'+str(gid)+'.html'
            # print rm_file_ord,rm_document_ord
            os.system(rm_file_ord)
            os.system(rm_document_ord)



    def clearCGoods(self,ValidityDay):
        """清理数据表con_goods中的创建日期，清理该表及其相关表中的数据"""
        goodsids_sql="""
            SELECT a.goods_id from
            (select goods_id from ec_con.con_goods where  TIMESTAMPDIFF(day,create_time,NOW())>ValidityDay)a LEFT join
            (SELECT DISTINCT content_id from ec_con.con_guide_content)b on a.goods_id=b.content_id where b.content_id is null
            """
        n=cursor.execute(goodsids_sql.replace('ValidityDay',ValidityDay))
        goodsids=[int(row[0]) for row in cursor.fetchall()]
        if goodsids!=[]:
            addGoodssql=str(tuple(goodsids))
            deleteCGoods_sql='DELETE from ec_con.con_goods where goods_id in '+addGoodssql.replace(',)',')')
            n=cursor.execute(deleteCGoods_sql)
            conn.commit()
            self.removeServerDate('goods',goodsids)



    def clearCGuide(self,ValidityDay):
        """根据攻略表con_guide中的创建日期，清理该表及其相关表中的数据"""
        guideids_sql="""
                    #获得攻略ID
                    select guide_id from ec_con.con_guide where  TIMESTAMPDIFF(day,create_time,NOW())>ValidityDay;
                    """
        n=cursor.execute(guideids_sql.replace('ValidityDay',ValidityDay))
        guideids=[int(row[0]) for row in cursor.fetchall()]


        goodsids_sql="""
                    #获得已删除攻略中且不为未删除的攻略所用到的商品ID
                    select goods_id from ec_con.con_goods where goods_id in(
                    select b.content_id from ec_con.con_guide a,ec_con.con_guide_content b
                      where  TIMESTAMPDIFF(day,a.create_time,NOW())>ValidityDay
                      and a.guide_id=b.guide_id
                    group by b.content_id
                       having count(distinct b.content_id)=1);
        """
        n=cursor.execute(goodsids_sql.replace('ValidityDay',ValidityDay))
        goodsids=[int(row[0]) for row in cursor.fetchall()]


        #删除datebase和服务器上的数据,分别为：
        if goodsids!=[]:
            addGoodssql=str(tuple(goodsids))
            #删除con_goods_banner表中已删除商品
            deleteCGB_sql='DELETE from ec_con.con_goods_banner where goods_id in '+addGoodssql.replace(',)',')')
            # print deleteCGB_sql
            n=cursor.execute(deleteCGB_sql)
            conn.commit()
            #删除已删除攻略中且不为未删除的攻略所用到的商品
            deleteCGoods_sql='DELETE from ec_con.con_goods where goods_id in '+addGoodssql.replace(',)',')')
            n=cursor.execute(deleteCGoods_sql)
            conn.commit()
            self.removeServerDate('goods',goodsids)

        if guideids!=[]:
            addGuidesql=str(tuple(guideids))
            #删除con_guide_content中的内容
            deleteCGC_sql='DELETE FROM ec_con.con_guide_content where guide_id in '+addGuidesql.replace(',)',')')
            n=cursor.execute(deleteCGC_sql)
            conn.commit()
            #删除攻略
            deleteCGuide_sql='DELETE FROM ec_con.con_guide where guide_id in '+addGuidesql.replace(',)',')')
            n=cursor.execute(deleteCGuide_sql)
            conn.commit()
            self.removeServerDate("guide",guideids)


    def clearCCC(self):
        """清理数据表con_category_content"""
        #清理content_type=1,即内容为商品,该处清理的是已经不存在商品表中的商品
        contentids_sql="""
                    SELECT content_id from
                    (select DISTINCT content_id from ec_con.con_category_content where content_type=1) a LEFT join
                    (select goods_id from ec_con.con_goods)b on a.content_id=b.goods_id  where b.goods_id is null
                    """
        n=cursor.execute(contentids_sql)
        contentids=[int(row[0]) for row in cursor.fetchall()]
        if contentids!=[]:
            addCCCsql=str(tuple(contentids))
            #删除数据表con_category_content表中已经不存在的商品
            deleteCCC_sql='DELETE from ec_con.con_category_content where content_type=1 and content_id in '+addCCCsql.replace(',)',')')
            # print deleteCCC_sql
            n=cursor.execute(deleteCCC_sql)
            conn.commit()
        #清理content_type=2,即内容为攻略该，处清理的是已经不存在攻略表中的攻略
        contentids_sql="""
                    SELECT content_id from
                    (select DISTINCT content_id from ec_con.con_category_content where content_type=2) a LEFT join
                    (select guide_id from ec_con.con_guide)b on a.content_id=b.guide_id  where b.guide_id is null
                    """
        n=cursor.execute(contentids_sql)
        contentids=[int(row[0]) for row in cursor.fetchall()]
        if contentids!=[]:
            addCCCsql=str(tuple(contentids))
            #删除数据表con_category_content表中已经不存在的攻略
            deleteCCC_sql='DELETE from ec_con.con_category_content where content_type=2 and content_id in '+addCCCsql.replace(',)',')')
            # print deleteCCC_sql
            n=cursor.execute(deleteCCC_sql)
            conn.commit()



    def clearDB(self):
        self.clearCGuide('90')
        self.clearCGoods('90')
        self.clearCCC()

def main():
    try:
        global cursor,conn
        host="100.98.73.21"
        user="commerce"
        passwd="Vd9ZcDSoo8eHCAVfcUYQ"
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db='public_db')
        cursor = conn.cursor()

        tmptable=updateTmpTable()

        tmptable.updatealltmptable()

        officetable=updateOfficeTable()

        officetable.updateallofficetable()

        cleardb=clearLWSdb()
        cleardb.clearDB()


    except Exception, e:
        raise e

if __name__ == '__main__':
    main()

