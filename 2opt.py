#!/usr/bin/env python3

import copy

from common import format_tour
from solver_greedy import distance


def read_input(file_num):
    filename = "input_" + str(file_num) + ".csv"
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def output(tour, file_num):
    with open(f'output_{file_num}.csv', 'w') as f:
        f.write(format_tour(tour) + '\n')


def ArrayDist(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist


def SolveGreedy(cities, start_city):
    N = len(cities)
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(start_city)
    tour = [start_city]
    current_city = start_city

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def Solve2opt(tour, dist):
    # vertex num
    N = len(tour)
    # 時間制限
    count = 0
    while count < 100:
        isSwap = False
        for i in range(N - 2):
            for j in range((i + 2), N):
                if j != N - 1:
                    now_distance1 = dist[tour[i]][tour[i + 1]]
                    now_distance2 = dist[tour[j]][tour[j + 1]]
                    if_distance1 = dist[tour[i]][tour[j]]
                    if_distance2 = dist[tour[j + 1]][tour[i + 1]]
                    if (now_distance1 +
                            now_distance2) > (if_distance1 +
                                              if_distance2):
                        # swap
                        tmp = tour[i + 1:j + 1]
                        tour[i + 1:j + 1] = tmp[::-1]
                        # Flag
                        isSwap = True
        if not isSwap:
            break
        count += 1
    return tour


def TotalDist(tour, dist):
    total = 0
    for index in range(len(tour) - 1):
        total += dist[tour[index]][tour[index + 1]]
    total += dist[0][len(tour) - 1]
    return total


def UpgradeSolveGreedy(cities, dist):
    # 今回のデータでは越えることがない
    min_total = 4000000.0
    min_tour = []
    # for start_index in range(len(tour)):
    for start_index in range(1):
        tour = SolveGreedy(cities, start_index)
        Solve2opt(tour, dist)
        total = TotalDist(tour, dist)
        if min_total > total:
            min_total = total
            min_tour = tour.copy()
    return min_tour


if __name__ == '__main__':
    for num in range(6, 8):
        # Input
        cities = read_input(num)
        # Calculate
        dist = ArrayDist(cities)
        tour = UpgradeSolveGreedy(cities, dist)
        # Output
        output(tour, num)