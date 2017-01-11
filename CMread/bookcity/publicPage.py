# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml



parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()



def TodayLimitedFree(categoryid):
    #今日限免
    public_url='http://wap.cmread.com/r/p/cbmfx.jsp?'
    public_jrxm_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=396853031')}
    public_jrxm_bids=parsexml.XMLBs4(public_url,public_jrxm_infos)
    autorenewbooks.RenewCategoryBooks(public_jrxm_bids,categoryid)

def HeavyHotread(categoryid):
    #重磅热读

    #对应web版咪咕阅读出版页面-重磅热读和分类精选节点下内容
    # public_url = 'http://wap.cmread.com/r/p/pwindex.jsp?'
    # public_zbtj_infos={'tagname':'a','taglocationmark':{'class':"bookBox"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=376215778')}
    # public_fljx_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=382733157')}
    # public_zbtj_bids=parsexml.XMLBs4(public_url,public_zbtj_infos)
    # public_fljx_bids=parsexml.XMLBs4(public_url,public_fljx_infos)
    # public_zbrd_bids=public_zbtj_bids+public_fljx_bids

    #对应客户端咪咕阅读出版页面-重磅热读和分类精选节点下内容
    public_zbtj_bids=[]
    for page in range(1,13):
        public_url = 'http://wap.cmread.com/rbc/p/zbxs.jsp?page=%d&onlyRender=383771'%page
        public_zbtj_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
        public_zbtj_bids+=parsexml.XMLBs4(public_url,public_zbtj_infos)

    autorenewbooks.RenewCategoryBooks(public_zbtj_bids,categoryid)


def NewBookFirst(categoryid):
    #新书抢先
    public_url = 'http://wap.cmread.com/r/p/hbxs.jsp?'
    public_hbxs_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=398177621')}
    public_hbxs_bids=parsexml.XMLBs4(public_url,public_hbxs_infos)
    autorenewbooks.RenewCategoryBooks(public_hbxs_bids,categoryid)


def ClassificationNodes():
    #图书分类节点
    classificationinfos=[(6893918,145),(6893820,146),(6894104,147),(6898223,143),(6894055,148),(6897851,144),(359142922,149),(399378038,150),(6898174,151)]
    for classificationinfo in classificationinfos:
        nid=classificationinfo[0]
        categoryid=classificationinfo[1]
        public_url = 'http://wap.cmread.com/r/l/n.jsp?nid='+str(nid)
        public_classification_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm')}
        public_classification_bids=parsexml.XMLBs4(public_url,public_classification_infos)

        #去掉文学小说页面诗集部分的书籍数据
        if categoryid==143:
            delete_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=392538300')}
            delete_bids=parsexml.XMLBs4(public_url,delete_infos)
            public_classification_bids=list(set(public_classification_bids)-set(delete_bids))


        autorenewbooks.RenewCategoryBooks(public_classification_bids,categoryid)

if __name__ == '__main__':
    ClassificationNodes()
