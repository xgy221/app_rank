import requests
import urllib.parse
import datetime
import csv


def get_rank_list(connection, date, token, rankRange):
    headers = {
        'X-BEE-COUNTRY': '0',
        'X-CSRF-TOKEN': token,
    }
    postData = {
        'listCat': 2,
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


def get_top_300():
    connection = requests.session()
    connection.get("http://fsight.qq.com/GameList?type=hotRank")
    token = urllib.parse.unquote(connection.cookies.get('wetest_token'))

    dateStart, dateEnd = datetime.date(2017, 1, 1), datetime.date(2017, 1, 2)
    date = dateStart
    res_sum = []
    id_name_dic = {}
    while date <= dateEnd:
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
    save_csv("rank_list", res_sum)
    save_csv("id_name", id_name)


get_top_300()
