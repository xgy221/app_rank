import csv
import math

rank_list_all_arr = None
K = 300
R = 100
T = 7
y = []


class LeadingEvent:
    startTime = 0
    endTime = 0
    mid1Time = None
    mid2Time = None


class LeadingSession:
    eventList = None
    startTime = None
    endTime = None

    def add_event(self, leading_event):
        if not self.eventList:
            self.eventList = []
        self.eventList.append(leading_event)
        self.endTime = leading_event.endTime


def get_leading_session(app_id):
    global rank_list_all_arr, K, R, T

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
    global rank_list_all_arr, K, R, T, y

    if not rank_list_all_arr:
        with open('../data/rank_list_all.csv', 'r') as f:
            reader = csv.reader(f)
            rank_list_all_arr = list(reader)

    for line in rank_list_all_arr:
        try:
            y.append(line.index(app_id) + 1)
        except ValueError:
            y.append(10000)

    event_list = []
    event = None
    for i in range(1, len(y) + 1):
        if y[i - 1] <= K:
            if event:
                event.endTime = i
                if y[i - 1] <= R:
                    event.mid2Time = i
                    if not event.mid1Time:
                        event.mid1Time = i
            else:
                event = LeadingEvent()
                event.startTime = event.endTime = i
        elif event:
            event_list.append(event)
            event = None
    if event:
        event_list.append(event)

    return event_list


def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)


def get_session_seita_s(session):
    degree_sum = []
    for event in session.eventList:

        start_time = event.startTime
        end_time = event.endTime
        middle1_time = event.mid1Time
        middle2_time = event.mid2Time
        if middle1_time == 0 or middle2_time == 0:
            continue

        if middle1_time - start_time > 0 and end_time - middle2_time > 0:
            degree1 = math.atan((K - y[middle1_time - 1]) / (middle1_time - start_time))
            degree2 = math.atan((K - y[middle2_time - 1]) / (end_time - middle2_time))
            degree_sum.append(degree1 + degree2)

    if len(degree_sum) == 0:
        return 0

    return sum(degree_sum) / len(degree_sum)


def get_evidence_1(app_id):
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
