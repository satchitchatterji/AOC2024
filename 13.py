# from tqdm import tqdm 
# import numpy as np

# lines = []
# with open('13_input.txt') as f:
#     lines = f.readlines()

# situations = [[]]
# for line in lines:
#     line = line.strip()
#     if line == "":
#         situations.append([])
#         continue
#     situations[-1].append(line)

# def situation_to_tuple(situation):
#     # input: ['Button A: X+94, Y+34', 'Button B: X+22, Y+67', 'Prize: X=8400, Y=5400']
#     # output: ((94, 34), (22, 67), (8400, 5400))
#     buttons = []
#     for line in situation:
#         line = line.split(": ")[1]
#         x, y = line.split(", ")
#         x, y = int(x[2:]), int(y[2:])
#         buttons.append((x, y))
#     return tuple(buttons)

# def distance(a, b):
#     return abs(a[0] - b[0]) + abs(a[1] - b[1])

# for i, sit in enumerate(situations):
#     situations[i] = situation_to_tuple(sit)

# # def play(cur_pos, buttons, prize, n_presses):
# #     # recursive function
# #     if n_presses[0] > 50 or n_presses[1] > 50: # if we pressed either button more than 100 times
# #         return 0
    
# #     if cur_pos == prize:
# #         return 1
    
# #     # press button A
# #     new_pos = (cur_pos[0] + buttons[0][0], cur_pos[1] + buttons[0][1])
# #     n_presses[0] += 1
# #     if play(new_pos, buttons, prize, n_presses):
# #         return 1
# #     n_presses[0] -= 1

# #     # press button B
# #     new_pos = (cur_pos[0] + buttons[1][0], cur_pos[1] + buttons[1][1])
# #     n_presses[1] += 1
# #     if play(new_pos, buttons, prize, n_presses):
# #         return 1
# #     n_presses[1] -= 1

# #     return 0

# import heapq

# def heuristic(node, goal):
#     # Manhattan distance heuristic
#     return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

# def a_star(start, goal, left, right):
#     # Priority queue
#     open_list = []
#     heapq.heappush(open_list, (0, start))

#     # Store visited nodes
#     came_from = {}
#     g_score = {start: 0}

#     while open_list:
#         _, current = heapq.heappop(open_list)
#         print(current)
#         if current == goal:
#             path = []
#             while current in came_from:
#                 path.append(current)
#                 current = came_from[current]
#             path.append(start)
#             return path[::-1]

#         # Explore neighbors: move left or right
#         for dx, dy in [left, right]:
#             neighbor = (current[0] + dx, current[1] + dy)
#             tentative_g_score = g_score[current] + 1

#             if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#                 came_from[neighbor] = current
#                 g_score[neighbor] = tentative_g_score
#                 f_score = tentative_g_score + heuristic(neighbor, goal)
#                 heapq.heappush(open_list, (f_score, neighbor))

#     return None

# def brute_force(cur_pos, buttons, prize, n_presses):
#     # visited nodes
#     button1, button2 = buttons
#     visited = np.zeros((100,100))
#     prize_paths = []
#     for i in range(100):
#         for j in range(100):
#             cur_pos = (button1[0] * i + button2[0] * j, 
#                        button1[1] * i + button2[1] * j)
#             if cur_pos == prize:
#                 prize_paths.append((i, j))
#     return prize_paths

# results = []
# for sit in situations:
#     # print(sit)
#     n_presses = [0, 0]
#     new_prize = (10000000000000+sit[2][0], 10000000000000+sit[2][1])
#     n_plays = a_star((0, 0), sit[2], sit[0], sit[1])
#     print(n_plays)
#     exit()
#     # results.append(n_plays)

# button_costs = [3,1]
# min_costs = []
# for result in results:
#     if len(result) == 0:
#         continue
#     # print(result)
#     costs = []
#     for res in result:
#         costs.append(res[0] * button_costs[0] + res[1] * button_costs[1])
#     min_costs.append(min(costs))

# print(sum(min_costs))

import re
import numpy as np

def calc_for_machine(d):
    A = np.array([[int(d[0]), int(d[2])], [int(d[1]), int(d[3])]])
    y = np.array([10000000000000 + int(d[4]), 10000000000000 + int(d[5])])
    x = np.linalg.solve(A, y)

    # check if x is whole numbers and larger than 0
    x_rounded = np.round(x)
    x_is_valid = np.all(0 <= x_rounded) and np.allclose(x, x_rounded, rtol=1e-14, atol=1e-8) # need to adjust the defaults rtol=1e-9, atol=1e-5, because they were too sensitive for large values in y
    if not x_is_valid:
        return 0
    return int(np.dot(tokens_cost, x_rounded.reshape(-1, 1)).item())

# parse
file_path = '13_input.txt'
with open(file_path, 'r') as file:
    file_complete = file.read()
data = re.findall(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)', file_complete)

# run
tokens_cost = np.array([3, 1])
tokens = sum(calc_for_machine(d) for d in data)
print('Result:', tokens)