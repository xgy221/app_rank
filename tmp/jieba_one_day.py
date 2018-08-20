import jieba
import csv

stop_words = []
result_words = []

with open("../data/stop_words.txt", "r") as f:
    for word in f:
        stop_words.append(word.strip())


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8-sig') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def format_str(content):
    # content = unicode(content, 'utf-8').
    content_str = ''
    for i in content:
        if is_chinese(i) or is_alphabet(i) or is_number(i):
            content_str = content_str + i
    return content_str


with open("../paper_needed/review1739536.csv", 'r', newline="", encoding='utf-8-sig') as f:
    all_list = list(csv.reader((line.replace('\0', '') for line in f)))
    for item in all_list:
        xixistr = format_str(item[3])
        review_words = jieba.cut(xixistr)
        out_words = []
        for word in review_words:
            if word not in stop_words:
                if word != '\t':
                    out_words.append(word)
        useful = out_words
        if len(useful) > 0:
            result_words.append(useful)

save_csv("../paper_needed/jieba_deal" + str(1739536), result_words)
