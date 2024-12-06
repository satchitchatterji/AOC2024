import numpy as np
from tqdm import tqdm

grid = []
with open("6_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        letters = [x for x in line.strip()]
        grid.append(letters)

grid = np.array(grid)

where_to_tuple = lambda x: (int(x[0][0]), int(x[1][0]))

guard_start = where_to_tuple(np.where(grid=="^"))

def check_left(guard_pos, grid):
    return guard_pos[0] >= len(grid) or guard_pos[0] < 0 or guard_pos[1] >= len(grid[0]) or guard_pos[1] < 0

def next_position(guard_pos, direction):
    if direction == 0: # upwards
        return guard_pos[0]-1, guard_pos[1]
    if direction == 1: # right
        return guard_pos[0], guard_pos[1]+1
    if direction == 2: # down
        return guard_pos[0]+1, guard_pos[1]
    if direction == 3: # left
        return guard_pos[0], guard_pos[1]-1

def get_guard_route(guard_position, direction, grid):
    checked = set()
    positions_checked_w_dirs = []
    loop = False
    while True:
        checked.add(guard_position)
        positions_checked_w_dirs.append((guard_position,direction))

        move_to = next_position(guard_position, direction)

        if check_left(move_to, grid):
            break
        
        if (move_to, direction) in positions_checked_w_dirs:
            loop = True
            break

        if grid[move_to[0], move_to[1]] == '#':
            direction = np.mod(direction+1, 4)
        else:
            guard_position = move_to

    return loop, checked

_, base_route = get_guard_route(guard_start, 0, grid)

loops_created = 0
for pos in tqdm(base_route):
    if pos == guard_start:
        continue
    grid_copy = grid.copy()
    grid_copy[pos[0], [pos[1]]] = "#"
    loop, _ = get_guard_route(guard_start, 0, grid_copy)
    loops_created += loop

print(loops_created)



