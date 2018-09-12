# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import numpy
from heapq import *


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def count_neighbours(array, x, y, width, height):
    count = 0
    i = -1
    while i < 2:
        j = -1
        while j < 2:
            n_x = x+i
            n_y = y+j
            if i == 0 and j == 0:
                pass
            elif n_x < 0 or n_y < 0 or n_x >= width or n_y >= height:
                count += 1
            elif width > n_x >= 0 and height > n_y >= 0 and array[n_y][n_x] == 1:
                count += 1
            j += 1
        i += 1
    return count

def a_star(array, start, goal):
    array = numpy.array(array)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    print(start)

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            nb_nei = count_neighbours(array, neighbor[0], neighbor[1], array.shape[0], array.shape[1])
            if 0 < nb_nei < 3:
                continue
            if 0 <= neighbor[0] < array.shape[1]:
                if 0 <= neighbor[1] < array.shape[0]:
                    if array[neighbor[1]][neighbor[0]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

    return False