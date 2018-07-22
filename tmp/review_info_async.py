import aiohttp
import asyncio
import urllib.parse
import requests
import datetime
import csv
import time


# 获取评论
async def get_review_origin(session, date_start, date_end, appid, headers):
    post_data = {
        'startDate': date_start,
        'endDate': date_end,
        'keywords': '',
        'entityId': 0,
        'gameId': appid,
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
        'sentiment': '0,1,2',
        'trashLevels': '0,1,2,3,4,5,6,7,8,9,10,11',
    }
    async with session.post("http://fsight.qq.com/DataSearchAjax", data=post_data, headers=headers) as response:
        try:
            json = await response.json(content_type=None)
            return json.get('ret').get('searchDatas')
        except BaseException as e:
            print(e)

    return []


def getuseful(dataraw):
    # return dataraw.get('createtime')
    return [
        dataraw.get('createtime'),
        dataraw.get('author'),
        dataraw.get('rank'),
        dataraw.get('content'),
        dataraw.get('docId'),
    ]


def datetime2timestamp(datetimestr):
    return time.mktime(time.strptime(datetimestr, "%Y-%m-%d %H:%M:%S"))


def getnextsecond(date):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datetime2timestamp(date) + 1))


def getmidtime(start, end):
    start = datetime2timestamp(start)
    end = datetime2timestamp(end)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((start + end) / 2))


async def get_data_async(session, start, end, appid, headers):
    print(start, end)
    data = await get_review_origin(session, start, end, appid, headers)
    data = list(map(getuseful, data))

    if len(data) < 30:
        return start, data

    # start = data[-1]
    start_sub = data[-1][0]
    mid = getmidtime(start_sub, end)

    ltask = get_data_async(session, start_sub, mid, appid, headers)
    rtask = get_data_async(session, mid, end, appid, headers)

    dones, pendings = await asyncio.wait([ltask, rtask])

    ldata = []
    rdata = []
    for task in dones:
        _start, _data = task.result()
        if start_sub == _start:
            ldata = _data
        else:
            rdata = _data

    data += ldata + rdata

    return start, data


async def gettoken(session, url):
    async with session.get(url) as response:
        # return await response.text()
        # token = response.cookies.get('wetest_token').value
        token = response.cookies['wetest_token'].value
        return urllib.parse.unquote(token)


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8-sig') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


def uniquedata(data):
    idset = set()
    res = []
    for row in data:
        id = row[-1]
        if id not in idset:
            idset.add(id)
            res.append(row[:-1])
    return res


async def main():
    now = time.time()

    date_start = datetime.datetime(2017, 5, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    # date_end = datetime.datetime(2017, 5, 1, 0, 2, 39).strftime('%Y-%m-%d %H:%M:%S')
    # date_end = datetime.datetime(2017, 6, 1, 0, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    date_end = datetime.datetime(2018, 5, 1, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')

    # date_start = datetime.datetime(2017, 5, 27, 20, 4, 8).strftime('%Y-%m-%d %H:%M:%S')
    # # date_end = datetime.datetime(2017, 10, 1, 0, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
    # date_end = datetime.datetime(2017, 5, 27, 20, 7, 46).strftime('%Y-%m-%d %H:%M:%S')

    # timeout = aiohttp.ClientTimeout(total=60)
    # async with aiohttp.ClientSession(timeout=timeout) as session:
    async with aiohttp.ClientSession() as session:
        token = await gettoken(session, 'http://fsight.qq.com/Game/173')
        headers = {
            'X-CSRF-TOKEN': token,
        }
        appids = [173]
        # appids = [1143952, 935106, 857030, 1203042, 1115251, 9185, 6681, 1191777, 667236, 7158, 1199024]
        # appids = [857030, 1203042, 1115251, 9185, 6681, 1191777, 667236, 7158, 1199024]
        for appid in appids:
            print(appid)
            _, data = await get_data_async(session, date_start, date_end, appid, headers)
            # 去重
            data = uniquedata(data)
            save_csv("../review_data/pay/dyh_t_" + str(appid), data)
            print(len(data), time.time() - now)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# 2017, 5, 1, 0, 00, 00

# 2017, 10, 1, 0, 00, 00
# 141919 65.3868260383606

# 216379 108.60358595848083
