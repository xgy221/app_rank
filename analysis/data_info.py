import csv
import matplotlib.pyplot as plt
import math
import analysis.tool as tool

"""数据集中app个数以及排名个数"""
with open('../data/id_name_all.csv', 'r',encoding='utf-8') as f:
    reader_id = csv.reader(f)
    app_list = list(reader_id)
    print("app个数: " + str(len(app_list)))

with open('../data/rank_list_all.csv', 'r') as f:
    reader_rank = csv.reader(f)
    rank_list = list(reader_rank)
    print("排名个数: " + str(len(rank_list) * 300))

"""不同排名的应用程序数量的分布"""
res = []
for col in range(0, 300):
    s = set()
    for row in range(len(rank_list)):
        s.add(rank_list[row][col])
    res.append(len(s))

x = range(0, 300)
y = res
rank_number_graph = plt.figure()
plt.scatter(x, y, s=4)
# x，y取值范围设置
plt.xlim(0, 300)
plt.ylim(0, 600)
plt.axis()
plt.title("Rank Number of Scatter Plot")
plt.xlabel("Ranking")
plt.ylabel("Number of Apps")
plt.savefig('Rank_Number_Scatter_Plot.png')

"""APP包含的event以及session数量分布"""
# res_event = []
# res_session = []
# for app_id, index in app_list:
#     res_event.append(len(tool.get_leading_event(str(app_id))))
#     res_session.append(len(tool.get_leading_session(str(app_id))))
# tool.save_csv('event_count', [res_event])
# tool.save_csv('session_count', [res_session])

with open('event_count.csv', 'r') as f:
    res_event = list(csv.reader(f))[0]
with open('session_count.csv', 'r') as f:
    res_session = list(csv.reader(f))[0]

"""event_number"""
chart_data = []
max_i = 60
for i in range(max_i):
    chart_data.append(0)

for i in range(len(res_event)):
    if int(res_event[i]) >= max_i:
        continue
    chart_data[int(res_event[i])] += 1

plt.clf()
x = range(len(chart_data))
y = chart_data
plt.xlim(0, max_i)
plt.bar(x, y)
plt.savefig('Event_Number.png')

sum = 0
for number in res_event:
    sum += int(number)
print('每个APP的平均event个数: ' + str(sum / len(res_event)))

"""session_number"""
chart_data = []
max_i = 20
for i in range(max_i):
    chart_data.append(0)

for i in range(len(res_session)):
    if int(res_event[i]) >= max_i:
        continue
    chart_data[int(res_session[i])] += 1

plt.clf()
x = range(len(chart_data))
y = chart_data
plt.xlim(0, max_i)
plt.bar(x, y)
plt.savefig('Session_Number.png')

sum = 0
for number in res_session:
    sum += int(number)
print('每个APP的平均session个数: ' + str(sum / len(res_session)))

"""event_session个数"""
# session_event_number = []
# for app_id, index in app_list:
#     for session in tool.get_leading_session(str(app_id)):
#         session_event_number.append(len(session.eventList))
# tool.save_csv('session_event_count', [session_event_number])

with open('session_event_count.csv', 'r') as f:
    session_event_number = list(csv.reader(f))[0]

chart_data = []
max_i = 40
for i in range(max_i):
    chart_data.append(0)

for i in range(len(session_event_number)):
    chart_data[int(session_event_number[i])] += 1

plt.clf()
x = range(len(chart_data))
y = chart_data
plt.xlim(0, max_i)
plt.bar(x, y)
plt.savefig('Session_Event_Number.png')

sum = 0
for number in session_event_number:
    sum += int(number)
print('每个session的平均event个数: ' + str(sum / len(session_event_number)))
