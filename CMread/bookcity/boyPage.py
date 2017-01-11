# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml



parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()

def TueWedFree(categoryid):
    #周一周二免费
    man_url='http://wap.cmread.com/r/p/ycmfpd.jsp?'
    man_wbFree_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=398645922')}
    man_wbFree_bids=parsexml.XMLBs4(man_url,man_wbFree_infos)
    autorenewbooks.RenewCategoryBooks(man_wbFree_bids,categoryid)

def JYFree(categoryid):
    #今夜免费
    man_url='http://wap.cmread.com/r/p/ycmfpd.jsp?'
    man_jyFree_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=403334882')}
    man_jyFree_bids=parsexml.XMLBs4(man_url,man_jyFree_infos)
    autorenewbooks.RenewCategoryBooks(man_jyFree_bids,categoryid)

def HeavyThisWeek(categoryid):
    #本周重磅
    man_url = 'http://wap.cmread.com/r/p/wwfxb.jsp?'
    man_wwfxb_infos={'tagname':'a','taglocationmark':{'class':"bookBox"},'tagre':('href',r'/r/(\d+)/index\.htm')}
    man_rdsj_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm')}

    man_bzzb_bids=parsexml.XMLBs4(man_url,man_wwfxb_infos)
    man_bzzb_bids=parsexml.XMLBs4(man_url,man_rdsj_infos)

    man_bzzb_bids=man_bzzb_bids+man_bzzb_bids
    autorenewbooks.RenewCategoryBooks(man_bzzb_bids,categoryid)

def MillionsUsersHotread(categoryid):
    #百万用户热读
    man_url = 'http://wap.cmread.com/r/p/yczzsw.jsp?'
    man_bwyhrd_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=365390256')}
    man_bwyhrd_bids=parsexml.XMLBs4(man_url,man_bwyhrd_infos)
    autorenewbooks.RenewCategoryBooks(man_bwyhrd_bids,categoryid)

def NewBookFirst(categoryid):
    #新书抢先
    man_url = 'http://wap.cmread.com/r/p/qxsd.jsp?'
    man_xsqx_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=399135643')}
    man_xsqx_bids=parsexml.XMLBs4(man_url,man_xsqx_infos)
    autorenewbooks.RenewCategoryBooks(man_xsqx_bids,categoryid)

def ClassificationNodes():
    #图书分类节点
    classificationinfos=[(358852585,124),(6888073,130),(6889867,125),(6891296,127),(6891829,126),(6891369,128),(409175157,129)]
    for classificationinfo in classificationinfos:
        nid=classificationinfo[0]
        categoryid=classificationinfo[1]
        man_url = 'http://wap.cmread.com/r/l/n.jsp?nid='+str(nid)
        man_classification_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm')}
        man_classification_bids=parsexml.XMLBs4(man_url,man_classification_infos)
        autorenewbooks.RenewCategoryBooks(man_classification_bids,categoryid)

if __name__ == '__main__':
    TueWedFree()




