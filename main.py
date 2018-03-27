# -*- coding: utf-8 -*-
import collections

import chardet
from collections import Counter
from https import Http
from parse import Parse
from setting import headers
from setting import cookies
import time
import logging
import sys
import xlwt
import csv
import pygal
import codecs
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from selenium import webdriver
from wordcloud import WordCloud
import charts
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
reload(sys)
sys.setdefaultencoding('utf8')
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
csvfile = codecs.open('csv.csv', 'w')  #打开方式还可以使用file对象
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
# htmlunit = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
# htmlunit.get("http://www.baidu.com")
series=[
]

word_dict= {}
pie_chart = pygal.Pie()
pie_chart.title = 'Browser usage by version in February 2012 (in %)'




def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    print(pageCount)
    info = []
    for i in range(1, 2):
        print('第%s页' % i)
        para['pn'] = str(i)
        htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
        generalParse = Parse(htmlCode)
        info = info + getInfoDetail(generalParse)
        time.sleep(2)
    return info


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info
#
# def jiebaclearText(text):
#     mywordlist = []
#     seg_list = jieba.cut(text, cut_all=False)
#     liststr="/ ".join(seg_list)
#     f_stop_text = ''
#     f_stop_text=unicode(f_stop_text,'utf-8')
#     f_stop_seg_list=f_stop_text.split('\n')
#     for myword in liststr.split('/'):
#         if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
#             mywordlist.append(myword)
#     return ''.join(mywordlist)

def processInfo(info, para):
    """
    信息存储
    """
    text = ''

    word_lst = []
    series1= [{
        'type': 'pie',
        'name': '浏览器访问量占比',
        'data': [
    #         ['Firefox', 45.0],
    #         ['IE', 26.8],
    # ['Safari', 8.5],
    # ['Opera', 6.2],
    ]
    }]
    logging.error('Process start')
    try:
        writer.writerow(['公司名称', '公司类型', '融资阶段','标签','公司规模','公司所在地','职位类型','职位要求','学历要求','福利','薪资','工作经验'])
        for p in info:
            text = text + str(p['content'])
            word_lst.append(str(p['positionSalary']))
            writer.writerow([str(p['companyName']),str(p['companyType']),str(p['companyStage']),str(p['companyLabel']),str(p['companySize']),str(p['companyDistrict']),str(p['positionType']),str(p['content']),str(p['positionEducation']),str(p['positionAdvantage']),str(p['positionSalary']), str(p['positionWorkYear'])])
        csvfile.close()
        seg_list = jieba.cut(text, cut_all=False)
        tags = jieba.analyse.extract_tags(text, topK=50)
    # type = chardet.detect("".join(seg_list))
        # text1 = text.decode(type["encoding"])
        for item in word_lst:
            if item not in word_dict:
                word_dict[item] = 1
            else:
                word_dict[item] += 1
        for key ,value in word_dict.items():
         series1[0]['data'].append(            [key,value*100/word_lst.__len__() ],
                                               )
         #                             )
         series.append( {
        'name':key,
        'data':[value],
        'type':'column',
                        })
        charts.plot(series1,options=dict(title=dict(text='薪资分布!!!')))

        # charts.plot(series,options=dict(title=dict(text='Charts is awesome!!!')))

        print "\"%s\":\"%s\"" % (key, value/word_dict.__len__()*100)

        print key,value*100/word_lst.__len__()
        print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
        # print (text)
        # text=jiebaclearText(text)
        print("Default Mode: " + "/ ".join(tags))  # 精确模式
        font_path = '肥肥扭扭体.ttf'
        wordcloud = WordCloud(background_color='white',font_path=font_path,scale=1.5).generate(text)

#显示词云图片

        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

        return True
    except Exception as e:
        print(e)
        return None


def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        info = getInfo(url, para)  # 获取信息
        flag = processInfo(info, para)  # 信息储存
        return flag
    else:
        return None


if __name__ == '__main__':
    kdList = [u'物联网应用技术']
    cityList = [u'上海']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    for city in cityList:
        print('%s爬取成功' % city)
        para = {'first': 'true', 'pn': '1', 'kd': kdList[0], 'city': city,'needAddtionalResult':'false','isSchoolJob':'0'}
        flag = main(url, para)
        if flag:
            print('%s爬取成功' % city)
        else:
            print('%s爬取失败' % city)
