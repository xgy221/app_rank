import analysis.tool as tool
import matplotlib.pyplot as plt
import csv
import numpy as np
import math

tool.init()

y = tool.get_app_rank_daily('39968')

plt.figure()
plt.plot(range(1, 731), y[1:])
plt.ylim(0, 300)
plt.gca().invert_yaxis()
plt.show()

sessions = tool.get_leading_session('39968')
for session in sessions:
    print(str(session.startTime) + '-' + str(session.endTime)+ ":")
    events = session.eventList
    for event in events:
        print('\t' + str(event.startTime) + '-' + str(event.endTime))

a = 1

exit(0)

# -------------------------------------------------------------计算所有app_id

# ids = []
# with open('../data/id_name_all.csv', 'r') as f:
#     reader = csv.reader(f)
#     for line in reader:
#         ids.append(line[0])
#         ids = sorted(ids, key=int)
#     tool.save_csv('data/ids', [ids])

# -------------------------------------------------------------计算所有app排名

# with open('../data/rank_list_all.csv', 'r') as f:
#     reader = csv.reader(f)
#     rank_list_all_arr = list(reader)
#
# app_id_dic, ids = tool.get_app_id_dic_and_ids()
# table = np.zeros((len(app_id_dic) + 1, 730 + 2), dtype=np.int32)
# for row, id in enumerate(ids):
#     table[row][0] = int(id)
# for day, row in enumerate(rank_list_all_arr):
#     for rank, item in enumerate(row):
#         table[app_id_dic[item]][day + 1] = rank + 1
#
# tool.save_csv('data/app_rank_daily', table)


# -------------------------------------计算所有session的sita evidence_1

# ids = tool.app_ids
#
# sitas = []
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     for session in sessions:
#         sita = session.get_sita()
#         if sita > 0:
#             sitas.append(sita)
#
# sitas_mean = np.mean(sitas)  # 3.0326049070384244
# sitas_var = np.var(sitas)  # 0.035239392759751756
#
# a = 1

# -------------------------------------计算所有get_evidence_1

# tool.get_evidence_1('23796')

# -------------------------------------计算所有session的x evidence_2

# ids = tool.app_ids
#
# xs = []
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     for session in sessions:
#         x = session.get_x()
#         if x > 0:
#             xs.append(x)
#
# xs_mean = np.mean(xs)  # 188.22618053898066
# xs_var = np.var(xs)  # 6990.113601081377
#
# a = 1

# -------------------------------------计算所有get_evidence_2

# tool.get_evidence_2('23796')

# -------------------------------------计算所有session的 evidence_3

# ids = tool.app_ids
#
# ecs = []
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     for session in sessions:
#         e_c = len(session.eventList)
#         ecs.append(e_c)
#
# lmd = np.mean(ecs)  # 1.7705485378093095
#
# a = 1

# -------------------------------------计算所有get_evidence_3

# tool.get_evidence_3('23796')

# -------------------------------------存储所有Session的三个证据

# ids = tool.app_ids
#
# data = []
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     for session in sessions:
#         row = [id]
#         e1 = tool.get_session_sita_p(session)
#         e2 = tool.get_session_x_p(session)
#         e3 = tool.get_session_3_p(session)
#         row.append(e1)
#         row.append(e2)
#         row.append(e3)
#         data.append(row)
# tool.save_csv('data/session_evidence', data)


# -------------------------------------计算三个权重
# w1 = w2 = w3 = 1 / 3
# ids = tool.app_ids
#
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     for session in sessions:
#         e1 = tool.get_session_sita_p(session)
#         e2 = tool.get_session_x_p(session)
#         e3 = tool.get_session_3_p(session)
#         e = (e1 + e2 + e3) / 3
#         v1 = (e1 - e) * (e1 - e)
#         v2 = (e2 - e) * (e2 - e)
#         v3 = (e3 - e) * (e3 - e)
#         sum_e = w1 * math.exp(-0.01 * v1) + w2 * math.exp(-0.01 * v2) + w3 * math.exp(-0.01 * v3)
#         w1 = (w1 * math.exp(-0.01 * v1)) / sum_e
#         w2 = (w2 * math.exp(-0.01 * v2)) / sum_e
#         w3 = (w3 * math.exp(-0.01 * v3)) / sum_e
# print(w1,w2,w3)

# -------------------------------------计算每个Session的a_evidence
ids = tool.app_ids
a_evidence_array = []
for id in ids:
    sessions = tool.get_leading_session(id)
    for session in sessions:
        e1 = tool.get_session_sita_p(session)
        e2 = tool.get_session_x_p(session)
        e3 = tool.get_session_3_p(session)
        a_evidence = tool.w1 * e1 + tool.w2 * e2 + tool.w3 * e3
        a_evidence_array.append([id, a_evidence])
a_evidence_array = sorted(a_evidence_array, key=lambda row: -row[-1])
tool.save_csv('data/session_evidence_aggregation', a_evidence_array)
