import numpy as np

map = []
with open("10_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        letters = [int(x) for x in line.strip()]
        map.append(letters)

def arr_to_str_list(arr):
    str_list = []
    for row in arr:
        str_list.append("".join(row))

    return str_list

def count_trails(map, start_pos):
    # visited nodes
    visited = np.zeros(map.shape)
    # queue
    queue = [start_pos]
    # number of paths
    n_paths = 0

    while len(queue) > 0:
        cur_pos = queue.pop(0)

        # if map[cur_pos[0], cur_pos[1]] == 9 and visited[cur_pos] == 0:   # for first puzzle 
        if map[cur_pos[0], cur_pos[1]] == 9:                               # for second puzzle
            n_paths += 1

        visited[cur_pos] = 1

        for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_pos = (cur_pos[0] + direction[0], cur_pos[1] + direction[1])
            if new_pos[0] < 0 or new_pos[0] >= len(map) or new_pos[1] < 0 or new_pos[1] >= len(map[0]):
                continue
            if visited[new_pos] == 1:
                continue
            if map[new_pos] != map[cur_pos[0], cur_pos[1]] + 1:
                continue

            queue.append(new_pos)

    return n_paths

map = np.array(map)
start_positions = np.where(map == 0)
start_positions = list(zip(start_positions[0], start_positions[1]))

n_trails = []
for start_pos in start_positions:
    n_trails.append(count_trails(map, start_pos))

print(sum(n_trails))