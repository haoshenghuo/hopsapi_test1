# @Time    : 6/18/2020 9:07 AM
# @Author  : Yang Xiaobai
# @Email   : yangzhiyongtest@163.com
import json

import jsonpath

from utils.config_tool.request_header import RequestHeader
from utils.logger import Log
from utils.new_tools.common_tool import Common

logger = Log(logger='para_analysis').get_log()
class ParaAnalysis:
    def __init__(self):
        pass

    # 1、 将header中的token添加到header
    def tokenToHeader(self,responseValue,requestPara,envContentDic=None):
        requestPara=requestPara[7]
        logger.info(requestPara)
        # requestPara = json.dumps(requestPara,ensure_ascii=False)
        requestPara = json.loads(requestPara,encoding='utf-8')
        logger.info(requestPara["isTransmit"])
        header_tokenKey = requestPara["isTransmit"]["tokenName"]
        logger.info(header_tokenKey)
        if not isinstance(header_tokenKey,list):
            header_tokenKey = eval(header_tokenKey)
        listNum = Common().estimateList(header_tokenKey)
        if self.isAppRequest(isAppDic=requestPara):
            header_token = RequestHeader.APPHEADER
        else:
            header_token = RequestHeader.WEBHEADER
        if listNum ==1 and responseValue != None :
            for list_item in header_tokenKey:
                header_tokenValue = responseValue[list_item[1]]
                header_token[list_item[0]]=header_tokenValue
        elif listNum == 0 and responseValue != None:
            header_tokenValue = responseValue[header_tokenKey[1]]
            header_token[header_tokenKey[0]] = header_tokenValue
        return header_token

    # header处理选择
    def chooseHeader(self,caseList,responseValue=None):
        paraDic = caseList[7]
        paraDic = json.dumps(paraDic,ensure_ascii=False)
        tokenlist = jsonpath.jsonpath(paraDic,'$.isTransmit.tokenName')
        paraDic = json.loads(paraDic,encoding='utf-8')
        if tokenlist == '' and (paraDic['isApp'] == 'N' or paraDic['isApp'] == 'n'):
            return RequestHeader.WEBHEADER
        elif tokenlist == '' and (paraDic['isApp'] == 'Y' or paraDic['isApp'] == 'y'):
            return RequestHeader.APPHEADER
        elif tokenlist != '':
            headerdata=self.tokenToHeader(responseValue=responseValue, requestPara=caseList, envContentDic=None)
            return headerdata

    # 2、将需要传递的健值添加参数
    def paraToRequestData(self,requestPara,requestData,responseValue,envContentDic={}):
        # requestPara = requestPara[7]
        requestData = json.loads(requestData,encoding='utf-8')
        # requestData = json.loads(requestData,encoding='utf-8')
        requestPara = json.loads(requestPara,encoding='urt-8')
        logger.info(requestData)
        logger.info(requestPara)
        logger.info(type(requestPara))
        logger.info(type(requestData))
        transmitKey = requestPara["isTransmit"]["transmitName"]
        requestDataJson = requestData["paData"]["paramData"]
        listNum = Common().estimateList(transmitKey)
        if listNum ==1 and responseValue != None:
            for list_item in transmitKey:
                strKey = list_item[0]
                strValue=jsonpath.jsonpath(responseValue,list_item[1]["getValuePath"])[0]
                envContentDic["transmitDic"][strKey]=strValue
                requestDataJson=Common().replaceStr(requestDataJson, strKey, strValue)
        elif listNum == 0  and responseValue != None:
            strKey = transmitKey[0]
            logger.info(strKey)
            strValue = jsonpath.jsonpath(responseValue, transmitKey[1]["getValuePath"])[0]
            logger.info(strValue)
            envContentDic["transmitDic"][strKey] = strValue
            requestDataJson=Common().replaceStr(requestDataJson, strKey, strValue)
            logger.info(requestDataJson)
        return {"requestDataJson":requestDataJson,"envContentDic":envContentDic}

    # 获取参数
    def choosePara(self,caseList,responseValue=None):
        paraRequestDict = caseList[7]
        paraRequestJson = caseList[6]
        paraRequestDictTemp = json.dumps(paraRequestDict,ensure_ascii=False)
        # paraRequestJson = json.dumps(paraRequestJson,ensure_ascii=False)
        paraList = jsonpath.jsonpath(paraRequestDictTemp,'$.isTransmit.transmitName')
        logger.info(paraList)
        if paraList == '':
            return paraRequestJson["PaData"]["paramData"]
        else:
            return self.paraToRequestData(requestPara=paraRequestDict,requestData=paraRequestJson,responseValue=responseValue)


    # 3、 获取Python脚本
    def acquirePython(self):
        pass
    # 4、 上下文的处理
    def envContent(self):
        pass
    # 5、判断是否是APP
    #{"isApp":"False","isTransmit":{"tokenName":"tokenKey","transmitName":"transmitKey"}}
    def isAppRequest(self,isAppDic):
        if isAppDic["isApp"] == 'Y' or isAppDic["isApp"] == 'y':
            return True
        else:
            return False



if __name__ == '__main__':
    pass
