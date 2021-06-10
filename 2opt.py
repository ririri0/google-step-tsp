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


def SolveGreedy(cities, current_city):
    N = len(cities)

    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

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
    count = 0
    while count < 100:
        isSwap = False
        for i in range(N - 2):
            for j in range((i + 2), N):
                if j == N - 1:
                    j_next = 0
                else:
                    j_next = j + 1
                now_distance1 = dist[tour[i]][tour[i + 1]]
                now_distance2 = dist[tour[j]][tour[j_next]]
                if_distance1 = dist[tour[i]][tour[j]]
                if_distance2 = dist[tour[j_next]][tour[i + 1]]
                if (now_distance1 + now_distance2) > (if_distance1 + if_distance2):
                    # swap
                    tmp = tour[i + 1:j_next]
                    tour[i + 1:j_next] = tmp[::-1]
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
    min_total = 4000000.0
    min_tour = []
    # for current_index in range(len(tour)):
    for current_index in range(1):
        tour = SolveGreedy(cities, current_index)
        Solve2opt(tour, dist)
        total = TotalDist(tour, dist)
        if min_total > total:
            min_total = total
            min_tour = tour.copy()
    return min_tour


if __name__ == '__main__':
    for num in range(1, 7):
        # Input
        cities = read_input(num)
        # Calculate
        dist = ArrayDist(cities)
        tour = UpgradeSolveGreedy(cities, dist)
        # Output
        output(tour, num)
