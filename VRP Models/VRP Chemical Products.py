"""
A set partitioning model of a vehicle routing problem

Author: Diego Rubas 2021
"""

from pulp import *


def calc_routes(input_depot):
    if input_depot == acid_depot:
        routes = []
        for r in poss_routes:
            if input_depot not in r:
                new_r = [input_depot] + r[:] + [input_depot]
                routes.append(shortest_route(perm_route(new_r)))
    else:
        routes = [['Anvers', 'Liege', 'Anvers']]
    return routes


def calc_dist(input_route):
    tot_dist = 0
    for i in range(1, len(input_route)):
        tot_dist += distances[input_route[i]][input_route[i - 1]]
    return tot_dist


def calc_time(input_route):
    stop_time = unloading_time * (len(input_route) + 1)
    road_time = calc_dist(input_route) / truck_speed
    tot_time = stop_time + road_time
    return tot_time


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
max_sites = 3
sites = "Anvers Bruxelles Charleroi Gand Hasselt Liege".split()

acid_depot = "Liege"
base_depot = "Anvers"

acid_clients = ["Liege"]
base_clients = "Anvers Bruxelles Charleroi Gand Hasselt".split()

annual_acid_demand = {"Liege": 30000}
annual_base_demand_1 = {"Anvers": 9000,
                        "Bruxelles": 6200,
                        "Charleroi": 12000,
                        "Gand": 2000,
                        "Hasselt": 350}
annual_base_demand_2 = {"Anvers": 9000,
                        "Bruxelles": 6200,
                        "Charleroi": 12000,
                        "Gand": 2000,
                        "Hasselt": 1300}
annual_demand_1 = {**annual_acid_demand, **annual_base_demand_1}
annual_demand_2 = {**annual_acid_demand, **annual_base_demand_2}

annual_demand = {"Liege": 30000,
                 "Anvers": 9000,
                 "Bruxelles": 6200,
                 "Charleroi": 12000,
                 "Gand": 2000,
                 "Hasselt": 350}

truck_price = 40000
truck_max_capacity = 16.5
truck_min_capacity = 5
truck_speed = 70
unloading_time = 1
weeks_per_month = 4
days_per_week = 5
hours_per_day = 8
hours_in_month = weeks_per_month * days_per_week * hours_per_day
cleaning_time = 3 * hours_per_day

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

# create lists of all possible routes
poss_routes = [list(c) for c in allcombinations(sites, max_sites)]
acid_routes = calc_routes(acid_depot)
base_routes = calc_routes(base_depot)
all_routes = acid_routes + base_routes

#time constants and variable
"""truck_no = range(15)
years = range(2)
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (truck_no, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (truck_no, months), 0, 1, LpInteger)
truck_sell = LpVariable.dicts("truck_sell", (truck_no, months), 0, 1, LpInteger)
"""
# for route in all_routes:
#     print(route)
#
# print(len(all_routes))

vehicle_numbers = range(2)

truck_routes = [(v, tuple(r)) for v in vehicle_numbers for r in all_routes]
# for i in truck_routes:
#     print(i)

# variable indicating if truck takes route
truck_route_vars = LpVariable.dicts("truck_route", truck_routes, 0, None, LpContinuous)

"""
# distribution among sites on a route
combos = [(t, s) for t in truck_routes for s in t[1][1:-1]]
dist_vars = LpVariable.dicts("route_site_proportion", combos, 0, None, LpContinuous)"""

prob = LpProblem("Chemical_Products_VRP", LpMinimize)

# annual demand met
for site in sites:
    total = 0
    for t in truck_routes:
        if site in t[1][1:-1]:
            total += truck_route_vars[t] * (1/(len(t[1])-2)) * truck_max_capacity
    prob += total == annual_demand[site]

"""
for n in vehicle_numbers :
    # todo: add washing time for trucks delivering acids and bases
    # todo: add travel time for trucks going from the base factory to the acid factory and vice versa
    for y in years:
        acid_hours = lpSum([route_info_vars[n][(a_f, a_c)][y] * round_trip_time(a_f, a_c)
                            for a_f in acid_factories for a_c in acid_clients])
        base_hours = lpSum([route_info_vars[n][(b_f, b_c)][y] * round_trip_time(b_f, b_c)
                           for b_f in base_factories for b_c in base_clients])
        prob += lpSum(truck_status[n][m] * hours_in_month for m in range(y * 12, (y + 1) * 12)) >= \
                acid_hours + base_hours, \
                "Truck {} time check during year {}".format(n, y)

#contraintes pour le nombre de mois 
for m in months:  # remplit la truck_buy list selon la truck_status list
    for t in truck_no:
        if m == 0 and t not in range(5):  # if first month and not in the first 5 trucks
            prob += truck_buy[t][m] == truck_status[t][m]  # status is bought if it's available
            # status is nothing if it's not available
        elif m == 0 and t in range(5):  # if first month and in the first 5 trucks
            prob += truck_status[t][m] == 1
            prob += truck_buy[t][m] == 0
        else:
            prob += truck_buy[t][m] >= truck_status[t][m] - truck_status[t][m - 1]
            prob += truck_buy[t][m] <= 1 - truck_status[t][m - 1]
            prob += truck_buy[t][m] <= truck_status[t][m]

for m in months:  # fills the truck_sell list using the truck_status list
    for t in truck_no:
        if m == 0:
            prob += truck_sell[t][m] == 0
        else:
            prob += truck_sell[t][m] >= truck_status[t][m - 1] - truck_status[t][m]
            prob += truck_sell[t][m] <= 1 - truck_status[t][m]
            prob += truck_sell[t][m] <= truck_status[t][m]
            
"""

prob.writeLP("Chemical_Products_VRP.lp")
status = prob.solve(solver=GLPK(msg=True, keepFiles=True, options=["--tmlim", "10"]))

for i in truck_routes:
    if truck_route_vars[i].varValue is not None and truck_route_vars[i].varValue > 0:
        print("Truck number {} goes on the route {} {} times.".format(i[0], i[1], truck_route_vars[i].varValue))