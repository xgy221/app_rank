import requests
import urllib.parse
import datetime
import csv
import threading
from dateutil.relativedelta import relativedelta


# 获取某一天的某个排名区间
def get_rank_list(connection, date, token, rankRange):
    headers = {
        'X-BEE-COUNTRY': '0',
        'X-CSRF-TOKEN': token,
    }
    postData = {
        # 1：免费榜 2：付费榜 3：畅销榜
        'listCat': 1,
        'listType': 0,
        'rankRange': rankRange,
        'listDate': date,
    }

    response = connection.post("http://fsight.qq.com/GameListAjax", data=postData, headers=headers)
    return response.json().get('ret').get('ranks')


# 存储csv文件
def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


# 获取某段时间每天排名前300的APP信息
def get_top_100(dateStart, dateEnd):
    connection = requests.session()
    connection.get("http://fsight.qq.com/GameList?type=hotRank")
    token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

    # dateStart, dateEnd = datetime.date(2016, 4, 27), datetime.date(2018, 4, 27)
    date = dateStart
    res_sum = []
    id_name_dic = {}
    while date < dateEnd:
        print(date)

        rank_1_30 = get_rank_list(connection, date, token, 1)
        rank_31_200 = get_rank_list(connection, date, token, 2)

        res = list(rank_1_30) + list(rank_31_200)
        date += datetime.timedelta(days=1)
        res = res[0:100]

        for i in range(0, 100):
            id_name_dic[res[i].get('game_id')] = res[i].get('game_name')
            res[i] = res[i].get('game_id')
        res_sum.append(res)

    id_name = []
    for key, value in id_name_dic.items():
        id_name.append([key, value])
    save_csv("../data/rank_list_" + str(dateStart)+"_free"+str(100), res_sum)
    save_csv("../data/id_name_" + str(dateStart)+"_free"+str(100), id_name)
    print('finish=' + str(dateStart) + ':' + str(dateEnd))


# 使用线程提高爬取数据的速度：每个月开一线程
date = datetime.date(2017, 5, 1)
th_arr = []
while date < datetime.date(2018, 5, 1):
    next_month = date.month + 1
    next_year = date.year
    if next_month > 12:
        next_month = 1
        next_year += 1

    date_start = datetime.date(date.year, date.month, 1)
    date_end = datetime.date(next_year, next_month, 1)

    th_arr.append(threading.Thread(target=get_top_100, args=(date_start, date_end)))
    date += relativedelta(months=+1)

for th in th_arr:
    th.start()

# 等待所有子线程返回
for th in th_arr:
    th.join()

print('ok')
