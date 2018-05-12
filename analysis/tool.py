import csv
import math
import numpy as np

# 计算得出
sitas_mean = 3.0326049070384244
sitas_var = 0.035239392759751756
xs_mean = 188.22618053898066
xs_var = 6990.113601081377
lmd = 1.7705485378093095
w1 = 0.00023324623743173472
w2 = 0.01825358196608796
w3 = 0.9815131717964803

K = 300
R = 100
T = 7

rank_list_all_arr = None
app_index_dic = None
app_ids = None


def init():
    get_app_id_dic_and_ids()


class LeadingEvent:
    startTime = 0
    endTime = 0
    mid1Time = None
    mid2Time = None
    degreeLeft = None
    degreeRight = None
    mRankSum = 0

    def get_degree(self):
        if self.degreeLeft and self.degreeRight:
            return self.degreeLeft + self.degreeRight
        return 0

    # 维持阶段时长
    def get_m_t(self):
        if self.mid1Time and self.mid2Time and self.mid2Time >= self.mid1Time:
            return self.mid2Time - self.mid1Time + 1
        return 0

    # 维持阶段排名平均值
    def get_r_m_mean(self):
        m_t = self.get_m_t()
        if self.mRankSum and m_t:
            return self.mRankSum / m_t
        return 0


class LeadingSession:
    eventList = None
    startTime = None
    endTime = None

    def add_event(self, leading_event):
        if not self.eventList:
            self.eventList = []
        self.eventList.append(leading_event)
        self.endTime = leading_event.endTime

    # evidence1 指标
    def get_sita(self):
        if not self.eventList:
            return 0
        d_arr = []
        for event in self.eventList:
            event_degree = event.get_degree()
            if not event_degree:
                continue
            d_arr.append(event_degree)
        if not len(d_arr):
            return 0
        return np.mean(d_arr)

    # evidence2 指标
    def get_x(self):
        global K
        if not self.eventList:
            return 0
        x_arr = []
        for event in self.eventList:
            duration = event.get_m_t()
            mean = event.get_r_m_mean()
            if not duration:
                continue
            x_arr.append((K - mean) / duration)
        if not len(x_arr):
            return 0
        return np.mean(x_arr)


def get_leading_session(app_id):
    global T

    event_list = get_leading_event(app_id)

    session = None
    session_list = []
    for event in event_list:
        if not session:
            session = LeadingSession()
            session.add_event(event)
            session.startTime = event.startTime
            continue
        if session.endTime + T >= event.startTime:
            session.add_event(event)
        else:
            session_list.append(session)
            session = LeadingSession()
            session.add_event(event)
            session.startTime = event.startTime
    if session:
        session_list.append(session)

    return session_list


def get_leading_event(app_id):
    global K, R

    y = get_app_rank_daily(app_id)

    event_list = []
    event = None
    for i in range(1, len(y)):
        if y[i] <= K:
            if not event:
                event = LeadingEvent()
                event.startTime = event.endTime = i
            event.endTime = i

            if y[i] <= R:
                event.mRankSum += y[i]
                if not event.mid1Time:
                    event.mid1Time = i
                    if i > event.startTime:
                        event.degreeLeft = math.atan((K - y[i]) / (i - event.startTime))
                event.mid2Time = i
            if event.mid2Time and i > event.mid2Time:
                event.degreeRight = math.atan((K - y[event.mid2Time]) / (i - event.mid2Time))
        elif event:
            event_list.append(event)
            event = None
    if event:
        event_list.append(event)

    return event_list


def get_app_rank_daily(app_id):
    global rank_list_all_arr, app_index_dic

    if not rank_list_all_arr:
        with open('data/app_rank_daily.csv', 'r') as f:
            reader = csv.reader(f)
            rank_list_all_arr = list(reader)

    app_index = app_index_dic[app_id]
    res = list(map(int, rank_list_all_arr[app_index][0:731]))
    for index, item in enumerate(res):
        if not item:
            res[index] = 10000
    return res


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


# def get_session_sita_s(session):
#     degree_sum = []
#     for event in session.eventList:
#
#         start_time = event.startTime
#         end_time = event.endTime
#         middle1_time = event.mid1Time
#         middle2_time = event.mid2Time
#         if not middle1_time or not middle2_time == 0:
#             continue
#
#         if middle1_time - start_time > 0 and end_time - middle2_time > 0:
#             degree1 = math.atan((K - y[middle1_time - 1]) / (middle1_time - start_time))
#             degree2 = math.atan((K - y[middle2_time - 1]) / (end_time - middle2_time))
#             degree_sum.append(degree1 + degree2)
#
#     if len(degree_sum) == 0:
#         return 0
#
#     return sum(degree_sum) / len(degree_sum)


def get_app_id_dic_and_ids():
    global app_index_dic, app_ids
    if app_index_dic and app_ids:
        return app_index_dic, app_ids

    ids = []
    with open('data/ids.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            ids = line
    dic = {}
    for index, id in enumerate(ids):
        dic[id] = index

    app_index_dic = dic
    app_ids = ids
    return dic, ids


def get_session_sita_p(session: LeadingSession):
    global sitas_mean, sitas_var

    return 1 / 2 * (1 + math.erf((session.get_sita() - sitas_mean) / (sitas_var * math.sqrt(2))))


def get_evidence_1(app_id):
    sessions = get_leading_session(app_id)
    for session in sessions:
        print(get_session_sita_p(session))


def get_session_x_p(session: LeadingSession):
    global xs_mean, xs_var

    return 1 / 2 * (1 + math.erf((session.get_x() - xs_mean) / (xs_var * math.sqrt(2))))


def get_evidence_2(app_id):
    sessions = get_leading_session(app_id)
    for session in sessions:
        print(get_session_x_p(session))


def get_session_3_p(session: LeadingSession):
    global lmd

    e_c = len(session.eventList)
    sum = 0

    for i in range(0, e_c):
        sum += (lmd ** i) / np.math.factorial(i)
    return math.exp(-lmd) * sum


def get_evidence_3(app_id):
    sessions = get_leading_session(app_id)
    for session in sessions:
        print(get_session_3_p(session))

# global rank_list_all_arr, K, R, T, y
#
# session_list = get_leading_session(app_id)
#
# degrees = []
#
# for session in session_list:
#     degree_avg = get_session_seita_s(session)
#     degrees.append(degree_avg)
#
# # 计算全局的 n1, n2
# n1 = 1  # 平均值
# n2 = 1  # 方差
#
# return 1 / 2 * (1 + math.erf((sdegree - n1) / (n2 * math.sqrt(2))))
