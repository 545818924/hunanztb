#!/usr/bin/env python
# coding: utf-8

"""
Author: Liu.mou
Date: 2021-07-06
Description: 湖南省招标投标监管网的招标信息(截止到当天所有项目)
"""
import re
import json
import requests
import pandas as pd

# 获取总计项目条数
url = 'http://bidding.hunan.gov.cn/bidding/notice?categoryId=92'
response = requests.get(url)
text = response.text
total = re.search('共 (\d+) 条', text).group(1)

# 获取api信息
api_url = f'http://bidding.hunan.gov.cn/ztb/api/getBiddingList?totalCount={total}&limit={total}&categoryId=92&areaNo='
file_base_url = 'http://bidding.hunan.gov.cn/ztbPdf/'
filename = 'ztb_result.xlsx'
rlist = []


try:
    response = requests.get(api_url)
    result = response.json()
    items = result['page']['list']
#         print(items)
except:
    print("爬取失败")
else:
    for item in items:
        rlist.append({'id': item.get('id'),
                      '创建时间': item.get('createTime'),
                      '项目名称': item.get('projectName'),
                      '文件地址': f'{file_base_url}{item.get("bidFilePath")}' if item.get('bidFilePath') else '接口未包含pdf地址'
                      })


# 保存到excel
df = pd.DataFrame(rlist)
df.to_excel(filename, index=False, encoding='utf8')
