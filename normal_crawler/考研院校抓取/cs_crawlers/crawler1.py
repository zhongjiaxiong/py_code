import requests
import parsel
import xlwt

headers = {
'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
'Referer': 'http://www.cdgdc.edu.cn/webrms/pages/Ranking/xkpmGXZJ2016.jsp',
'Cookie':'scrolls=300; JSESSIONID=35D8A1C40F981CF49B8F265057F67545; sto-id-20480-web_80=CBAKBAKMJABP; UM_distinctid=17048706dcf1e-01879567ff9ff9-313f69-1fa400-17048706dd043f; sto-id-20480-xww_webrms=CCAKBAKMEJBP; CNZZDATA2328862=cnzz_eid%3D1894230608-1581762577-%26ntime%3D1582168644'
}
url = 'http://www.cdgdc.edu.cn/webrms/pages/Ranking/xkpmGXZJ2016.jsp?yjxkdm=0812&xkdm=08'
response = requests.get(url,headers=headers)
# print(response.text)
selector = parsel.Selector(response.text)
universitys = selector.re('[\u4e00-\u9fa5]{2,7}大学', response.text)
workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = workbook.add_sheet('university', cell_overwrite_ok=True)

for i in range(10,len(universitys)):
    sheet.write(i-10+1,0,universitys[i])

workbook.save(r'cs_university.xls')


