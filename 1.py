import pandas as pd

data = pd.read_csv("1_input.txt", header=None, sep="   ", engine="python")

data[0] = sorted(data[0].tolist())
data[1] = sorted(data[1].tolist())
data["dif"] = (data[0]-data[1]).abs()

print(data['dif'].sum())

left_freq = {k:int((data[0]==k).sum()) for k in data[0]}
right_freq = {k:int((data[1]==k).sum()) for k in data[1]}

sim = 0
for k in left_freq:
    if k in right_freq:
        sim += k * left_freq[k] * right_freq[k]

print(sim)
