# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml


parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()

def NewbookOne(categoryid):
    #新书1分读
    girl_url='http://wap.cmread.com/r/p/nsmianfei.jsp?'
    girl_xs1fd_infos={'tagname':'a','taglocationmark':{'class':"bookcon"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394150808')}
    girl_xs1fd_1bids=parsexml.XMLBs4(girl_url,girl_xs1fd_infos)
    girl_xs1fd_infos={'tagname':'a','taglocationmark':{'class':"lineOne"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394150808')}
    girl_xs1fd_2bids=parsexml.XMLBs4(girl_url,girl_xs1fd_infos)
    girl_xs1fd_bids=girl_xs1fd_1bids+girl_xs1fd_2bids
    # print girl_xs1fd_bids
    autorenewbooks.RenewCategoryBooks(girl_xs1fd_bids,categoryid)

def EndbookTwo(categoryid):
    #完本2折区
    girl_url='http://wap.cmread.com/r/p/nsmianfei.jsp?'
    girl_wb2zq_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394150810')}
    girl_wb2zq_bids=parsexml.XMLBs4(girl_url,girl_wb2zq_infos)
    autorenewbooks.RenewCategoryBooks(girl_wb2zq_bids,categoryid)

def NightFree(categoryid):
    #夜场免费
    girl_url='http://wap.cmread.com/r/p/nsmianfei.jsp?'
    girl_ycmf_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394150809')}
    girl_ycmf_bids=parsexml.XMLBs4(girl_url,girl_ycmf_infos)
    autorenewbooks.RenewCategoryBooks(girl_ycmf_bids,categoryid)

def GirlPreferred(categoryid):
    #女生优选
    girl_url='http://wap.cmread.com/r/p/nsindex.jsp?'
    girl_yxtj_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=398778581')}
    girl_yxtj_bids=parsexml.XMLBs4(girl_url,girl_yxtj_infos)
    autorenewbooks.RenewCategoryBooks(girl_yxtj_bids,categoryid)

def EditorRecommends(categoryid):
    #小编力荐
    girl_url='http://wap.cmread.com/r/p/nsyc.jsp?'
    girl_ysyc_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid')}
    girl_ysyc_bids=parsexml.XMLBs4(girl_url,girl_ysyc_infos)
    autorenewbooks.RenewCategoryBooks(girl_ysyc_bids,categoryid)

def NewBookFirst(categoryid):
    #新书抢先
    girl_url='http://wap.cmread.com/r/p/nsxs.jsp?'
    girl_xsqx_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=408992008')}
    girl_xsqx_bids=parsexml.XMLBs4(girl_url,girl_xsqx_infos)
    autorenewbooks.RenewCategoryBooks(girl_xsqx_bids,categoryid)

def ClassificationNodes():
    #图书分类节点
    classificationinfos=[(6893664,138),(378533409,135),(6897898,134),(379699410,136),(402544862,137),(402219785,139)]
    for classificationinfo in classificationinfos:
        nid=classificationinfo[0]
        categoryid=classificationinfo[1]
        girl_url = 'http://wap.cmread.com/r/l/n.jsp?nid='+str(nid)
        girl_classification_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm')}
        girl_classification_bids=parsexml.XMLBs4(girl_url,girl_classification_infos)
        autorenewbooks.RenewCategoryBooks(girl_classification_bids,categoryid)



if __name__ == '__main__':
    ClassificationNodes()