import requests
import urllib.parse
import datetime
import csv
import threading
from dateutil.relativedelta import relativedelta


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


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


def get_top_300(dateStart, dateEnd):
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
        rank_201_400 = get_rank_list(connection, date, token, 3)

        res = list(rank_1_30) + list(rank_31_200) + list(rank_201_400)
        date += datetime.timedelta(days=1)
        res = res[0:300]

        for i in range(0, 300):
            id_name_dic[res[i].get('entityId')] = res[i].get('game_name')
            res[i] = res[i].get('entityId')
        res_sum.append(res)

    id_name = []
    for key, value in id_name_dic.items():
        id_name.append([key, value])
    save_csv("../data/rank_list_" + str(dateStart), res_sum)
    save_csv("../data/id_name_" + str(dateStart), id_name)
    print('finish=' + str(dateStart) + ':' + str(dateEnd))


date = datetime.date(2016, 5, 1)
th_arr = []
while date < datetime.date(2018, 5, 1):
    next_month = date.month + 1
    next_year = date.year
    if next_month > 12:
        next_month = 1
        next_year += 1

    date_start = datetime.date(date.year, date.month, 1)
    date_end = datetime.date(next_year, next_month, 1)

    th_arr.append(threading.Thread(target=get_top_300, args=(date_start, date_end)))
    date += relativedelta(months=+1)

for th in th_arr:
    th.start()

for th in th_arr:
    th.join()

print('ok')
