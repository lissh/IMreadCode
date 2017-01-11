__author__ = 'lish'
# -*- coding: utf-8 -*-
from igt_push import *
from igetui.template import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.template.igt_notypopload_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *
import os
#toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'false'

#采用"Python SDK 快速入门"， "第二步 获取访问凭证 "中获得的应用配置
APPKEY = "Mjv706pTKt5cTcjtqaToz8"
APPID = "JroCkPGgpF6LzFQqqoWlhA"
MASTERSECRET = "uIBtmad7RK706cy5MKdfp3"
CID1 = "e560b884d8d9bf5bc5a0f9da545a11f3"
CID2 = "e560b884d8d9bf5bc5a0f9da545a11f4"
#ALIAS1= ""
#ALIAS2= ""
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

def pushMessageToList():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 消息模版：
    # NotificationTemplate：通知透传功能模板
    template = TransmissionTemplateDemo()

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = 0

    target1 = Target()
    target1.appId = APPID
    target1.clientId = CID1
#   target1.alias = Alias1
    target2 = Target()
    target2.appId = APPID
    target2.clientId = CID2
#   target2.alias = Alias2
    arr = []

    arr.append(target1)
    arr.append(target2)
    contentId = push.getContentId(message, 'ToList_任务别名_可为空')
    ret = push.pushMessageToList(contentId, arr)
    print ret

# 通知透传模板动作内容
def TransmissionTemplateDemo():
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '请输入您要透传内容'
#   iOS setAPNInfo
#   apnpayload = APNPayload()
#   apnpayload.badge = 4
#   apnpayload.sound = "sound"
#   apnpayload.addCustomMsg("payload", "payload")
#   apnpayload.contentAvailable = 1
#   apnpayload.category = "ACTIONABLE"
#
#   alertMsg = DictionaryAlertMsg()
#   alertMsg.body = 'body'
#   alertMsg.actionLocKey = 'actionLockey'
#   alertMsg.locKey = 'lockey'
#   alertMsg.locArgs=['locArgs']
#   alertMsg.launchImage = 'launchImage'
#   IOS8.2以上版本支持
#   alertMsg.title = 'Title'
#   alertMsg.titleLocArgs = ['TitleLocArg']
#   alertMsg.titleLocKey = 'TitleLocKey'
#   apnpayload.alertMsg=alertMsg
#   template.setApnInfo(apnpayload)

    # 设置通知定时展示时间，结束时间与开始时间相差需大于6分钟，消息推送后，客户端将在指定时间差内展示消息（误差6分钟）
    #begin = "2015-03-04 17:40:22";
    #end = "2015-03-04 17:47:24";
    #template.setDuration(begin, end)
    return template
    print ret

pushMessageToList()