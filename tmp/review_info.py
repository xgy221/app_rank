import requests
import urllib.parse
import datetime
import csv

app_id = 1612581
mid_time = ''
res_review = []
content_list_sum = []


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
        'gameId': 1612581,
        'nextPage': next_page,
        'maxPage': 0,
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


def get_review_332(date_start, date_end):
    global mid_time, content_list_sum
    connection = requests.session()
    connection.get("http://fsight.qq.com/Game/1612581")
    token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

    review_sum = []
    count = 0

    for i in range(0, 332):
        global res_review
        review = get_review_origin(connection, date_start, date_end, i, token)
        if len(review):
            count = count + 1
            res_review = list(review)
            for review in res_review:
                review_sum.append(review)
    if count == 332:
        mid_time = res_review[-1].get('createtime')
        print(mid_time)

    if date_start == datetime.datetime(2017, 5, 1, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S'):
        for i in range(0, len(review_sum)):
            content_list = []
            content_list.append(review_sum[i].get('createtime'))
            content_list.append(review_sum[i].get('author'))
            content_list.append(review_sum[i].get('rank'))
            content_list.append(review_sum[i].get('content'))
            content_list_sum.append(content_list)
    else:
        for i in range(1, len(review_sum)):
            content_list = []
            content_list.append(review_sum[i].get('createtime'))
            content_list.append(review_sum[i].get('author'))
            content_list.append(review_sum[i].get('rank'))
            content_list.append(review_sum[i].get('content'))
            content_list_sum.append(content_list)

    # str(date_start[0:10])


def get_review():
    get_review_332(datetime.datetime(2017, 5, 1, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S'),
                   datetime.datetime(2018, 5, 1, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S'))
    mid_time_before = ''
    mid_time_after = mid_time
    while mid_time_before != mid_time_after:
        get_review_332(mid_time_after, datetime.datetime(2018, 5, 1, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S'))
        mid_time_before = mid_time_after
        mid_time_after = mid_time
    save_csv("../review_data/pay/author_content_" + str(app_id), content_list_sum)


get_review()
