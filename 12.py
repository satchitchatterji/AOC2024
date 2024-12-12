import numpy as np
from itertools import permutations

# Part 1: 
# Treat regions as graphs of connected components
# Areas are the number of nodes in each graph
# Perimeters are the 4 - len(node.neighbors) for each node in the graph

map = []
with open("12_input.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        letters = [x for x in line.strip()]
        map.append(letters)
map = np.array(map, dtype=object)

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.neighbors = []
        self.visited = False
        self.group = None

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def __str__(self):
        return f"Node({self.x}, {self.y}, {self.value})"

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.value})"

map = np.pad(map, 1, mode='constant', constant_values=' ')

for i in range(len(map)):
    for j in range(len(map[i])):
        map[i][j] = Node(i, j, map[i][j])

groups = [] # groups of connected nodes by value
for i in range(len(map)):
    for j in range(len(map[i])):
        node = map[i][j]
        if node.visited:
            continue

        group = []
        queue = [node]
        while len(queue) > 0:
            cur_node = queue.pop(0)
            if cur_node.visited:
                continue
            cur_node.visited = True
            group.append(cur_node)

            for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
                new_x = cur_node.x + direction[0]
                new_y = cur_node.y + direction[1]
                if new_x < 0 or new_x >= len(map) or new_y < 0 or new_y >= len(map[0]):
                    continue
                if map[new_x][new_y].value != cur_node.value:
                    continue

                queue.append(map[new_x][new_y])

        groups.append(group)

for group_idx, group in enumerate(groups):
    for node in group:
        node.group = group_idx

# add neighbors
for group in groups:
    for node in group:
        for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
            new_x = node.x + direction[0]
            new_y = node.y + direction[1]
            if new_x < 0 or new_x >= len(map) or new_y < 0 or new_y >= len(map[0]):
                continue

            for neighbor in group:
                if neighbor.x == new_x and neighbor.y == new_y:
                    node.add_neighbor(neighbor)
                    break

areas = []
perimeters = []
for group in groups:
    areas.append(len(group))
    perimeter = 0
    for node in group:
        perimeter += 4 - len(node.neighbors)

    perimeters.append(perimeter)

print(sum([area * perimeter for area, perimeter in zip(areas[1:], perimeters[1:])]))


# Part 2: 
# Areas are the number of nodes in each graph (same as above)
# Number of sides of each group is the number of corners of each group
#        which are pattern matched against the 5 possible corner patterns

# types of corners:
# A A  |  A A  |  A B  |  A B  |  A B
# A B  |  B C  |  C D  |  B A  |  C A
# flattened: 
# AAAB |  AABC | ABCD  | ABBA  | ABCA
# [x] if AAAB, corners += 1 for A and B
# [x] if ABCD, corners += 1 for A, B, C and D
# [x] if ABBA, corners += 2 for A and B
# [x] if AABC, corners += 1 for B and C                         # first case
# [x] if ABCA, corners += 1 for B and C and corners += 2 for A  # second case

def get_rotations(window):
    rotations = []
    for rotation in range(4):
        rotations.append(window)
        window = np.rot90(window)
        for flip in [True, False]:
            if flip:
                rotations.append(np.flip(window, axis=0))
            else:
                rotations.append(window)

    return [list(rotations.flatten()) for rotations in rotations]

def generate_2D_windows_no_corners(group1, group2):
    base_window = np.array([[group1,group1], [group2,group2]])
    return get_rotations(base_window)

def generate_2D_windows_2_corners(group1, group2):
    base_window = np.array([[group1,group2], [group2,group1]])
    return get_rotations(base_window)

def generate_2D_windows_3_groups_case_1(group1, group2, group3):
    base_window = np.array([[group1,group1], [group2,group3]])
    return get_rotations(base_window)

def generate_2D_windows_3_groups_case_2(group1, group2, group3):
    base_window = np.array([[group1,group2], [group3,group1]])
    return get_rotations(base_window)

corners_of_groups = {g_idx:0 for g_idx in range(len(groups))}

for i in range(len(map)-1):
    for j in range(len(map[i])-1):
        window = map[i:i+2, j:j+2].flatten()
        window_groups = [node.group for node in window]
        
        groups_in_window = list(set(window_groups))

        if len(groups_in_window) == 1:
            # if AAAA, continue
            continue

        elif len(groups_in_window) == 4:
            # if ABCD, corners += 1 for A, B, C and D
            corners_of_groups[groups_in_window[0]] += 1
            corners_of_groups[groups_in_window[1]] += 1
            corners_of_groups[groups_in_window[2]] += 1
            corners_of_groups[groups_in_window[3]] += 1
            continue

        elif len(set(groups_in_window)) == 2:
            # if AABB or BBAA, continue
            if window_groups in generate_2D_windows_no_corners(groups_in_window[0], groups_in_window[1]):
                continue
            # if ABBA or BAAB, corners += 2 for A and B
            elif window_groups in generate_2D_windows_2_corners(groups_in_window[0], groups_in_window[1]):
                corners_of_groups[groups_in_window[0]] += 2
                corners_of_groups[groups_in_window[1]] += 2
                continue
            # if AAAB or BBBA, corners += 1 for A and B
            else: 
                corners_of_groups[groups_in_window[0]] += 1
                corners_of_groups[groups_in_window[1]] += 1
                continue

        elif len(groups_in_window) == 3:
            for permutation in permutations(groups_in_window):
                g1, g2, g3 = permutation
                if window_groups in generate_2D_windows_3_groups_case_1(*permutation):
                    # if AABC, corners += 1 for B and C
                    corners_of_groups[g2] += 1
                    corners_of_groups[g3] += 1
                    break
                elif window_groups in generate_2D_windows_3_groups_case_2(*permutation):
                    # if ABCA, corners += 1 for B and C and corners += 2 for A
                    corners_of_groups[g1] += 2
                    corners_of_groups[g2] += 1
                    corners_of_groups[g3] += 1
                    break

print(sum([area * corner for area, corner in zip(areas[1:], list(corners_of_groups.values())[1:])]))