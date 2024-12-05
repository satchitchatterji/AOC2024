with open("5_input.txt", "r") as f:
    lines = [x.strip() for x in f.readlines()]

split_idx = lines.index('')
rules = lines[:split_idx]
updates = lines[split_idx+1:]

rules = ",".join(rules)
updates = [[int(x) for x in update.split(',')] for update in updates]

def generate_antirules(update):
    update = update[::-1]
    antirules = []
    for idx1 in range(len(update)):
        for idx2 in range(idx1, len(update)):
            if idx1 == idx2:
                continue
            antirules.append("|".join([str(update[idx1]), str(update[idx2])]))
    return antirules

def check_violation(rules, antirules, update):
    for antirule in antirules:
        # print(antirule)
        if antirule in rules:
            return True
    return False

violations = []
total = 0
for update in updates:
    antirules = generate_antirules(update)
    if check_violation(rules, antirules, update):
        violations.append(update)
    else:
        total += update[len(update)//2]

print(total)

##########

def reorder_update(rules, update):
    violation = False
    antirules = generate_antirules(update)
    for antirule in antirules:
        if antirule in rules:
            num1, num2 = [int(x) for x in antirule.split("|")]
            idx1, idx2 = update.index(num1), update.index(num2)
            update[idx1], update[idx2] = num2, num1
            violation = True
        
    if violation:
        return reorder_update(rules, update)
    
    return update[len(update)//2]

total_violation = 0
for violation in violations:
    total_violation += reorder_update(rules, violation)
print(total_violation)
