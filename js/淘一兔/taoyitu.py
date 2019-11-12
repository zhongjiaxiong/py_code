import requests
from lxml import etree
import execjs
import re
import json
url1 = 'http://www.taoyizhu.com'
url2 = 'http://www.taoyizhu.com/GetPlanToken'
url3 = 'http://www.taoyizhu.com/RateUserInfo'

headers = {
'Cookie': 'ASP.NET_SessionId=roqyttkmkhor4kosldlfdpnl; __RequestVerificationToken=onvCfK-nQQipsohCEUR1eC8wGmvfaDIaiBeKzABS224-n9elCPWhDUX259m7TxWaQ2YY-_aDv5q_Qe4K5BZETjvlpciUqioUDtGU7aPhinyjB1bVCeeAHtfbt3lBG8eST6NSZZ7Vcb0gECOIDD06Dg2; UM_distinctid=16e5a979694945-0760db250e1784-b363e65-144000-16e5a979695385; CNZZDATA1261631176=267018084-1573474813-null%7C1573474813; bdshare_firstime=1573477914696; TAOSHENGSHI_SHOPNAME=%E4%BD%A0%E5%A5%BD; TytKey=WU6APO/hqV8baequrqaVd6lGCDQ%3D%3DHPXXN',
'Host': 'www.taoyizhu.com',
'Origin': 'http://www.taoyizhu.com',
'Referer': 'http://www.taoyizhu.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

def get_js_function(js_path,func_name,func_args):
    '''
    :param js_path: js文件存放的路径
    :param func_name: 文件内的函数名
    :param func_args: 文件的参数
    :return: 函数执行后的结果
    '''
    with open(js_path,'r',encoding='utf-8')as f:
        js = f.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name,func_args)
def main():
    res1 = requests.get(url1, headers=headers).text
    html = etree.HTML(res1)
    __RequestVerificationToken = html.xpath('//input[@name="__RequestVerificationToken"]/@value')
    keyName = '你好'
    data1 = {
        '__RequestVerificationToken': __RequestVerificationToken[0],
        'keyName': keyName
    }

    res2 = requests.post(url2, data=data1, headers=headers).text
    jsondata1 = json.loads(res2)
    code, keyname = jsondata1['code'], jsondata1['keyName']
    data2 = {
        '__RequestVerificationToken': __RequestVerificationToken[0],
        'keyName': keyname
    }
    res3 = requests.post(url2,data=data2,headers=headers).text
    jsondata2 = json.loads(res3)
    code, keyname = jsondata2['code'], jsondata2['keyName']

    jiami = get_js_function('taoyitu.js', 'TaoyituAjax', keyName)
    data2 = {
        'nick': keyname,
        '__RequestVerificationToken': __RequestVerificationToken[0],
        'tokens': f'{code},{jiami}',
    }
    # print(data2)
    res4 = requests.post(url3,data=data2,headers=headers).text
    print(res4)


if __name__ == "__main__":
    main()



