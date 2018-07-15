import requests
import urllib.parse
import datetime
import csv
import numpy as np
import threading
from dateutil.relativedelta import relativedelta


# 获取评论
def get_review_origin(connection, date_start, date_end, next_page, token):
    headers = {
        'X-CSRF-TOKEN': token,
    }
    post_data = {
        'startDate': date_start,
        'endDate': date_end,
        'keywords': '',
        'entityId': 0,
        'gameId': 1791,
        'nextPage': next_page,
        'maxPage': 100,
        'currentPage': 0,
        # 不限制等级
        'rank': 0,
        'isTitle': 1,
        'isKeyword': 0,
        # 按照时间升序排列:1 ,降序：2
        'orderBy': 1,
        # 数据源：AppStore
        'categoryId': 9,
        # 应用商店评论
        'cateType': 2,
        # 垃圾过滤
        'filterRubbish': 1,
        'or_and': 'and',
        'filterFields': '',
        'filterValues': '',
        'sentiment': '0,1,2',
        'trashLevels': '0,1,2,3,4,5,6,7,8,9,10,11',
    }

    response = connection.post("http://fsight.qq.com/DataSearchAjax", data=post_data, headers=headers)
    return response.json().get('ret').get('searchDatas')


# 存储csv文件
def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8-sig') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


def get_review(date_start, date_end):
    connection = requests.session()
    connection.get("http://fsight.qq.com/Game/1791")
    token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

    review_sum = []

    for i in range(0, 20000):
        review = get_review_origin(connection, date_start, date_end, i, token)
        res_review = list(review)
        if len(res_review) == 0:
            break
        for review in res_review:
            review_sum.append(review)

    content_list_sum = []

    for i in range(0, len(review_sum)):
        content_list = []
        content_list.append(review_sum[i].get('createtime'))
        content_list.append(review_sum[i].get('author'))
        content_list.append(review_sum[i].get('rank'))
        content_list.append(review_sum[i].get('content'))
        content_list_sum.append(content_list)

    save_csv("../data/author_content", content_list_sum)


get_review(datetime.datetime(2016, 5, 1, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S'),
           datetime.datetime(2018, 5, 1, 23, 59, 00).strftime('%Y-%m-%d %H:%M:%S'))
