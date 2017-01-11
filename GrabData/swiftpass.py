#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author lish
# @time 2016-08-10

import sys,urllib2,cookielib,urllib,json,MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')


global cursor,conn
host="182.92.184.14"
user="cx_fujun"
passwd="fjfjie%mysql3"
db="ods"
conn=MySQLdb.connect(host=host,user=user,passwd=passwd,charset="utf8",db=db)
cursor = conn.cursor()


def Importdata(datas):
	#清空表
    tr_sql='TRUNCATE TABLE ods.pay_org_swiftpass_settle_d'
    n = cursor.execute(tr_sql)
    #导入最新数据
    sql="""
    INSERT INTO ods.pay_org_swiftpass_settle_d (
            pageSize,successCount,channelId,payRemitFee,thirdFee,refundCount,total,merchantId,checked,thirdCommissionFee,compareBeforeMoney,actSuccessFee,displayMerchantId,billRate,tradeRate,successFee,pageNumber,compareBeforeFee,payNetFee,costRate,mchFee,orgType,mchDealType,accOrg,payTradeTime,refundFee,payTypeId,average,mchRemitFee,payAccpetOrg,spss,apiCode,payCenterId,payTypeIdName,feeType
        )
        VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
    n = cursor.executemany(sql,datas)


def Grabdata(StartTime,EndTime):
        payStartTimeDate=str(StartTime)[0:4]+'-'+str(StartTime)[4:6]+'-'+str(StartTime)[6:8]
        payEndTimeDate=str(EndTime)[0:4]+'-'+str(EndTime)[4:6]+'-'+str(EndTime)[6:8]
        paradata={
        'loginOrgId':"6522900011",
        'payStartTimeDate':payStartTimeDate,
        'payEndTimeDate':payEndTimeDate,
        'feeType':"CNY",
        'page':"1",
        'rows':"10"
        }

        headers={
                'Host':"mch.swiftpass.cn",
                'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0",
                'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8",
                'Referer':"https://mch.swiftpass.cn/system/index",
                'Proxy-Connection': 'close',
                'Connection':"keep-alive"
                }

        #获取一个保存cookie的对象
        cj = cookielib.LWPCookieJar()
        #将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        loginUrl='http://mch.swiftpass.cn/login2'
        logindata={'userName':"6522900011",'password':"3cd9ea15ac799e943820ed9de1445af8",'randCode':""}
        loginreqs = urllib2.Request(loginUrl,urllib.urlencode(logindata), headers=headers)
        logincont = urllib2.urlopen(loginreqs).read()


        url='https://mch.swiftpass.cn/acc/checkBillMerchant/datagrid.json'
        reqs = urllib2.Request(url,urllib.urlencode(paradata),headers = headers)
        cont = urllib2.urlopen(reqs).read()
        # print cont
        jsoncont=json.loads(cont)
        records=[]
        for record in jsoncont['rows']:
            pageSize=record['pageSize']                        #页面显示记录条数
            successCount=record['successCount']                #
            channelId=record['channelId']                       #深圳市汇兆业投资发展有限公司WAP
            payRemitFee=record['payRemitFee']
            thirdFee=record['thirdFee']
            refundCount=record['refundCount']
            total=record['total']
            merchantId=record['merchantId']
            checked=record['checked']
            thirdCommissionFee=record['thirdCommissionFee']
            compareBeforeMoney=record['compareBeforeMoney']
            actSuccessFee=record['actSuccessFee']
            displayMerchantId=record['displayMerchantId']
            billRate=record['billRate']
            tradeRate=record['tradeRate']
            successFee=record['successFee']
            pageNumber=record['pageNumber']
            compareBeforeFee=record['compareBeforeFee']
            payNetFee=record['payNetFee']
            costRate=record['costRate']
            mchFee=record['mchFee']
            orgType=record['orgType']
            mchDealType=record['mchDealType']
            accOrg=record['accOrg']
            payTradeTime=record['payTradeTime']
            refundFee=record['refundFee']
            payTypeId=record['payTypeId']
            average=record['average']
            mchRemitFee=record['mchRemitFee']
            payAccpetOrg=record['payAccpetOrg']
            spss=record['spss']
            apiCode=record['apiCode']
            payCenterId=record['payCenterId']
            payTypeIdName=record['payTypeIdName']
            feeType=record['feeType']

            recordcont=tuple([pageSize,successCount,channelId,payRemitFee,thirdFee,refundCount,total,merchantId,checked,thirdCommissionFee,compareBeforeMoney,actSuccessFee,displayMerchantId,billRate,tradeRate,successFee,pageNumber,compareBeforeFee,payNetFee,costRate,mchFee,orgType,mchDealType,accOrg,payTradeTime,refundFee,payTypeId,average,mchRemitFee,payAccpetOrg,spss,apiCode,payCenterId,payTypeIdName,feeType])
            # print len(recordcont)
            records.append(recordcont)
            # print pageSize,successCount,channelId,payRemitFee,thirdFee,refundCount,total,merchantId,checked,thirdCommissionFee,compareBeforeMoney,actSuccessFee,displayMerchantId,billRate,tradeRate,successFee,pageNumber,compareBeforeFee,payNetFee,costRate,mchFee,orgType,mchDealType,accOrg,payTradeTime,refundFee,payTypeId,average,mchRemitFee,payAccpetOrg,spss,apiCode,payCenterId,payTypeIdName,feeType
        return records


def main():
    records=Grabdata(20160801,20160807)
    Importdata(records)



if __name__ == '__main__':

    main()



