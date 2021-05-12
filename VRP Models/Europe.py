"""
A set partitioning model of a vehicle routing problem

Author: Diego Rubas 2021
"""

from pulp import *


def calc_dist(input_route):
    tot_dist = 0
    for i in range(1, len(input_route)):
        tot_dist += distances[input_route[i]][input_route[i-1]]
    return tot_dist


def perm_route(input_route):
    if len(input_route) <= 3:
        return [input_route]
    routes_list = []
    origin = [input_route[0]]
    new_route = input_route[1:-1]
    for perm in allpermutations(new_route, len(new_route)):
        if len(perm) == len(new_route):
            routes_list.append(origin + list(perm) + origin)
    return routes_list


def shortest_route(input_list):
    if len(input_list) == 1:
        return input_list[0]
    min_distance, min_route = 1000, input_list[0]
    for r in input_list:
        if calc_dist(r) < min_distance:
            min_distance = calc_dist(r)
            min_route = r
    return min_route


max_routes = 6
max_sites = 6
sites = "Anvers Bruxelles Charleroi Gand Hasselt Liege".split()

distances = [
    # Anvers Bruxelles Charleroi Gand Hasselt Liege
    [0, 45, 100, 40, 50, 105],  # Anvers
    [45, 0, 60, 40, 50, 100],  # Bruxelles
    [100, 60, 0, 100, 80, 100],  # Charleroi
    [40, 40, 100, 0, 60, 140],  # Gand
    [50, 50, 80, 60, 0, 60],  # Hasselt
    [105, 100, 100, 140, 60, 0]  # Liege
]
distances = makeDict([sites, sites], distances, 0)

# create list of all possible tables
poss_routes = [list(c) for c in allcombinations(sites, max_sites)]
acid_routes = []
base_routes = []

for route in poss_routes:
    if 'Liege' not in route:
        acid_route = ['Liege'] + route[:] + ['Liege']
        acid_routes.append(acid_route)
    elif 'Anvers' not in route:
        base_route = ['Anvers'] + route[:] + ['Anvers']
        base_routes.append(base_route)

for route in acid_routes:
    best_route = shortest_route(perm_route(route))
    print(route, calc_dist(route), best_route, calc_dist(best_route))

for route in base_routes:
    best_route = shortest_route(perm_route(route))
    print(route, calc_dist(route), best_route, calc_dist(best_route))
