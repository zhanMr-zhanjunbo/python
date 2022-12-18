import time
import requests
import json
from multiprocessing.dummy import Pool

baseurl = 'http://www.moj.gov.cn/sfbsearch/es/getTrsNewsByParams?anyOneWords=&beginDate=&endDate=&filterWords=&'


# 自定义函数
def query(name):
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


laws_list = query("劳动仲裁")
print(len(laws_list))
for i in laws_list:
    print(i)

# start = time.time()
# name_list = ["合同诈骗", "劳动仲裁", "交通安全事故", "离婚案件", "遗产继承"]
# pool = Pool(5)
# pool.map(query, name_list)
# end = time.time()
# print(f'5线程访问100次CSDN，耗时：{end - start}')
