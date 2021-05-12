import random

import pulp
from pulp import *

sites = "Anvers Bruxelles Charleroi Gand Hasselt Liege".split()
site_count = len(sites)

vehicle_count = 4

vehicle_capacity = 50

distance = [
    # Anvers Bruxelles Charleroi Gand Hasselt Liege
    [0, 45, 100, 40, 50, 105],  # Anvers
    [45, 0, 60, 40, 50, 100],  # Bruxelles
    [100, 60, 0, 100, 80, 100],  # Charleroi
    [40, 40, 100, 0, 60, 140],  # Gand
    [50, 50, 80, 60, 0, 60],  # Hasselt
    [105, 100, 100, 140, 60, 0]  # Liege
]
distance = makeDict([sites, sites], distance, 0)

demand = [random.uniform(0, 1) * 20 for j in sites]

# solve with pulp

# definition of lpproblem instance
problem = LpProblem("CVRP", LpMinimize)

for i in range(vehicle_count):

    # definition of binary variables
    x = [[[LpVariable("x%s_%s,%s" % (i, j, k), cat="Binary") if i != j else None for k in range(vehicle_count)] for
          j in range(site_count)] for i in range(site_count)]

    # add objective function
    problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                          for k in range(vehicle_count)
                          for j in range(site_count)
                          for i in range(site_count))

    # constraints
    # only one visit per vehicle per site
    for j in range(1, site_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0
                              for i in range(site_count)
                              for k in range(vehicle_count)) == 1

    # depart from depot
    for k in range(vehicle_count):
        problem += pulp.lpSum(x[0][j][k] for j in range(1, site_count)) == 1
        problem += pulp.lpSum(x[i][0][k] for i in range(1, site_count)) == 1

    # number of vehicles coming in and out of a site is the same
    for k in range(vehicle_count):
        for j in range(site_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0
                                  for i in range(site_count)) - pulp.lpSum(
                x[j][i][k] for i in range(site_count)) == 0

    # delivery capacity of each vehicle should not exceed maximum capacity
    for k in range(vehicle_count):
        problem += pulp.lpSum(demand[j] * x[i][j][k] if i != j else 0 for i in range(site_count) for j in
                              range(1, site_count)) <= vehicle_capacity

    # removal of subtours
    subtours = []
    for i in range(2, site_count):
        subtours += itertools.combinations(range(1, site_count), i)

    for s in subtours:
        problem += pulp.lpSum(
            x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2) for k in range(vehicle_count)) <= len(
            s) - 1

    # print vehicle_count needed to solve problem
    # print calculated minimum distance value
    if problem.solve() == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Moving Distance:', pulp.value(problem.objective))
        break
