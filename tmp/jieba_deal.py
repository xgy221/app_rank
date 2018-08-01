import jieba
import csv

stop_words = []
result_words = []

with open("../data/stop_words.txt", "r") as f:
    for word in f:
        stop_words.append(word.strip())

print(stop_words)

with open("../review_data/free/review75.csv", 'r', newline="", encoding='utf-8-sig') as f:
    all_list = list(csv.reader((line.replace('\0', '') for line in f)))
    for item in all_list:
        review_words = jieba.cut(item[3])
        out_words = []
        for word in review_words:
            if word not in stop_words:
                if word != '\t':
                    out_words.append(word)
        result_words.append(out_words)


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8-sig') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


save_csv("../pre_processed_data/free" + str(75), result_words)


