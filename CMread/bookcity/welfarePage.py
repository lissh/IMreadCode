# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml



parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()

def BoyFree(categoryid):
    #男生免费
    welfare_url='http://wap.cmread.com/r/p/zhycmf.jsp?'
    welfare_boy_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=409745462')}
    welfare_boy_bids=parsexml.XMLBs4(welfare_url,welfare_boy_infos)
    autorenewbooks.RenewCategoryBooks(welfare_boy_bids,categoryid)

def GirlFree(categoryid):
    #女生免费
    welfare_url='http://wap.cmread.com/r/p/zhnsmf.jsp?'
    welfare_girl_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=409745463')}
    welfare_girl_bids=parsexml.XMLBs4(welfare_url,welfare_girl_infos)
    autorenewbooks.RenewCategoryBooks(welfare_girl_bids,categoryid)

def TodayFree(categoryid):
    #今日免费

    welfare_yctoday_url='http://wap.cmread.com/r/p/ycmfpd.jsp'
    welfare_yctoday_infos={'tagname':'a','taglocationmark':{'class':"bookcon"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=393037626')}
    welfare_yctoday_bids=parsexml.XMLBs4(welfare_yctoday_url,welfare_yctoday_infos)

    welfare_todayxm_url='http://wap.cmread.com/r/p/cbmfx.jsp'
    welfare_todayxm_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=396853029')}
    welfare_todayxm_bids=parsexml.XMLBs4(welfare_todayxm_url,welfare_todayxm_infos)

    welfare_nstj_url='http://wap.cmread.com/r/p/nsmianfei.jsp'
    welfare_nstj_infos={'tagname':'a','taglocationmark':{'class':"bookcon"},'tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394150807')}
    welfare_nstj_bids=parsexml.XMLBs4(welfare_nstj_url,welfare_nstj_infos)

    welfare_mf_url='http://wap.cmread.com/r/p/mianfei.jsp'
    welfare_mf_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=401045271')}
    welfare_mf_bids=parsexml.XMLBs4(welfare_mf_url,welfare_mf_infos)

    welfare_today_bids=welfare_yctoday_bids+welfare_todayxm_bids+welfare_nstj_bids+welfare_mf_bids
    autorenewbooks.RenewCategoryBooks(welfare_today_bids,categoryid)

def PublishFree(categoryid):
    #出版免费
    welfare_publish_url='http://wap.cmread.com/r/p/mianfei.jsp'
    welfare_publish_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=369936346')}
    welfare_publish_bids=parsexml.XMLBs4(welfare_publish_url,welfare_publish_infos)
    print welfare_publish_bids
    autorenewbooks.RenewCategoryBooks(welfare_publish_bids,categoryid)

def OneWeekFree(categoryid):
    #一周免费
    welfare_yzmf_url='http://wap.cmread.com/r/p/mianfei.jsp'
    welfare_yzmf_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=394908098')}
    welfare_yzmf_bids=parsexml.XMLBs4(welfare_yzmf_url,welfare_yzmf_infos)
    # print welfare_yzmf_bids
    # autorenewbooks.RenewCategoryBooks(welfare_yzmf_bids,categoryid)


if __name__ == '__main__':
    OneWeekFree(278)

