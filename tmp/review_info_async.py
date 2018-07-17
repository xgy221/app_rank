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
        json = await response.json(content_type=None)
    return json.get('ret').get('searchDatas')


def getuseful(dataraw):
    # return dataraw.get('createtime')
    return [
        dataraw.get('createtime'),
        dataraw.get('author'),
        dataraw.get('rank'),
        dataraw.get('content'),
    ]


def datetime2timestamp(datetimestr):
    return time.mktime(time.strptime(datetimestr, "%Y-%m-%d %H:%M:%S"))


def getmidtime(start, end):
    start = datetime2timestamp(start)
    end = datetime2timestamp(end)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((start + end) / 2))


async def get_data_async(session, start, end, appid, headers):
    print(start, end)
    data = await get_review_origin(session, start, end, appid, headers)
    data = list(map(getuseful, data))

    if len(data) < 30:
        return data

    # start = data[-1]
    start = data[-1][0]
    mid = getmidtime(start, end)

    ltask = get_data_async(session, start, mid, appid, headers)
    rtask = get_data_async(session, mid, end, appid, headers)

    dones, pendings = await asyncio.wait([ltask, rtask])

    for task in dones:
        data += task.result()

    return data


async def gettoken(session, url):
    async with session.get(url) as response:
        # return await response.text()
        # token = response.cookies.get('wetest_token').value
        token = response.cookies['wetest_token'].value
        return urllib.parse.unquote(token)


async def main():
    appid = 173

    now = time.time()

    date_start = datetime.datetime(2017, 5, 1, 0, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
    # date_end = datetime.datetime(2017, 10, 1, 0, 00, 00).strftime('%Y-%m-%d %H:%M:%S')
    date_end = datetime.datetime(2018, 5, 1, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')

    async with aiohttp.ClientSession() as session:
        token = await gettoken(session, 'http://fsight.qq.com/Game/' + str(appid))
        headers = {
            'X-CSRF-TOKEN': token,
        }
        data = await get_data_async(session, date_start, date_end, appid, headers)

    print(len(data), time.time() - now)
    return data


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# 2017, 5, 1, 0, 00, 00

# 2017, 10, 1, 0, 00, 00
# 141919 65.3868260383606

# 216379 108.60358595848083