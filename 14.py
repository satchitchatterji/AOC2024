import numpy as np
import re
import matplotlib.pyplot as plt
from tqdm import trange

map_size = (101,103)

class Robot:
    def __init__(self, init_str, map_size=(100, 100)):
        self.x = None
        self.y = None
        self.dx = None
        self.dy = None
        self.parse_init_str(init_str)
        self.map_size = map_size

    def parse_init_str(self, init_str):
        # str of form: p=0,4 v=3,-3
        p, v = init_str.split(' ')
        self.x, self.y = map(int, re.findall(r'-?\d+', p))
        self.dx, self.dy = map(int, re.findall(r'-?\d+', v))
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.x %= self.map_size[0]
        self.y %= self.map_size[1]

def final_result(robots):
    map_size = robots[0].map_size
    vertical_centerline = map_size[0] // 2
    horizontal_centerline = map_size[1] // 2
    quadrant_sums = np.zeros(4)
    for robot in robots:
        if robot.x < vertical_centerline and robot.y < horizontal_centerline:
            quadrant_sums[0] += 1
        elif robot.x < vertical_centerline and robot.y > horizontal_centerline:
            quadrant_sums[1] += 1
        elif robot.x > vertical_centerline and robot.y < horizontal_centerline:
            quadrant_sums[2] += 1
        elif robot.x > vertical_centerline and robot.y > horizontal_centerline:
            quadrant_sums[3] += 1
    return quadrant_sums


class Robots:
    def __init__(self, robots):
        self.robots = robots
        self.map_size = robots[0].map_size
        self.grid = np.zeros(self.map_size)
        self.positions = np.zeros((len(robots), 2), dtype=int)
        self.velocities = np.zeros((len(robots), 2), dtype=int)
        self.parse_robots()
    
    def parse_robots(self):
        for i, robot in enumerate(self.robots):
            self.positions[i] = [robot.x, robot.y]
            self.velocities[i] = [robot.dx, robot.dy]

    def move(self):
        self.positions += self.velocities
        self.positions %= self.map_size

    def compute_final_result(self):
        vertical_centerline = self.map_size[0] // 2
        horizontal_centerline = self.map_size[1] // 2
        quadrant_sums = np.zeros(4)
        quadrant_sums[0] = np.sum(np.logical_and(np.less(self.positions[:, 0], vertical_centerline), np.less(self.positions[:, 1], horizontal_centerline)))
        quadrant_sums[1] = np.sum(np.logical_and(np.less(self.positions[:, 0], vertical_centerline), np.greater(self.positions[:, 1], horizontal_centerline)))
        quadrant_sums[2] = np.sum(np.logical_and(np.greater(self.positions[:, 0], vertical_centerline), np.less(self.positions[:, 1], horizontal_centerline)))
        quadrant_sums[3] = np.sum(np.logical_and(np.greater(self.positions[:, 0], vertical_centerline), np.greater(self.positions[:, 1], horizontal_centerline)))
        
        return np.prod(quadrant_sums)

robots = []
with open('14.txt') as f:
    for line in f:
        robots.append(Robot(line.strip(), map_size))

robots = Robots(robots)

results = []
for i in trange(0, 10404):
    robots.move()
    results.append(robots.compute_final_result())

    grid = np.zeros(map_size)
    for x, y in robots.positions:
        grid[x, y] = 1

    plt.imshow(grid)
    plt.savefig(f'14_imgs/14_{i}.png', bbox_inches='tight')
    plt.close()

plt.plot(results)
plt.savefig('14_imgs/14_results.png', bbox_inches='tight')

# grid = np.full(map_size, '.')

# print(int(np.prod(final_result(robots))))