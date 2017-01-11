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
          sign='f57fa6df1b82c776aac9e9b504d22dff',
          d_model='iPhone6,2',
          st='1470820442956',
          clientVersion='5.1.0',
          screen='640*1136',
          osVersion='9.3.4',
          openudid='dd210bd5269d3a338b38c7d23dc4887381ee7a6f',
          networkType='wifi',
          sv='110',
          d_brand='apple',
          client='apple'
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
        headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.126.1470819022878; mba_sid=126.10'

        data['body']='{"flag":"nickname"}'
        data['sign']='8f5963a48a421fa4a21149e0132d45ba'
        data['st']=	'1470820443575'
        data['area']=	'15_1213_3038_0'
        data['partner']=	'apple'
        data['sv']=	'111'
        data['build']=	'103689'

        url='http://api.m.jd.com/client.action?functionId=newUserInfo'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        print cont


def vote():





        #信息页
        headers['Content-Length']='351'
        headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.126.1470819022878; mba_sid=126.10'

        data['body']='{"flag":"nickname"}'
        data['sign']='8f5963a48a421fa4a21149e0132d45ba'
        data['st']=	'1470820443575'
        data['area']=	'15_1213_3038_0'
        data['partner']=	'apple'
        data['sv']=	'111'
        data['build']=	'103689'

        url='http://api.m.jd.com/client.action?functionId=newUserInfo'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()

        #购物车
        headers['Content-Length']='527'
        headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470820451923; mba_sid=127.2; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'

        data['body']='{"syntype":"1","specialId":"1","cartuuid":"hjudwgohxzVu96krv\/T6Hg==","noResponse":false,"openudid":"dd210bd5269d3a338b38c7d23dc4887381ee7a6f"}'
        data['sign']='ace5122375605eeeb9835cfc690ba4b7'
        data['st']=	'1470820457184'
        data['sv']=	'111'

        url='http://api.m.jd.com/client.action?functionId=cart'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()

        #秒杀页面详情
        headers['Content-Length']='324'
        headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470820451923; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'

        data['body']='{}'
        data['sign']='17db5208237699fefd84ac159b73991f'
        data['st']=	'1470822528942'
        data['sv']=	'110'

        url='http://api.m.jd.com/client.action?functionId=miaoShaAreaList'
        reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        cont = urllib2.urlopen(reqs).read()

        # #加入购物车
        # headers['Content-Length']='634'
        # headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470820451923; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'

        # data['body']='{"syntype":"1","operations":[{"TheSkus":[{"num":"1","Id":"2339136"}],"carttype":"2"}],"cartuuid":"hjudwgohxzVu96krv\/T6Hg==","noResponse":false,"openudid":"dd210bd5269d3a338b38c7d23dc4887381ee7a6f"}'
        # data['sign']='6c148ad0e619b890242025c6d4bfb06f'
        # data['st']=	'1470823178716'
        # data['sv']=	'101'
        #
        # url='http://api.m.jd.com/client.action?functionId=cartAdd'
        # reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        # cont = urllib2.urlopen(reqs).read()

        # #获取送货地址列表信息及ID
        # headers['Content-Length']='324'
        # headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470820451923; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'
        #
        # data['body']='{}'
        # data['sign']='657fe005add9a28d58adf54896ca3a81'
        # data['st']=	'1470823493648'
        # data['sv']=	'110'
        #
        # url='http://api.m.jd.com/client.action?functionId=getAddressByPin'
        # reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        # cont = urllib2.urlopen(reqs).read()
        #
        # #获取当前订单详情
        # headers['Content-Length']='1631'
        # headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470820451923; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'
        #
        # data['body']='{"CartStr":{"TheSkus":[{"num":"1","Id":"2339136"}]},"solidCard":false,"OrderStr":{"Mobile":"187****9865","IdTown":0,"IdCity":1213,"coord_type":2,"Id":137656425,"Name":"李诗恒","addressDefault":true,"longitude":1000,"ProvinceName":"浙江","Phone":"18758879865","IdProvince":15,"addressDetail":"长河街道秋溢路288号东冠高新科技园1号1406室","latitude":1000,"CityName":"杭州市","CountryName":"滨江区","TownName":"","IdArea":3038,"Where":"浙江杭州市滨江区长河街道秋溢路288号东冠高新科技园1号1406室"},"isInternational":false,"isYYS":false,"addressGlobal":true,"isLastOrder":true,"isSupportAllInvoice":true,"is170":"0","giftBuy":false}'
        # data['sign']='ac5b02f47c38e6861d73f0fa629a7413'
        # data['st']=	'1470823494191'
        #
        #
        # url='http://api.m.jd.com/client.action?functionId=currentOrder'
        # reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        # cont = urllib2.urlopen(reqs).read()

        #提交订单
        # headers['Content-Length']='3402'
        # headers['Cookie']='pin=18758879865_p;wskey=AAFXqZwZAEAdoyCb5wvKS7zliF7lGFi2qL6zaS7AYKFEtoeZZypFf4H6AM0_ZBJDCO8NmYpNaWtXCbT6MVqLm13gE3pL19jt;whwswswws=YGmQBNu%2FSoEz2NP%2BDMw0RnMkpaejkI8kRixb3D3CVJPZPOrhhSy5rA%3D%3D; mba_muid=1470758417178-1f60ff58113eecbac6.127.1470824511998; mba_sid=127.19; pt_key=app_openAAFXqvBgADBj5grGaD2MvJW1B_bOPjMxwCy3T4L7Q4hTkVuXo9M5NBYnUYySwfSHiy6p5BhsKpA; pt_pin=18758879865_p; pwdt_id=18758879865_p; sid=fc02e98da195845cbe8c198de1e0d3fw'
        #
        # data['body']='{"solidCard":false,"fk_traceIp":"192.168.1.118","CartStr":{"TheSkus":[{"num":"1","Id":"2339136"}]},"isInternational":false,"statisticsStr":{"TheSkus":[{"source_value":"","Id":"2339136","source_type":"shoppingCart_webSite"}]},"fk_longtitude":"120.196318","fk_latitude":"30.191670","giftBuy":false,"fk_appId":"com.360buy.jdmobile","hasSopSku":false,"isYYS":false,"fk_imei":"","totalPrice":"42.80","fk_macAddress":"","OrderStr":{"IdCity":1213,"IdInvoiceContentsType":3,"inputPasswordExplain":"请输入京东支付密码","Name":"李诗恒","IdInvoiceType":1,"IdInvoiceHeaderType":5,"IdTown":0,"canUseJdBeanCount":1000,"IdInvoicePutType":1,"PromotionPrice":59,"IdCompanyBranch":0,"Discount":22.2,"isShortPwd":false,"CompanyName":"北京聚能鼎力科技股份有限公司","IsUseBalance":false,"isIdCardVerifyRequired":false,"IdProvince":15,"totalJdBeanCount":1850,"param":{"isSupportAllInvoice":true,"solidCard":false,"isIousBuy":false,"refreshShipmentType":true,"supportJdBean":true,"isInternational":false,"isOpenPaymentPassword":false,"giftBuy":false,"needRemark":false,"isYYS":false,"immediatelyBuy":false,"isLastOrder":true,"judgeChangeBigItem":true,"isShortPwd":false},"CountryName":"滨江区","isUseJdBean":false,"MoneyBalance":0,"Price":59,"isSelectedFreeFright":0,"addressDetail":"长河街道秋溢路288号东冠高新科技园1号1406室","IsPutBookInvoice":false,"Mobile":"187****9865","InvoiceTitle":"åä½","addressDefault":true,"TownName":"","Phone":"187****9865","IdInvoiceContentTypeBook":-2,"IdArea":3038,"CurrentUsedJdBean":0,"Where":"浙江杭州市滨江区长河街道秋溢路288号东冠高新科技园1号1406室","useJdBeanCount":0,"UserLevel":0,"needRemark":false,"isSupportAllInvoice":true,"CityName":"杭州市","isChange":false,"Id":137656425,"ProvinceName":"浙江","isOpenPaymentPassword":true,"isLimitBuyVender":false},"fk_terminalType":"02"}'
        # data['sign']='b6c9775f83f98b43647156e6adde0bd5'
        # data['st']=	'1470825204684'
        # data['sv']=	'101'
        # data['usid']='ZSYYOWZ37HQEF6C4SRROPL2DDXDNXRSZW53TP6CBTZBVMCNHE7ZHLXQVP2MZZLC7'
        #
        # url='http://api.m.jd.com/client.action?functionId=submitOrder'
        # reqs = urllib2.Request(url,urllib.urlencode(data),headers = headers)
        # cont = urllib2.urlopen(reqs).read()

        print cont


if __name__ == '__main__':
    personPage()



