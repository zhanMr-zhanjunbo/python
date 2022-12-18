import requests
import json

baseurl = 'http://www.moj.gov.cn/sfbsearch/es/getTrsNewsByParams?anyOneWords=&beginDate=&endDate=&filterWords=&'


# 自定义函数
def query_law_msg(name):
    wd = f'keyWords={name}&pageNum=1&pageSize=50&place=&range=&searchType=2'
    url = baseurl + wd
    laws_list = []
    res = requests.get(url)
    law = json.loads(res.text)
    lawsList = law['list']
    for j in lawsList:
        content = j.get('docContent')[:300]
        laws_list.append(tuple((j.get('docTitle'), content, j.get('docPubUrl'))))
    return laws_list




