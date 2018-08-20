import requests
import urllib.parse
import datetime
import csv

app_id = 1739536
mid_time = ''
res_review = []
content_list_sum = []


# 获取评论
def get_review_origin(connection, date_start, date_end, token):
    global app_id
    headers = {
        'X-CSRF-TOKEN': token,
    }
    post_data = {
        'startDate': date_start,
        'endDate': date_end,
        'keywords': '',
        'entityId': 0,
        'gameId': app_id,
        'nextPage': 0,
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
        'sentiment': '',
        'trashLevels': '',
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
    global mid_time, content_list_sum
    connection = requests.session()
    connection.get("http://fsight.qq.com/Game/" + str(app_id))
    token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

    review_sum = []

    review = get_review_origin(connection, date_start, date_end, token)
    if len(review):
        global res_review
        res_review = list(review)
        for review in res_review:
            review_sum.append(review)

    if date_start == datetime.datetime(2018, 8, 12, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S'):
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

def save_review():
    get_review(datetime.datetime(2018, 8, 12, 00, 00, 00).strftime('%Y-%m-%d %H:%M:%S'),
           datetime.datetime(2018, 8, 12, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S'))
    save_csv("../paper_needed/review" + str(app_id), content_list_sum)

save_review()