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
    stop_time = unload_time * (len(input_route) + 1)
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
max_sites = 6
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

annual_demand_1_whole = {}
annual_demand_1_rest = {}

annual_demand_2_whole = {}
annual_demand_2_rest = {}

for key in annual_demand_1.keys():
    annual_demand_1_whole[key] = (annual_demand_1[key] // 16.5) * 16.5
    annual_demand_2_whole[key] = (annual_demand_2[key] // 16.5) * 16.5
    annual_demand_1_rest[key] = annual_demand_1[key] % 16.5
    annual_demand_2_rest[key] = annual_demand_2[key] % 16.5

month_dict = {
    0: "January",
    1: "February",
    2: "March",
    3: "April",
    4: "May",
    5: "June",
    6: "July",
    7: "August",
    8: "September",
    9: "October",
    10: "November",
    11: "December"
}

truck_buy_price = 40000
truck_sell_price = 20000
truck_maint_price = 166.67
truck_max_cap = 16.5
truck_min_cap = 5
truck_speed = 70
unload_time = 1
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
print(all_routes)

prob = LpProblem("Chemical_Products_VRP", LpMinimize)

vehicle_numbers = range(20)
years = range(1)
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (vehicle_numbers, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (vehicle_numbers, months), cat='Binary')
truck_sell = LpVariable.dicts("truck_sell", (vehicle_numbers, months), cat='Binary')
truck_type = LpVariable.dicts("truck_type", (vehicle_numbers, months), cat='Binary')
truck_hybrid = LpVariable.dicts("truck_hybrid", vehicle_numbers, cat='Binary')

truck_routes = [(v, tuple(r)) for v in vehicle_numbers for r in all_routes]

# variable indicating how many times truck takes route
truck_route_vars = LpVariable.dicts("truck_route", truck_routes, 0, None, LpInteger)

# annual demand met
for site in sites:
    total = 0
    for t in truck_routes:
        if site in t[1][1:-1]:
            total += truck_route_vars[t] * (1/(len(t[1])-2)) * truck_max_cap
    prob += total >= annual_demand_1_whole[site]

for n in vehicle_numbers:
    # todo: add washing time for trucks delivering acids and bases
    # todo: add travel time for trucks going from the base factory to the acid factory and vice versa
    total = 0
    for t in truck_routes:
        if t[0] == n:
            total += truck_route_vars[t] * calc_time(t[1])
            # total += truck_hybrid[n] * (cleaning_time + calc_time(['Anvers', 'Liege']))
    prob += total <= lpSum(truck_status[n][m] * hours_in_month for m in range(12))

# for n in vehicle_numbers:
#     for t in truck_routes:

for m in months:  # remplit la truck_buy list selon la truck_status list
    for t in vehicle_numbers:
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
    for t in vehicle_numbers:
        if m == 0:
            prob += truck_sell[t][m] == 0
        else:
            prob += truck_sell[t][m] >= truck_status[t][m - 1] - truck_status[t][m]
            prob += truck_sell[t][m] <= 1 - truck_status[t][m]
            prob += truck_sell[t][m] <= truck_status[t][m]


prob.writeLP("Chemical_Products_VRP.lp")
status = prob.solve(solver=GLPK(msg=True, keepFiles=True, options=["--tmlim", "60"]))

obj_func = 0
supply_dict = dict(annual_demand_1)
for key in supply_dict.keys():
    supply_dict[key] = 0

for t in vehicle_numbers:
    rent_list, buy_list, sell_list = [], [], []
    for m in months:
        rent_list.append(truck_status[t][m].varValue)
        buy_list.append(truck_buy[t][m].varValue)
        sell_list.append(truck_sell[t][m].varValue)
    buy_price = buy_list.count(1) * truck_buy_price
    sell_price = sell_list.count(1) * truck_sell_price
    rent_price = rent_list.count(1) * truck_maint_price
    total_price = buy_price + rent_price - sell_price
    avail_time = rent_list.count(1) * hours_in_month
    total_time = 0
    obj_func += total_price
    if total_price > 0:
        t_routes = {}
        for t_r in truck_routes:
            if t_r[0] == t and truck_route_vars[t_r].varValue is not None and truck_route_vars[t_r].varValue > 0:
                t_routes[t_r[1]] = truck_route_vars[t_r].varValue
        print("Truck number {}".format(t + 1))
        if buy_price > 0 and sell_price > 0:
            print("Bought in {} and sold in {}".format(month_dict[buy_list.index(1)], month_dict[sell_list.index(1)]))
        elif buy_price > 0 and sell_price == 0:
            print("Bought in {} and kept until the end".format(month_dict[buy_list.index(1)]))
        elif buy_price == 0 and sell_price > 0:
            print("Available from the beginning and kept until {}".format(month_dict[sell_list.index(1)]))
        elif buy_price == 0 and sell_price == 0:
            print("Available from the beginning and kept until the end")
        print("Total cost: {} (purchase: {}, sell: -{}, rent: {})".format(
            int(total_price), buy_price, sell_price, int(rent_price))
        )
        for route in t_routes.keys():
            total_time += calc_time(route) * t_routes[route]
            print("{} {} times for {} hours;  {} / {} hours".format(
                route, t_routes[route], round(calc_time(route) * t_routes[route], 2), round(total_time, 2), avail_time
            ))
            for city in route[1:-1]:
                print("supplied {} to {}".format((16.5 * t_routes[route] / (len(route) - 2)), city))
                supply_dict[city] += (16.5 * t_routes[route] / (len(route) - 2))
        print("current supply")
        for key in supply_dict:
            print("{} : {} / {}".format(key, supply_dict[key], annual_demand_1[key]))
        print("")

print("total supply")
for key in supply_dict:
    print("{} : {} / {}".format(key, supply_dict[key], annual_demand_1_whole[key]))

print("total cost is {}.".format(int(obj_func)))
