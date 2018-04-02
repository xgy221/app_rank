import Leadingsession as ls
import math

R = 100
degrees = []

for session in ls.sessionList:
    degree_sum = []
    for event in session.eventList:
        startTime = event.startTime
        endTime = event.endTime
        middle1Time = 0
        middle2Time = 0
        for time in range(startTime-1, endTime, 1):
            if ls.y[time] <= R:
                middle1Time = time+1
                break
        for time in range(endTime-1, startTime-2, -1):
            if ls.y[time] <= R:
                middle2Time = time+1
                break
        if middle1Time == 0 or middle2Time == 0:
            continue
        try:
            print('~~', startTime, middle1Time, middle2Time, endTime)
            degree1 = math.atan((ls.K - ls.y[middle1Time-1]) / (middle1Time - startTime))
            degree2 = math.atan((ls.K - ls.y[middle2Time-1]) / (endTime - middle2Time))
            degree_sum.append(degree1 + degree2)
        except ZeroDivisionError:
            print('******')
            continue
    if len(degree_sum) == 0:
        continue
    degree_s = sum(degree_sum) / len(degree_sum)
    degrees.append(degree_s)
if len(degrees) == 0:
    print('无数据')
    exit(1)

if len(degrees) == 1:
    print(degrees[0])
    exit(1)

average = sum(degrees) / len(degrees)
variance = 0
sum_degree = 0

for i in degrees:
    sum_degree += (i - average) * (i - average)
    # variance = (i - average) * (i - average)
    # evidence1 = 1 / 2 * (1 + math.erf((i - average) / (math.sqrt(variance) * math.sqrt(2))))
    # print(i, evidence1)
variance = sum_degree / len(degrees)  # 均值
for sdegree in degrees:
    evidence1 = 1 / 2 * (1 + math.erf((sdegree - average) / (variance * math.sqrt(2))))
    print(sdegree, evidence1)
