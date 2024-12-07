
results, reports = [], []
with open("7_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        result, line = line.split(":")
        result = int(result)
        results.append(result)
        nums = [int(x.strip()) for x in line.split()]
        reports.append(nums)

def check_valid(result, report):
    if len(report) == 1:
        return report[0] == result
    
    report_new = report[1:].copy()
    report_new[0] += report[0]
    
    add_valid = check_valid(result, report_new)

    report_new[0] -= report[0]
    report_new[0] *= report[0]

    mult_valid = check_valid(result, report_new)

    report_new[0] /= report[0]
    report_new[0] = int(str(report[0]) + str(int(report_new[0])))

    str_valid = check_valid(result, report_new)

    return add_valid or mult_valid or str_valid

total = 0
for result, report in zip(results, reports):
    if check_valid(result, report):
        total+=result

print(total)