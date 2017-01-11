# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml



parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()

def EveryoneIsWatching(categoryid):
    #大家都在看
    search_url='http://wap.cmread.com/r/p/custom.jsp?'
    search_srtj_infos={'tagname':'a','tagre':('href',r'/r/(\d+)/index\.htm.*?nid=')}
    search_srtj_bids=parsexml.XMLBs4(search_url,search_srtj_infos)
    # print search_srtj_bids
    autorenewbooks.RenewCategoryBooks(search_srtj_bids,categoryid)




if __name__ == '__main__':
    EveryoneIsWatching()