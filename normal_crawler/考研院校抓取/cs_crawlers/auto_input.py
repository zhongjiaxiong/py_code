from selenium import webdriver
import xlrd
import xlwt
from threading import Thread
from selenium.webdriver.support.ui import Select
import parsel
import re
import requests
import time

def browser_init():
    options = webdriver.FirefoxOptions
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    return driver
def get_uni_name():      #从excel中得到大学的名称
    data = xlrd.open_workbook('cs_university.xls')
    table = data.sheet_by_index(0)
    nrows = table.nrows
    for i in range(nrows):
        school_name= table.cell(i, 0).value
        yield school_name
    print('*'*20+'开始获取'+school_name+'数据'+'*'*20)
    print('*' * 20 + '延时两秒'+'*'*20+'\n'*2)
    time.sleep(2)


def get_uni_url(driver,university_name):  #根据大学的名字获取研招网下该大学硕士招生网址
    try:

        driver.get('https://yz.chsi.com.cn/zsml/queryAction.do')
        s1 = Select(driver.find_element_by_css_selector('#mldm'))# 门类
        s1.select_by_value('zyxw')   #专业学位
        s2 = Select(driver.find_element_by_css_selector('#yjxkdm'))#专业领域
        s2.select_by_value('0854')   #电子信息
        s3 = Select(driver.find_element_by_css_selector('#xxfs'))#学习方式
        s3.select_by_value('1')    #全日制
        uni_input = driver.find_element_by_css_selector('#dwmc')#招生单位
        uni_input.send_keys(university_name)
        chaxun = driver.find_element_by_css_selector('[name=button]')#查询
        chaxun.click()
    except:
        print('自动输入出错')
        pass

    ###############################    页面跳转   ##############################

    driver.implicitly_wait(10)
    try:
        response = driver.page_source
    except:
        print('转跳失败')
        pass
    selector = parsel.Selector(response)
    url_text = selector.re('/zsml/querySchAction.do?.*?zymc=')[0]
    part_url = re.sub('&amp;','&',url_text)
    uni_url = 'https://yz.chsi.com.cn/' +part_url
    print('*' * 20 + '正在获取'+university_name+'数据' +'*'*20+'\n'*2)
    driver.close()
    return uni_url


def get_exam_urls(uni_url):  #得到各个研究方向的考试范围的网址

    time.sleep(2)
    headers = {
        "Cookie": " _ga=GA1.3.836403335.1579454875; zg_did=%7B%22did%22%3A%20%2216fbed8c999437-0b3834e9d4f35c-b363e65-144000-16fbed8c99a45b%22%7D; __utma=65168252.836403335.1579454875.1579455770.1579455770.1; __utmz=65168252.1579455770.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); acw_tc=2760829c15820907193288530e9be58a1725a3ec734830e1d1f86c002f575c; _gid=GA1.3.1894503399.1582431910; __utma=229973332.836403335.1579454875.1582441213.1582441213.1; __utmz=229973332.1582441213.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201582440456041%2C%22updated%22%3A%201582441237879%2C%22info%22%3A%201582440456045%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fyz.chsi.com.cn%2Fzsml%2FqueryAction.do%22%7D; aliyungf_tc=AQAAAGSGgAcJfwIADECHd6qO0ayfaC3x; CHSICC_CLIENTFLAGZSML=de3901ac561c306945606f900cc38fa4; TS01d9ac57=01886fbf6efb11f342a4746ca98a37662adc4fdc09645ac93fb56c3fc398a4ead65b2b0d4449218039091dee14bbc11ba560168a65733796b8fb5af567619f540c5b20e6e3",
        "Host": " yz.chsi.com.cn",
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
    }
    response = requests.get(uni_url,headers=headers)
    selector = parsel.Selector(response.text)
    exam_list=selector.xpath('//tbody/tr/td[last()-2]/a/@href').getall()
    exam_urls = []
    for exam in exam_list:
        exam_url = 'https://yz.chsi.com.cn'+exam
        exam_urls.append(exam_url)
        # yield exam_url
        print(exam_url)
    print('*' * 20 + '接收到考试范围网址' + '*' * 20+'\n'*2)
    return exam_urls


def get_infomation(exam_url): #输入考试范围地址，解析得到专业信息（字典）
    headers = {
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
    }
    try:
        response = requests.get(exam_url, headers=headers)
    except:
        print('获取网页失败')
        pass
    selector = parsel.Selector(response.text)
    exam_info = {}
    # 考试范围,包括政治，外语，业务课一，业务课二
    exam_info['院系所'] = selector.xpath('//tbody/tr[2]/td[2]/text()').get()
    exam_info['研究方向'] = selector.xpath('//tbody/tr[4]/td[2]/text()').get()
    exam_info['招生人数'] = selector.xpath('//tbody/tr[5]/td[2]/text()').get()
    exam_info['政治'] = selector.xpath('//tbody[@class="zsml-res-items"]/tr/td[1]/text()').get()
    exam_info['外语']= selector.xpath('//tbody[@class="zsml-res-items"]/tr/td[2]/text()').get()
    exam_info['业务课一']= selector.xpath('//tbody[@class="zsml-res-items"]/tr/td[3]/text()').get()
    exam_info['业务课二']= selector.xpath('//tbody[@class="zsml-res-items"]/tr/td[4]/text()').get()

    for lesson in exam_info:
        exam_info[lesson]=re.sub(r'\s+','',exam_info[lesson]) #去除包括换行符的所有空白

    return exam_info   #dict


def save_info(sheet,exam_num,exam_info,uni_name):
#将返回的字典数据保存 key作为第一行，value作为后面几行 exam_num表示一共有多少组该学校的数据
#填充数据
    print('正在保存'+uni_name+'第'+str(exam_num)+'数据'+'\n'*2)
    for i, k, v in zip(range(len(exam_info) + 1), exam_info.keys(), exam_info.values()):   #exam_info加一是为了给学校名留多一列
        sheet.write(0, 0, '学校\详情')
        sheet.write(exam_num, 0, uni_name)  #学校名
        sheet.write(0, i + 1, k)  # 写入表头
        sheet.write(exam_num, i + 1, v)




if __name__ == "__main__":
    driver = browser_init()
    university_name_gen= get_uni_name()
    exam_num_total = 0  # 表示招生院系数
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = workbook.add_sheet('university_info', cell_overwrite_ok=True)
    for university_name in university_name_gen:
        uni_url = get_uni_url(driver,university_name)
        exam_urls = get_exam_urls(uni_url)
        exam_num = len(exam_urls)
        # print(university_name,+'专业条目数：'+str(exam_num))
        for i,url in zip(range(exam_num_total, exam_num_total+exam_num+1), exam_urls):
            print('正在获取考试内容网址。。。。' + '\n' * 2)
            exam_info = get_infomation(url)
            print('*' * 20 + '解析考试范围网址成功' + '*' * 20 + '\n' * 2)
            save_info(sheet, i, exam_info, university_name)
        exam_num_total += len(exam_urls)
        print('保存'+university_name+'数据成功')
        workbook.save('uni_info.xls')



