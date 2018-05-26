import csv
import datetime
from dateutil.relativedelta import relativedelta

date = datetime.date(2016, 5, 1)
id_name = {}
while date <= datetime.date(2018, 4, 1):
    with open('data/id_name_' + str(date) + '.csv', 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            id_name[row[0]] = row[1]
        date += relativedelta(months=+1)

id_name_all = []
for key, value in id_name.items():
    id_name_all.append([key, value])


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


save_csv('data/id_name_all', id_name_all)

date = datetime.date(2016, 5, 1)
rank_list = []
while date <= datetime.date(2018, 4, 1):
    with open('data/rank_list_' + str(date) + '.csv', 'r') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            rank_list.append(row)
        date += relativedelta(months=+1)

save_csv('data/rank_list_all', rank_list)