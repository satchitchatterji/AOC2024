import re

with open("3_input.txt", "r") as f:
    lines = f.read()

pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
matches = re.findall(pattern, lines)

total = 0
for match in matches:
    n1, n2 = match
    n1, n2 = int(n1), int(n2)
    total += n1*n2

print(total)


#######################

dostring = r"do\(\)"
dontstring = r"don't\(\)"
domatches = [match.start() for match in re.finditer(dostring, lines)]
dontmatches = [match.start() for match in re.finditer(dontstring, lines)]

newstr = ""
do_flag = True
for i,letter in enumerate(lines):
    # print(letter, i, dontmatches and i == dontmatches[0], domatches and i == domatches[0], do_flag)
    if dontmatches and i == dontmatches[0]:
        dontmatches.pop(0)
        do_flag = False

    if domatches and i == domatches[0]:
        domatches.pop(0)
        do_flag = True

    if do_flag:
        newstr+=letter

print(lines)
print(newstr)

pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
matches = re.findall(pattern, newstr)

total = 0
for match in matches:
    n1, n2 = match
    n1, n2 = int(n1), int(n2)
    total += n1*n2

print(total)