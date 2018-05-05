import analysis.tool as tool
import matplotlib.pyplot as plt
import csv
import numpy as np

tool.init()

# y = tool.get_app_rank_daily('23350')
#
# plt.figure()
# plt.plot(range(1, 731), y[1:])
# plt.ylim(0, 300)
# plt.gca().invert_yaxis()
# plt.show()
#
# a = 1
#
# exit(0)

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

# -------------------------------------计算所有session的sita, 存到./data/0.csv中

# ids = tool.app_ids
#
# id_sitas = []
# ii = 0
# for id in ids:
#     sessions = tool.get_leading_session(id)
#     sitas = [id]
#     for session in sessions:
#         sita = session.get_sita()
#         if sita > 0:
#             sitas.append(sita)
#     id_sitas.append(sitas)
#     print(id)
#
#     # if len(id_sitas) == 100:
#     #     tool.save_csv('data/' + str(ii), id_sitas)
#     #     ii += 1
#     #     id_sitas = []
#
# tool.save_csv('data/' + str(ii), id_sitas)
#
# a = 1


# -------------------------------------计算所有session的sita

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
# sitas_mean = np.mean(sitas)  # 3.061398376330555
# sitas_var = np.var(sitas)  # 0.026046925110970412
#
# a = 1

# -------------------------------------计算所有get_evidence_1

tool.get_evidence_1('23796')
