#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'lish'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os,requests,re,random,time,json,urllib2,urllib

global data,headers
data=dict(
          uuid ='hjudwgohxzVu96krv/T6Hg==',
          body='{"dataVersion":"1470665563000"}',
          sign='046f91737a726a12d80b4d2ea57de350',
          d_model='iPhone8,1',
          st='1477986352998',
          clientVersion='5.4.1',
          screen='750*1334',
          osVersion='10.1',
          openudid='2465fa4afe47aa1758029dcb85c6a1ac6836071d',
          networkType='wifi',
          sv='120',
          d_brand='apple',
          client='apple',
          area='15_1213_3038_0',
          partner='apple',
          build='122445'
        )
headers={
         'Host': 'api.m.jd.com',
         'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
         'Proxy-Connection': 'close',
         'Cookie':'mba_muid=1470758417178-1f60ff58113eecbac6.126.1470819022878; mba_sid=126.10',
         'User-Agent': 'CMBCPersonBank/3.20 (iPhone; iOS 9.3.3; Scale/2.00) Paros/3.2.13',
         'Content-Length': '316',
          'Connection': 'close'}

def personPage():
        #信息页
        headers['Content-Length']='351'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{"flag":"nickname"}'
        data['sign']='8f5963a48a421fa4a21149e0132d45ba'
        data['st']=	'1470820443575'
        data['sv']=	'111'

        url='http://api.m.jd.com/client.action?functionId=newUserInfo'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        print cont


def seckillPage():
        #秒杀页面详情
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{}'
        data['sign']='17db5208237699fefd84ac159b73991f'
        data['st']=	'1470822528942'

        url='http://api.m.jd.com/client.action?functionId=miaoShaAreaList'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()

        screenedCommodities=[]
        jsoncont=json.loads(cont)
        for para in jsoncont['miaoShaList']:

                # canBuy=para['canBuy'] #是否可以购买
                # # tagText=para['tagText'] #前三的标签名
                # expid=para['expid']
                # sourceValue=para['sourceValue'] #
                # spuId=para['spuId'] #商品ID
                # clockNum=para['clockNum'] #设置闹钟提醒数
                # canFreeRead=para['canFreeRead'] #
                # rate=para['rate'] #折扣
                # cName=para['cName']
                # message=para['message']
                # miaoShaPrice=para['miaoShaPrice'] #秒杀价格
                # rid=para['rid']
                # promotionId=para['promotionId'] #促销ID
                # index=para['index']
                # wname=para['wname'] #商品名称
                # endRemainTime=para['endRemainTime'] #剩余时间
                # book=para['book']
                # resultSort=para['resultSort'] #排序方式
                # startTimeShow=para['startTimeShow'] #秒杀开始时间
                # good=para['good']
                # # colorRGB=para['colorRGB'] #前三的标签颜色
                # imageurl=para['imageurl'] #图片
                # miaoSha=para['miaoSha'] #是否为秒杀商品
                # discount=para['discount'] #活动差价
                # moreFunId=para['moreFunId'] #更多FunID
                # activeId=para['activeId'] #
                # adword=para['adword'] #广告语
                # # tagType=para['tagType'] #前三的标签类型：2-热卖，1-推荐，4-超值
                # wareId=para['wareId'] #加入购物车的ID
                # soldRate=para['soldRate'] #已售百分比
                # cid=para['cid']
                # startRemainTime=para['startRemainTime']
                # jdPrice=para['jdPrice'] #京东原价
                # promotion=para['promotion']
                # # print startTimeShow
                # print canBuy,expid,sourceValue,spuId,clockNum,canFreeRead,rate,cName,message,miaoShaPrice,rid,promotionId,index,wname,endRemainTime,book,resultSort,startTimeShow,good,imageurl,miaoSha,discount,moreFunId,activeId,adword,wareId,soldRate,cid,startRemainTime,jdPrice,promotion

            canBuy=para['canBuy'] #是否可以购买
            promotionId=para['promotionId'] #促销ID
            wname=para['wname'] #商品名称
            rate=para['rate'] #折扣
            miaoShaPrice=para['miaoShaPrice'] #秒杀价格
            discount=para['discount'] #活动差价
            jdPrice=para['jdPrice'] #京东原价
            wareId=para['wareId'] #加入购物车的ID
            # print canBuy,promotionId,spuId,wname,miaoShaPrice,rate,discount,jdPrice
            # print rate
            ratevalue=float(re.findall('(\d\.\d+.*?)',rate)[0])
            screenedCommodities.append(wareId)
            # if ratevalue<=5 or float(discount)>=500:
            #     screenedCommodities.append(wareId)
        # print screenedCommodities
        return screenedCommodities





def cartPage():
        #购物车


        headers['Content-Length']='527'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{"syntype":"1","specialId":"1","cartuuid":"hjudwgohxzVu96krv\/T6Hg==","noResponse":false,"openudid":"dd210bd5269d3a338b38c7d23dc4887381ee7a6f"}'
        data['sign']='ace5122375605eeeb9835cfc690ba4b7'
        data['st']=	'1470820457184'
        data['sv']=	'111'

        url='http://api.m.jd.com/client.action?functionId=cart'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        print cont






def addCart(commodityid):
        #加入购物车
        print commodityid
        headers['Content-Length']='634'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{"syntype":"1","operations":[{"TheSkus":[{"num":"1","Id":"'+str(commodityid)+'"}],"carttype":"2"}],"cartuuid":"hjudwgohxzVu96krv\/T6Hg==","noResponse":false,"openudid":"dd210bd5269d3a338b38c7d23dc4887381ee7a6f"}'
        data['sign']='a1c638cdba155b5b0127351321c9c5ed'
        data['st']=	'1470903659662'
        data['sv']=	'101'

        url='http://api.m.jd.com/client.action?functionId=cartAdd'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        print cont



def getAddress():
        #获取送货地址列表信息及ID
        headers['Content-Length']='324'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{}'
        data['sign']='657fe005add9a28d58adf54896ca3a81'
        data['st']=	'1470823493648'
        data['sv']=	'110'

        url='http://api.m.jd.com/client.action?functionId=getAddressByPin'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()




def currentOrder():
        #获取当前订单详情
        headers['Content-Length']='1631'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865'

        data['body']='{"CartStr":{"TheSkus":[{"num":"1","Id":"2339136"}]},"solidCard":false,"OrderStr":{"Mobile":"187****9865","IdTown":0,"IdCity":1213,"coord_type":2,"Id":137656425,"Name":"李诗恒","addressDefault":true,"longitude":1000,"ProvinceName":"浙江","Phone":"18758879865","IdProvince":15,"addressDetail":"长河街道秋溢路288号东冠高新科技园1号1406室","latitude":1000,"CityName":"杭州市","CountryName":"滨江区","TownName":"","IdArea":3038,"Where":"浙江杭州市滨江区长河街道秋溢路288号东冠高新科技园1号1406室"},"isInternational":false,"isYYS":false,"addressGlobal":true,"isLastOrder":true,"isSupportAllInvoice":true,"is170":"0","giftBuy":false}'
        data['sign']='ac5b02f47c38e6861d73f0fa629a7413'
        data['st']=	'1470823494191'


        url='http://api.m.jd.com/client.action?functionId=currentOrder'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()

def submitOrder():

        #提交订单
        headers['Content-Length']='3758'
        headers['Cookie']='pin=18758879865_p;wskey=AAFX2BBeAEDllwap1RskpG7UwgTuE_aMZSTs8hSAkM5dX6avZbr3uyyVn-Z0gKXmDoHh1rAUv_GxsovkEubt6VfAePLUoldL;whwswswws=18758879865; USER_FLAG_CHECK=107f0b74bebe901d2cdb74ec1aa7d215; abtest=20160913224806757_87; pt_key=app_openAAFYGAZQADCHWv-2XjRVf8FME6KlCWK7sgIXDWmiiDNQ3VL3SMbcjo2U4WwC1VGDFqEeNmZhGKU; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=566c7a931c1fa6189c451990010ac22w; mba_muid=1473777725425-2f6152e853b0fa4278.22.1477969498627; __tru=08966672-aaad-4e76-852b-1ba238a54c25; mt_subsite=%7C%7C125%252C1476971669; __tra=122270672.194380385.1476971669.1476971669.1476971669.1; __trv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1476971668991; __jdu=1983803933; __jda=97325571.1983803933.1473778344958.1475454671.1476971519620.19; mobilev=html5; shshshfpa=de1078cf-1d58-f3e8-df91-e7de5c67f124-1473986394; shshshfpb=1f1903ab808934882ab77f165a858de4500c43361069c28a957db3f5af; _jrda=1'

        data['body']='{"solidCard":false,"fk_traceIp":"192.168.1.118","CartStr":{"TheSkus":[{"num":"1","Id":"2339136"}]},"isInternational":false,"statisticsStr":{"TheSkus":[{"source_value":"","Id":"2339136","source_type":"shoppingCart_webSite"}]},"fk_longtitude":"120.196318","fk_latitude":"30.191670","giftBuy":false,"fk_appId":"com.360buy.jdmobile","hasSopSku":false,"isYYS":false,"fk_imei":"","totalPrice":"42.80","fk_macAddress":"","OrderStr":{"IdCity":1213,"IdInvoiceContentsType":3,"inputPasswordExplain":"请输入京东支付密码","Name":"李诗恒","IdInvoiceType":1,"IdInvoiceHeaderType":5,"IdTown":0,"canUseJdBeanCount":1000,"IdInvoicePutType":1,"PromotionPrice":59,"IdCompanyBranch":0,"Discount":22.2,"isShortPwd":false,"CompanyName":"北京聚能鼎力科技股份有限公司","IsUseBalance":false,"isIdCardVerifyRequired":false,"IdProvince":15,"totalJdBeanCount":1850,"param":{"isSupportAllInvoice":true,"solidCard":false,"isIousBuy":false,"refreshShipmentType":true,"supportJdBean":true,"isInternational":false,"isOpenPaymentPassword":false,"giftBuy":false,"needRemark":false,"isYYS":false,"immediatelyBuy":false,"isLastOrder":true,"judgeChangeBigItem":true,"isShortPwd":false},"CountryName":"滨江区","isUseJdBean":false,"MoneyBalance":0,"Price":59,"isSelectedFreeFright":0,"addressDetail":"长河街道秋溢路288号东冠高新科技园1号1406室","IsPutBookInvoice":false,"Mobile":"187****9865","InvoiceTitle":"åä½","addressDefault":true,"TownName":"","Phone":"187****9865","IdInvoiceContentTypeBook":-2,"IdArea":3038,"CurrentUsedJdBean":0,"Where":"浙江杭州市滨江区长河街道秋溢路288号东冠高新科技园1号1406室","useJdBeanCount":0,"UserLevel":0,"needRemark":false,"isSupportAllInvoice":true,"CityName":"杭州市","isChange":false,"Id":137656425,"ProvinceName":"浙江","isOpenPaymentPassword":true,"isLimitBuyVender":false},"fk_terminalType":"02"}'
        data['sign']='046f91737a726a12d80b4d2ea57de350'
        data['st']=	'1477986352998'

        data['sv']=	'120'
        data['usid']='ZSYYOWZ37HQEF6C4SRROPL2DDXDNXRSZW53TP6FFTCD5EZU5KBGQMGU4RW5J4TUO'

        url='http://api.m.jd.com/client.action?functionId=submitOrder'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        print cont


if __name__ == '__main__':
    submitOrder()
    # millis = int(round(time.time() * 1000))
    # print millis
    # commodityids=seckillPage()
    # for commodityid in commodityids[0:3]:
    #     addCart(commodityid)



