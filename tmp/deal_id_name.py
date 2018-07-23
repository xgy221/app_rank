import csv


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8-sig') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


with open("../data/data_needed/id_name_free.csv", 'r', newline="", encoding='utf-8-sig') as f:
    all_list = list(csv.reader((line.replace('\0', '') for line in f)))
    for id_name in all_list:
        if id_name[0] == ''and id_name[1] == '':
            print(id_name)
            all_list.remove(id_name)
    save_csv("../data/data_needed/id_name_free_dealed", all_list)