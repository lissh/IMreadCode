# -*- coding: utf-8 -*-
from array import array
__author__ = 'lish'

from igt_push import *
from igetui.template import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.template.igt_notypopload_template import *
from igetui.template.igt_apn_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *
from BatchImpl import *
from payload.APNPayload import *

# toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'true'
global HOST
# http的域名
HOST = 'http://sdk.open.api.igexin.com/apiex.htm';
#https的域名
# HOST = 'https://api.getui.com/apiex.htm';

APPKEY = "85V6jauSVtAK0iPVnSaek8"
APPID = "d91E1YPp2U9T20ucbfxls2"
MASTERSECRET = "wWHvQW3CGw5TnUHBeePFW9"
CID = "3756cf458ec09fc21075471728606d14"
Alias = '请输入别名'
DEVICETOKEN = "bb04dd31ed74ecaf0b64dd8401ed284fde6d24c96927879987db308be293de2e"


def pushAPN():

    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    message = IGtSingleMessage()

   # APN旧版推送Demo
#     template = APNTemplate()
#     template.setPushInfo("", -1,"", "", "", "", "", "")

# APN简单推送
    template = APNTemplate()
    apn = APNPayload();
    alertMsg = SimpleAlertMsg()
    alertMsg.alertMsg = ""
    apn.alertMsg = alertMsg
    apn.badge = 2
    apn.sound = ""
    apn.addCustomMsg("payload", "payload")
#     apn.contentAvailable=1
#     apn.category="ACTIONABLE"
    template.setApnInfo(apn)

# APN高级推送
#     template = APNTemplate()
#     apnpayload = APNPayload()
#     apnpayload.badge = 4
#     apnpayload.sound = "sound"
#     apnpayload.addCustomMsg("payload", "payload")
# #     apnpayload.contentAvailable = 1
# #     apnpayload.category = "ACTIONABLE"
#
#
#     alertMsg = DictionaryAlertMsg()
#     alertMsg.body = 'body'
#     alertMsg.actionLocKey = 'actionLockey'
#     alertMsg.locKey = 'lockey'
#     alertMsg.locArgs=['locArgs']
#     alertMsg.launchImage = 'launchImage'
#     # IOS8.2以上版本支持
# #     alertMsg.title = 'Title'
# #     alertMsg.titleLocArgs = ['TitleLocArg']
# #     alertMsg.titleLocKey = 'TitleLocKey'
#     apnpayload.alertMsg=alertMsg
#     template.setApnInfo(apnpayload)

    # 单个用户推送接口
    message.data = template
    # print DEVICETOKEN
    ret = push.pushAPNMessageToSingle(APPID, DEVICETOKEN, message)
    print message
    print ret

    # 多个用户推送接口
#     message = IGtListMessage()
#     message.data = template
#     contentId = push.getAPNContentId(APPID, message)
#     deviceTokenList = []
#     deviceTokenList.append(DEVICETOKEN)
#     ret = push.pushAPNMessageToList(APPID, contentId, deviceTokenList)
#     print ret

def pushMessageToSingle(TemplateType,NetWorkType=0):
    #http的接口
    # push = IGeTui(None, APPKEY, MASTERSECRET,False)
    #https的接口
    # push = IGeTui(None, APPKEY, MASTERSECRET,True)
    #根据HOST区分是https还是http
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板
    if TemplateType=='Notification':
        template = NotificationTemplateDemo()
    elif TemplateType=='Link':
        template = LinkTemplateDemo()
    elif TemplateType=='Transmission':
        template = TransmissionTemplateDemo()
    elif TemplateType=='NotyPopLoad':
        template = NotyPopLoadTemplateDemo()

    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = NetWorkType    #设置是否根据WIFI推送消息，2为4G/3G/2G,1为wifi推送，0为不限制推送

    target = Target()
    target.appId = APPID
    target.clientId = CID

    try:
        ret = push.pushMessageToSingle(message, target)
        print ret
    except RequestException, e:
        requstId = e.getRequestId()
        ret = push.pushMessageToSingle(message, target, requstId)
        print ret

def pushMessageToSingleBatch(TemplateType,NetWorkType=0):
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    batch = BatchImpl(APPKEY, push)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    if TemplateType=='Notification':
        template = NotificationTemplateDemo()
    elif TemplateType=='Link':
        template = LinkTemplateDemo()
    elif TemplateType=='Transmission':
        template = TransmissionTemplateDemo()
    elif TemplateType=='NotyPopLoad':
        template = NotyPopLoadTemplateDemo()

    message = IGtSingleMessage()
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.data = template
    message.pushNetWorkType = NetWorkType

    target = Target()
    target.appId = APPID
    target.clientId = CID

    batch.add(message, target)
    try:
        ret = batch.submit()
        print ret
    except Exception, e:
        ret=batch.retry()
        print ret


def pushMessageToList(TemplateType,NetWorkType=0):
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    if TemplateType=='Notification':
        template = NotificationTemplateDemo()
    elif TemplateType=='Link':
        template = LinkTemplateDemo()
    elif TemplateType=='Transmission':
        template = TransmissionTemplateDemo()
    elif TemplateType=='NotyPopLoad':
        template = NotyPopLoadTemplateDemo()

    message = IGtListMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.pushNetWorkType = NetWorkType

    target1 = Target()
    target1.appId = APPID
    target1.clientId = CID
    target1.alias = Alias
    arr = []

    arr.append(target1)
    contentId = push.getContentId(message, 'ToList_任务别名_可为空')
    ret = push.pushMessageToList(contentId, arr)
    print ret


def pushMessageToApp(TemplateType,phoneType=[],province=[],tag=[],NetWorkType=0):
    push = IGeTui(HOST, APPKEY, MASTERSECRET)

    # 消息模版：
    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板

    if TemplateType=='Notification':
        template = NotificationTemplateDemo()
    elif TemplateType=='Link':
        template = LinkTemplateDemo()
    elif TemplateType=='Transmission':
        template = TransmissionTemplateDemo()
    elif TemplateType=='NotyPopLoad':
        template = NotyPopLoadTemplateDemo()

    message = IGtAppMessage()
    message.data = template
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 12
    message.appIdList.extend([APPID])
    # phoneType=["ANDROID", "IOS"]
    # province=["浙江", "上海"]
    # tag=["开心"]
    if phoneType!=[]:
        message.phoneTypeList.extend(phoneType)
    if province!=[]:
        message.provinceList.extend(province)
    if tag!=[]:
        message.tagList.extend(tag)
    message.pushNetWorkType = NetWorkType
    message.setSpeed(1000)#设置腿上速度，单位为条、秒,仅支持对指定的应用群接口

    ret = push.pushMessageToApp(message, 'toApp_任务别名_可为空')
    # print message.getSpeed()
    print ret





# 通知透传模板动作内容
def NotificationTemplateDemo(DeviceType,begin="2015-03-04 17:40:22",end="2015-03-04 17:47:22",Content=u"请填入透传内容",title=u"请填入通知标题",text=u"请填入通知内容",logo="icon.png",logoURL=""):
    template = NotificationTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionType = 1 #收到消息是否立即启动应用：1为立即，2则广播等待客户端自启动
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    template.transmissionContent = Content#请填入透传内容
    template.title = title#请填入通知标题
    template.text = text#请填入通知内容
    template.logo = logo#icon.png
    template.logoURL = logoURL
    begin = begin#"2015-03-04 17:40:22";
    end = end#"2015-03-04 17:47:24";
    template.setDuration(begin, end)
    if DeviceType=='ios':
        # iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
        # template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
        template.setPushInfo("open",4,"message","","","","","");

    return template

# 通知链接模板动作内容
def LinkTemplateDemo():
    template = LinkTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.title = u"请填入通知标题"
    template.text = u"请填入通知内容"
    template.logo = ""
    template.url = "http://www.baidu.com"
    template.transmissionType = 1
    template.transmissionContent = ''
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True
    begin = "2015-03-04 17:40:22"
    end = "2015-03-04 17:47:24"
    template.setDuration(begin, end)
    if DeviceType=='ios':
        # iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
        # template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
        template.setPushInfo("open",4,"message","test1.wav","","","","");
    return template

# 透传模板动作内容
def TransmissionTemplateDemo():
    template = TransmissionTemplate()
    template.transmissionType = 1
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = '请填入透传内容'
    # iOS 推送需要的PushInfo字段 前三项必填，后四项可以填空字符串
    # template.setPushInfo(actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage)
#     template.setPushInfo("", 0, "", "com.gexin.ios.silence", "", "", "", "");

# APN简单推送
    alertMsg = SimpleAlertMsg()
    alertMsg.alertMsg = "thank you lish!!"
    apn = APNPayload();
    apn.alertMsg = alertMsg
    apn.badge = 2
#     apn.sound = ""
    apn.addCustomMsg("payload", "payload")
#     apn.contentAvailable=1
#     apn.category="ACTIONABLE"
    template.setApnInfo(apn)

    # APN高级推送
#     apnpayload = APNPayload()
#     apnpayload.badge = 4
#     apnpayload.sound = "com.gexin.ios.silence"
#     apnpayload.addCustomMsg("payload", "payload")
# #     apnpayload.contentAvailable = 1
# #     apnpayload.category = "ACTIONABLE"
#     alertMsg = DictionaryAlertMsg()
#     alertMsg.body = 'body'
#     alertMsg.actionLocKey = 'actionLockey'
#     alertMsg.locKey = 'lockey'
#     alertMsg.locArgs=['locArgs']
#     alertMsg.launchImage = 'launchImage'
#     # IOS8.2以上版本支持
# #     alertMsg.title = 'Title'
# #     alertMsg.titleLocArgs = ['TitleLocArg']
# #     alertMsg.titleLocKey = 'TitleLocKey'
#     apnpayload.alertMsg=alertMsg
#     template.setApnInfo(apnpayload)


    return template

# 通知弹框下载模板动作内容
def NotyPopLoadTemplateDemo():
    template = NotyPopLoadTemplate()
    template.appId = APPID
    template.appKey = APPKEY
    template.notyIcon = "icon.png"
    template.logoUrl = ""
    template.notyTitle = u"通知弹框下载功能标题"
    template.notyContent = u"通知弹框下载功能内容"
    template.isRing = True
    template.isVibrate = True
    template.isClearable = True

    template.popTitle = u"弹框标题"
    template.popContent = u"弹框内容"
    template.popImage = ""
    template.popButton1 = u"下载"
    template.popButton2 = u"取消"

    template.loadIcon = "file://icon.png"
    template.loadTitle = u"下载内容"
    template.loadUrl = "http://gdown.baidu.com/data/wisegame/c95836e06c224f51/weixinxinqing_5.apk"
    template.isAutoInstall = True
    template.isActive = False
    begin = "2015-03-04 17:40:22"
    end = "2015-03-04 17:47:24"
    template.setDuration(begin, end)
    return template

# 获取用户状态
def getUserStatus():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    print push.getClientIdStatus(APPID, CID)

# 任务停止功能
def stopTask():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    print push.stop("OSA-1126_ZbmWXkP56S7UsLG9NRLSA9");

# 根据ClientID设置标签功能
def setTag():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    tagList = ['标签1', '标签2', '......']
    print push.setClientTag(APPID, CID, tagList);

# 根据taskId返回推送结果
def getPushResultTest():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    #返回根据任务tasdkId返回数据
#     print push.getPushResult("OSA-0304_LUNiKF8n6i8PXgvqARRUp8")
    #返回用户推送结果信息
#     print push.queryAppPushDataByDate(APPID, "20150525")
    #返回用户注册结果信息
    print push.queryAppUserDataByDate(APPID,"20160706")


# 根据ClientID查询标签
def getUserTagsTest():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    dictz = push.getUserTags(APPID, CID)
    for key in dictz:
	print key + ":" + dictz[key].decode("utf-8")

    #
    # 服务端支持三个接口推送
    # 1.PushMessageToSingle接口：支持对单个用户进行推送
    # 2.PushMessageToList接口：支持对多个用户进行推送，建议为50个用户
    # 3.pushMessageToApp接口：对单个应用下的所有用户进行推送，可根据省份，标签，机型过滤推送
    #
def queryAppPushDataByDate(querydate):
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.queryAppPushDataByDate(APPID,str(querydate))
    print(res)

def queryAppUserDataByDate(querydate):
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.queryAppUserDataByDate(APPID,str(querydate))
    print(res)

def getPersonaTagsDemo():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    res = push.getPersonaTags(APPID)
    print(json.dumps(res).decode("unicode_escape").encode("utf-8"))
    for result in res["tags"]:
        print(result["desc"])

if __name__ == '__main__':

    #获得某日推送的情况
    # queryAppPushDataByDate(20160707)
    #获得某日新增用户情况
    # queryAppUserDataByDate(20160707)


    # 1.TransmissionTemplate:透传功能模板
    # 2.LinkTemplate:通知打开链接功能模板
    # 3.NotificationTemplate：通知透传功能模板
    # 4.NotyPopLoadTemplate：通知弹框下载功能模板
    pushMessageToSingle('Transmission')
    pushMessageToSingleBatch('Transmission')
    pushMessageToList('Transmission')
    pushMessageToApp('Transmission')


    # IOS简化版推送接口
    # pushAPN()

    # 获取用户状态接口
    # getUserStatus()

    # 任务停止功能接口
    # stopTask()

    # 通过服务端设置用户标签
    # setTag()

    # 根据TaskID返回任务推送结果功能
    # getPushResultTest()

    # 根据ClientID查询标签功能
    # getUserTagsTest()

    #获取appid可以操作的用户属性
    # getPersonaTagsDemo()
