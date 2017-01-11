# -*- coding:utf-8 -*-
__author__ = 'lish'
import ParseXML as pxml



parsexml=pxml.ParseXML()
autorenewbooks=pxml.autoRenewBooks()
autorenewbooks.linkSQL()

def GirlsPopularity(categoryid):
    #女生人气榜
    ranking_nsrq_bids=[]
    ranking_nsrq_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    for page in range(1,10):
        ranking_url='http://wap.cmread.com/rbc/p/ns_phang.jsp?&page='+str(page)+'&vt=3&onlyRender=375943'
        rbids=parsexml.XMLBs4(ranking_url,ranking_nsrq_infos)
        if rbids !=[] and rbids[0] not in ranking_nsrq_bids:
            ranking_nsrq_bids+=rbids
        else:
            break
    autorenewbooks.RenewCategoryBooks(ranking_nsrq_bids,categoryid)


def BoysAttention(categoryid):
    #男生关注榜
    ranking_nsgz_bids=[]
    ranking_nsgz_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    for page in range(1,10):
        ranking_url='http://wap.cmread.com/rbc/p/yc_phang.jsp?&page='+str(page)+'&vt=3&onlyRender=380554'
        rbids=parsexml.XMLBs4(ranking_url,ranking_nsgz_infos)
        if rbids !=[] and rbids[0] not in ranking_nsgz_bids:
            ranking_nsgz_bids+=rbids
        else:
            break
    autorenewbooks.RenewCategoryBooks(ranking_nsgz_bids,categoryid)

def PublicationBoutique(categoryid):
    #出版精品榜
    ranking_cbjpb_bids=[]
    ranking_cbjpb_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    for page in range(1,10):
        ranking_url='http://wap.cmread.com/rbc/p/sort30.jsp?&page='+str(page)+'&vt=3&onlyRender=380549'
        rbids=parsexml.XMLBs4(ranking_url,ranking_cbjpb_infos)
        if rbids !=[] and rbids[0] not in ranking_cbjpb_bids:
            ranking_cbjpb_bids+=rbids
        else:
            break


    autorenewbooks.RenewCategoryBooks(ranking_cbjpb_bids,categoryid)

def FreeCoolReading(categoryid):
    #免费爽读榜
    ranking_mfsd_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    ranking_url='http://wap.cmread.com/rbc/p/mfbcs.jsp?ln=15958_399183__2_&t1=16825&cm=M8030001&vt=3'
    ranking_mfsd_bids=parsexml.XMLBs4(ranking_url,ranking_mfsd_infos)
    autorenewbooks.RenewCategoryBooks(ranking_mfsd_bids,categoryid)


def QiDianMonthly(categoryid):
    #起点月票榜
    ranking_qdyp_bids=[]
    ranking_qdyp_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    for page in range(1,10):
        ranking_url='http://wap.cmread.com/rbc/p/qdypb.jsp?&page='+str(page)+'&vt=3&onlyRender=380608'
        rbids=parsexml.XMLBs4(ranking_url,ranking_qdyp_infos)
        if rbids !=[] and rbids[0] not in ranking_qdyp_bids:
            ranking_qdyp_bids+=rbids
        else:
            break
    autorenewbooks.RenewCategoryBooks(ranking_qdyp_bids,categoryid)

def AmazonHot(categoryid):
    #亚马逊热销榜
    ranking_ymxrx_bids=[]
    ranking_ymxrx_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    for page in range(1,10):
        ranking_url='http://wap.cmread.com/rbc/p/qdypb.jsp?&page='+str(page)+'&vt=3&onlyRender=380714'
        rbids=parsexml.XMLBs4(ranking_url,ranking_ymxrx_infos)
        if rbids !=[] and rbids[0] not in ranking_ymxrx_bids:
            ranking_ymxrx_bids+=rbids
        else:
            break
    autorenewbooks.RenewCategoryBooks(ranking_ymxrx_bids,categoryid)

def AsianHot(categoryid):
    ranking_yzrs_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    ranking_ycrs_url='http://wap.cmread.com/rbc/p/wbrqrsb.jsp?&dataSrcId=85618673'  #亚洲好书榜-原创热书
    ranking_ycrs_bids=parsexml.XMLBs4(ranking_ycrs_url,ranking_yzrs_infos)

    ranking_nsrs_url='http://wap.cmread.com/rbc/p/wbrqrsbns.jsp?dataSrcId=85618673'  #亚洲好书榜-女生热书
    ranking_nsrs_bids=parsexml.XMLBs4(ranking_nsrs_url,ranking_yzrs_infos)

    ranking_cbrs_url='http://wap.cmread.com/rbc/p/wbrqrsbcb.jsp?dataSrcId=85618673'  #亚洲好书榜-出版热书
    ranking_cbrs_bids=parsexml.XMLBs4(ranking_cbrs_url,ranking_yzrs_infos)

    ranking_yzhs_bids=ranking_ycrs_bids+ranking_nsrs_bids+ranking_cbrs_bids
    autorenewbooks.RenewCategoryBooks(ranking_yzhs_bids,categoryid)



def AuthoritativeList(categoryid):
    ranking_qwb_infos={'tagname':'a','tagre':('href',r'/rbc/(\d+)/index\.htm')}
    ranking_boy_url='http://wap.cmread.com/rbc/p/npzh1410.jsp?dataSrcId=43684487'  #权威榜中榜-男生榜中榜-综合榜
    ranking_boy_bids=parsexml.XMLBs4(ranking_boy_url,ranking_qwb_infos)

    ranking_girl_url='http://wap.cmread.com/rbc/p/nszhbzb.jsp?dataSrcId=43684487'  #权威榜中榜-女生榜中榜-综合榜
    ranking_girl_bids=parsexml.XMLBs4(ranking_girl_url,ranking_qwb_infos)

    ranking_publish_url='http://wap.cmread.com/rbc/p/cbzhbzb.jsp?dataSrcId=43684487'  #权威榜中榜-出版榜中榜-综合榜
    ranking_publish_bids=parsexml.XMLBs4(ranking_publish_url,ranking_qwb_infos)

    ranking_qwb_bids=ranking_boy_bids+ranking_girl_bids+ranking_publish_bids
    autorenewbooks.RenewCategoryBooks(ranking_qwb_bids,categoryid)



if __name__ == '__main__':
    AmazonHot()
