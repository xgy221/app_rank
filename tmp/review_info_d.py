import requests
import urllib.parse
import datetime
import csv
import time
import threading

# app_id = 1612581
app_id = 173
mid_time = ''
res_review = []
content_list_sum = []


# 获取评论
def get_review_origin(connection, date_start, date_end, next_page, token):
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


def datetime2timestamp(datetimestr):
    return time.mktime(time.strptime(datetimestr, "%Y-%m-%d %H:%M:%S"))


def getmidtime(start, end):
    start = datetime2timestamp(start)
    end = datetime2timestamp(end)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((start + end) / 2))


class WorkerThread(threading.Thread):

    def __init__(self, func, args=()):
        super(WorkerThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result if self.result else []  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


tstart = time.time()

connection = requests.session()
connection.get("http://fsight.qq.com/Game/" + str(app_id))
token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

date_start = datetime.datetime(2017, 5, 1, 0, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
# date_end = datetime.datetime(2017, 10, 1, 0, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
date_end = datetime.datetime(2018, 5, 1, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')


def getuseful(dataraw):
    # return dataraw.get('createtime')
    return [
        dataraw.get('createtime'),
        dataraw.get('author'),
        dataraw.get('rank'),
        dataraw.get('content'),
    ]


# 同步多线程写法
def getDataThread(start, end):
    print(start, end)
    global connection, token
    data = get_review_origin(connection, start, end, 0, token)
    data = list(map(getuseful, data))

    if len(data) < 30:
        return data

    # start = data[-1]
    start = data[-1][0]
    mid = getmidtime(start, end)
    tleft = WorkerThread(getDataThread, args=(start, mid))
    tright = WorkerThread(getDataThread, args=(mid, end))
    tleft.start()
    tright.start()
    tleft.join()
    tright.join()
    data += tleft.get_result()
    data += tright.get_result()

    return data


# def getDataLine(start, end):
#     data = []
#     while datetime2timestamp(start) < datetime2timestamp(end):
#         review = get_review_origin(connection, start, end, 0, token)
#         review = list(map(getuseful, review))
#         data += review
#         if len(review) < 30:
#             break
#         # start = review[-1]
#         start = review[-1][0]
#     return data


data = getDataThread(date_start, date_end)

tend = time.time()

print(len(data), tend - tstart)
