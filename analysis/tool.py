import csv


class LeadingEvent:
    startTime = 0
    endTime = 0


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
    eventList = get_leading_event(app_id)

    session = None
    sessionList = []
    for event in eventList:
        if not session:
            session = LeadingSession()
            session.add_event(event)
            session.startTime = event.startTime
            continue
        if session.endTime + 7 >= event.startTime:
            session.add_event(event)
        else:
            sessionList.append(session)
            session = LeadingSession()
            session.add_event(event)
            session.startTime = event.startTime
    if session:
        sessionList.append(session)

    return sessionList


rank_list_all_arr = None


def get_leading_event(app_id):
    global rank_list_all_arr
    y = []

    if not rank_list_all_arr:
        with open('../data/rank_list_all.csv', 'r') as f:
            reader = csv.reader(f)
            rank_list_all_arr = list(reader)

    for line in rank_list_all_arr:
        try:
            y.append(line.index(app_id) + 1)
        except ValueError:
            y.append(10000)

    K = 300
    T = 7
    eventList = []
    event = None
    for i in range(0, len(y)):
        if y[i] <= K:
            if event:
                event.endTime = i + 1
            else:
                event = LeadingEvent()
                event.startTime = event.endTime = i + 1
        elif event:
            eventList.append(event)
            event = None
    if event:
        eventList.append(event)

    return eventList

def save_csv(file_name, data):
    with open(file_name + ".csv", "w", newline="", encoding='utf-8') as w:
        writer = csv.writer(w)
        for row in data:
            writer.writerow(row)