# -*- coding: utf-8 -*-
import random
import re
import demjson
from https import Http
from selenium import webdriver

import requests
from bs4 import BeautifulSoup
from lxml import etree
# from setting import cookies
import time
import  urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from setting import UA

# chrome_options = webdriver.ChromeOptions()
# driver = webdriver.PhantomJS(executable_path='/Users/zhangfan/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs.exe')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.get('https://www.baidu.com/')
#
# htmlunit = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
# htmlunit.get("http://www.baidu.com")

# chrome_options.add_argument('--headless')
# # driver = webdriver.Chrome(chrome_options=chrome_options)
# driver=webdriver.Chrome(executable_path='/Users/zhangfan/Downloads\chromedriver.exe')
# driver.get("https://www.lagou.com/jobs/3301094.html")
# print driver.page_source.encode('gbk','ignore') #这个函数获取页面的html

# html = getHtml("https://www.lagou.com/jobs/3301094.html")
# # webbrowser.open_new("https://www.lagou.com/jobs/3301094.html")
#
# print (html)
# html1=requests.get("https://www.lagou.com/jobs/3301094.html")
# print (html1.text)
text=''

cookies = {

    'Cookie': 'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644;'
              'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
              'index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=7277bc08d137413dac2590cea0465e39; '
              'TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
              'PRE_UTM=; PRE_HOST=; '
              'PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; '
              'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3413383.html; _gat=1; _'
              'gid=GA1.2.807135798.1504227456; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504252636; _ga=GA1.2.1721572155.1504227456; '
              'LGSID=20170901153335-dd437749-8ee7-11e7-903c-5254005c3644; '
              'LGRID=20170901155728-336ca29d-8eeb-11e7-9043-5254005c3644'
    'login=true;'
}

class Parse:
    '''
    解析网页信息
    '''

    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        self.json = demjson.decode(htmlCode)
        print (self.json)
        pass

    def parseTool(self, content):
        '''
        清除html标签
        '''
        # if type(content) != str: return content
        sublist = ['<p.*?>', '</p.*?>', '<b.*?>', '</b.*?>', '<div.*?>', '</div.*?>',
                   '</br>', '<br />', '<ul>', '</ul>', '<li>', '</li>', '<strong>',
                   '</strong>', '<table.*?>', '<tr.*?>', '</tr>', '<td.*?>', '</td>',
                   '\r', '\n', '&.*?;', '&', '#.*?;', '<em>', '</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error ' + str(substring.pattern))
        return content

    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        totalCount = self.json['content']['positionResult']['totalCount']  # 职位总数量
        resultSize = self.json['content']['positionResult']['resultSize']  # 每一页显示的数量
        pageCount = int(totalCount) // int(resultSize) + 1  # 页面数量
        return pageCount

    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        for position in self.json['content']['positionResult']['result']:
            i = {}
            i['companyName'] = position['companyFullName']
            i['companyDistrict'] = position['district']
            i['companyLabel'] = str(position['companyLabelList']).decode('unicode_escape')
            i['companySize'] = position['companySize']
            i['companyStage'] = position['financeStage']
            i['companyType'] = position['industryField']
            i['positionType'] = position['firstType']
            i['positionEducation'] = position['education']
            i['positionAdvantage'] = position['positionAdvantage']
            i['positionSalary'] = position['salary']
            i['positionWorkYear'] = position['workYear']
            print (position['workYear'])
            detail_url = 'https://www.lagou.com/jobs/{}.html'.format(position['positionId'])
            # browser = webdriver.Chrome(chrome_options=chrome_options)
            # browser.get(detail_url)
            # detail_url = 'https://www.lagou.com/jobs/3301094.html'
            generalHttp = Http()
            headers = {

                # 'Host': 'm.lagou.com',
                # 'Connection':'keep-alive',
                # 'Cache-Control': 'max-age=0',
                # 'Upgrade-Insecure-Requests': '1',
                # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Mobile Safari/537.36',
                # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                # 'Accept-Encoding':'gzip, deflate, br',
                # 'Referer':' https://m.lagou.com/jobs/3301094.html',
                # 'Accept-Language': 'zh-CN,zh;q=0.9'
                'User-Agent': 'User-Agent:' +'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Mobile Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host':'m.lagou.com',
                'Origin':'https://www.lagou.com',
                'Connection':'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Referer':detail_url,
                'Cookie':'LGUID=20160307113016-e8fc3a30-e414-11e5-90de-5254005c3644; user_trace_token=20170308111932-0c2a85f0-03ae-11e7-9229-5254005c3644; index_location_city=%E4%B8%8A%E6%B5%B7; _ga=GA1.2.1722702168.1457321416; _putrc=2CB251DE30BF7A93; login=true; unick=%E5%BC%A0%E5%B8%86; X_HTTP_TOKEN=82911677e2861961ab4d41cd940478b8; JSESSIONID=ABAAABAAAGCABCCDCE9F1D42A965C126D61D19D3376453D; _ga=GA1.3.1722702168.1457321416; _gid=GA1.2.659545200.1520211741; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520233119,1520234795,1520234873,1520264108; LGSID=20180305233508-c8ea45b3-208a-11e8-9d5c-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xec674bc500018470%26issp%3D1%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26oq%3D%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%252520%2525E5%25258F%25258D%2525E7%252588%2525AC%2525E8%252599%2525AB%26rsv_t%3D2f23Tf5I7EVO%252FEOGA%252FRynbeyb5kUGGkEERMI2u0sEJvSbEb3RKp4J%252FAddwCHR4EPgE7Q%26inputT%3D3%26rsv_pq%3Ded66c7640001b3f4%26rsv_sug3%3D29%26rsv_sug1%3D28%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D281%26rsv_sug%3D2; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; gate_login_token=6703abccc36ef6afbff75031e5704c82dc15d8be42790e6a; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1520264178; LGRID=20180305233619-f30f19ff-208a-11e8-b126-5254005c3644'
            }
            response = requests.get(url=detail_url, headers=headers)
            response.encoding = 'utf-8'
            # tree = etree.HTML(response.text)
            # desc = tree.xpath('//*[@class="content"]/dd[2]/div/p/text()')
            soup = BeautifulSoup(response.text.decode('utf-8'),'lxml')
            soup.decode('utf-8')
            print(soup.select_one('.content').get_text())
            i['content'] = soup.select_one('.content').get_text()

            print(response.text)

            # tree = etree.html(response.text)
            # desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
            # html = requests.get(url='https://m.lagou.com/jobs/3018564.html',headers=headers, cookies=cookies)
            # soup = BeautifulSoup(html.text)
            # detail_url = 'https://www.lagou.com/jobs/{}.html'.format(3018564)
            # response = requests.get(url=detail_url, headers=headers, cookies=cookies)
            # response.encoding = 'utf-8'
            tree = etree.HTML(response.text)
            desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
            # print(soup.select('.job_bt') )
            # print html.text
            print (position['companyShortName'])
            time.sleep(1)
            info.append(i)
        return info
