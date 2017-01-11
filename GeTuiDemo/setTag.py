# -*- coding: utf-8 -*-
from array import array
__author__ = 'lish'

from igt_push import *

#采用"Python SDK 快速入门"， "第二步 获取访问凭证 "中获得的应用配置
APPKEY = "koOb7dOrV46y5XOHuH9pH9"
APPID = "Er1g7mLQUS6pToymO5bBK6"
MASTERSECRET = "JDQgdIzrapA0NShuqv2YZ8"
CID = "e32d5c3c4ad68e247ca34f525df3daf7" #e32d5c3c4ad68e247ca34f525df3daf7
# Alias = '请输入别名'
# DEVICETOKEN = "3c1403b148278e54a8e62e0b81e1fc5dec8de86c93db0285c4b40b34dfb04642"


# APPKEY = "85V6jauSVtAK0iPVnSaek8"
# APPID = "d91E1YPp2U9T20ucbfxls2"
# MASTERSECRET = "wWHvQW3CGw5TnUHBeePFW9"
# CID = "18ad7e0de83bd629343c7f92f7f861"
# Alias = '请输入别名'
# DEVICETOKEN = "bb04dd31ed74ecaf0b64dd8401ed284fde6d24c96927879987db308be293de2e"

HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

# 根据clientid设置标签功能
def setTag():
    print HOST,APPKEY,MASTERSECRET,APPID,CID
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    tagList = ['老婆','言情','黑色豪门']
    print push.setClientTag(APPID, CID, tagList);

# 根据clientid查询标签
def getUserTagsTest():
    push = IGeTui(HOST, APPKEY, MASTERSECRET)
    dictz = push.getUserTags(APPID, CID)
    for key in dictz:
        print key + ":" + dictz[key].decode("utf-8")

# # 根据clientid查询用户状态
# def getUserStatus():
#     push = IGeTui(HOST, APPKEY, MASTERSECRET)
#     print push.getClientIdStatus(APPID, CID)
#
# # 根据taskId返回推送结果
# def getPushResultTest():
#     push = IGeTui(HOST, APPKEY, MASTERSECRET)
#     #返回根据任务tasdkId返回数据
#     print push.getPushResult("OSA-0304_LUNiKF8n6i8PXgvqARRUp8")
# #   返回单日推送数据信息
# #   print push.queryAppPushDataByDate(APPID, "20150525")
# #   返回单日用户结果信息
# #   print push.queryAppUserDataByDate(APPID,"20150525")
#
#
# # 调用此接口可以获取某个应用单日的推送数据（推送数据包括：发送总数，在线发送数，接收数，展示数，点击数）（目前只支持查询1天前的数据
# def queryAppPushDataByDateDemo():
#     push = IGeTui(HOST, APPKEY, MASTERSECRET)
#     res = push.queryAppPushDataByDate(APPID,"20160818")
#     print(res)
#
# # 大数据综合分析用户得到的标签:即用户画像
# def getPersonaTagsDemo():
#     push = IGeTui(HOST, APPKEY, MASTERSECRET)
#     res = push.getPersonaTags(APPID)
#     print(json.dumps(res).decode("unicode_escape").encode("utf-8"))
#     for result in res["tags"]:
#         print(result["desc"])


if __name__ == '__main__':
    setTag()