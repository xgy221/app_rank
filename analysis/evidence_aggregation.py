w = [1 / 3, 1 / 3, 1 / 3]
array_evidence_list = [[0.2, 0.4, 0.6], [0.1, 0.6, 0.8]]
evidence_aggregation_sum = []
average_evidence = []
variance_sum = []

for array_evidence in array_evidence_list:
    evidence_aggregation = 0
    for i in range(len(array_evidence)):
        evidence_aggregation = evidence_aggregation + w[i] * array_evidence[i]
    evidence_aggregation_sum.append(evidence_aggregation)

print(evidence_aggregation_sum)

for array_evidence in array_evidence_list:
    average_evidence_item = sum(array_evidence) / len(array_evidence)
    average_evidence.append(average_evidence_item)
    variance = []
    for evidence in array_evidence:
        variance_item = (evidence - average_evidence_item) * (evidence - average_evidence_item)
        variance.append(variance_item)
    variance_sum.append(variance)

# print(average_evidence)
# print(variance_sum)

sum_evidence = 0
for variance in variance_sum:
    for i in range(len(variance)):
        sum_evidence = sum_evidence + w[i] * variance[i]

print(sum_evidence)

