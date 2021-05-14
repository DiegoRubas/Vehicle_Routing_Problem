"""
A set partitioning model of a vehicle routing problem

Author: Diego Rubas 2021
"""

from pulp import *


# calcule toutes les routes qui passent par les clients selon le centre de production
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


# calcule la distance par route
def calc_dist(input_route):
    tot_dist = 0
    for i in range(1, len(input_route)):
        tot_dist += distances[input_route[i]][input_route[i - 1]]
    return tot_dist


# calcule le temps d'un temps d'une route
def calc_time(input_route):
    stop_time = unload_time * (len(input_route) + 1)
    road_time = calc_dist(input_route) / truck_speed
    tot_time = stop_time + road_time
    return tot_time


# toutes les permutations d'une route (pour ensuite en prendre le plus court)
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


# renvoie la route dans l'ordre de villes plus court
def shortest_route(input_list):
    if len(input_list) == 1:
        return input_list[0]
    min_distance, min_route = 1000, input_list[0]
    for r in input_list:
        if calc_dist(r) < min_distance:
            min_distance = calc_dist(r)
            min_route = r
    return min_route


max_sites = 5  # car distribution de min 5 tonnes par ville
sites = "Anvers Bruxelles Charleroi Gand Hasselt Liege".split()

acid_depot = "Liege"
base_depot = "Anvers"

acid_clients = "Anvers Bruxelles Charleroi Gand Hasselt".split()
base_clients = ["Liege"]

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
hourly_rate = 20
gas_rate = 0.10
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

factory_switch = distances['Liege']['Anvers'] / truck_speed

# create lists of all possible routes
poss_routes = [list(c) for c in allcombinations(sites, max_sites)]
acid_routes = calc_routes(acid_depot)
base_routes = calc_routes(base_depot)
all_routes = acid_routes + base_routes

max_delivery = truck_max_cap * hours_in_month / calc_time(shortest_route(all_routes))
min_delivery = 0

prob = LpProblem("Chemical_Products_VRP", LpMinimize)

vehicle_numbers = range(15)
years = range(1)
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (vehicle_numbers, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (vehicle_numbers, months), cat='Binary')
truck_sell = LpVariable.dicts("truck_sell", (vehicle_numbers, months), cat='Binary')
truck_acid = LpVariable.dicts("truck_acid", vehicle_numbers, cat='Binary')
truck_base = LpVariable.dicts("truck_base", vehicle_numbers, cat='Binary')
truck_hybrid = LpVariable.dicts("truck_hybrid", vehicle_numbers, cat='Binary')

truck_routes = [(v, tuple(r)) for v in vehicle_numbers for r in all_routes]

# variable indicating how many times truck takes route
truck_route_vars = LpVariable.dicts("truck_route", truck_routes, 0, None, LpInteger)
# truck_route_bin = LpVariable.dicts("truck_route_bin", truck_routes, 0, None, LpBinary)

# annual demand met
for site in sites:
    total = 0
    factor = 1
    for t in truck_routes:
        if site in t[1][1:-1]:
            total += truck_route_vars[t] * (1/(len(t[1])-2)) * truck_max_cap
    prob += total <= annual_demand_1[site], "Max annual demand {}". format(site)
    prob += total >= annual_demand_1[site] - 10, "Min annual demand {}". format(site)

for t_r in truck_routes:
    if t_r[1][0] == 'Liege':
        prob += truck_route_vars[t_r] >= min_delivery * truck_acid[t_r[0]]
        prob += truck_route_vars[t_r] <= max_delivery * truck_acid[t_r[0]]
    else:
        prob += truck_route_vars[t_r] >= min_delivery * truck_base[t_r[0]]
        prob += truck_route_vars[t_r] <= max_delivery * truck_base[t_r[0]]

for n in vehicle_numbers:
    prob += truck_hybrid[n] >= truck_acid[n] + truck_base[n] - 1
    prob += truck_hybrid[n] <= truck_acid[n]
    prob += truck_hybrid[n] <= truck_base[n]

grand_total, post_pulp_margin = 0, 100

for n in vehicle_numbers:
    total = truck_hybrid[n] * (cleaning_time + factory_switch)
    # total = 0
    for t in truck_routes:
        if t[0] == n:
            total += truck_route_vars[t] * calc_time(t[1])
    grand_total += total
    prob += total <= lpSum(truck_status[n][m] * hours_in_month for m in range(12)), "Max truck {} hours".format(n)

grand_total += post_pulp_margin
prob += grand_total <= lpSum(truck_status[n][m] * hours_in_month for m in range(12) for n in vehicle_numbers)

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


maintenance_vector = [(truck_status[n][m] * truck_maint_price for n in vehicle_numbers for m in months)]
purchase_vector = [truck_buy[n][m] * truck_buy_price for n in vehicle_numbers for m in months]
sell_vector = [-truck_sell[n][m] * truck_sell_price for n in vehicle_numbers for m in months]
salary_vector = [truck_route_vars[tr] * calc_time(tr[1] * hourly_rate) for tr in truck_routes]
gas_vector = [truck_route_vars[tr] * calc_dist(tr[1]) * gas_rate
              for tr in truck_routes]

prob += lpSum(
    salary_vector
    +
    gas_vector
    +
    maintenance_vector
    +
    purchase_vector
    +
    sell_vector
), "Total cost"

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
        print("truck delivers both products : {}".format(truck_hybrid[t].varValue == 1))
        if buy_price > 0:
            if sell_price > 0:
                print("Bought in {} and sold in {}".format(month_dict[buy_list.index(1)], month_dict[sell_list.index(1)]))
            else:
                print("Bought in {} and kept until the end".format(month_dict[buy_list.index(1)]))
        else:
            if sell_price > 0:
                print("Available from the beginning and kept until {}".format(month_dict[sell_list.index(1)]))
            else:
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
                print("supplied {} * {} = {} to {}".format((truck_max_cap/(len(route) - 2)), t_routes[route], truck_max_cap * t_routes[route] / (len(route) - 2), city))
                supply_dict[city] += (16.5 * t_routes[route] / (len(route) - 2))
        if truck_hybrid[t].varValue == 1:
            total_time += factory_switch + cleaning_time
            print("additional cleaning time ({}) and travelling to other production center ({}) : {} / {} hours".format(cleaning_time, factory_switch, round(total_time, 2), avail_time))
        print("current supply")
        for key in supply_dict:
            print("{} : {} / {}".format(key, supply_dict[key], annual_demand_1[key]))
        print("")

print("total supply")
for key in supply_dict:
    print("{} : {} / {}".format(key, supply_dict[key], annual_demand_1[key]))

print("total cost is {}.".format(int(obj_func)))
total_time, total_distance = 0, 0
for tr in truck_routes:
    total_time += truck_route_vars[tr].varValue * calc_time(tr[1])
    total_distance += truck_route_vars[tr].varValue * calc_dist(tr[1])
print("total pay for {} hours is {}".format(round(total_time, 2), round(total_time * hourly_rate, 2)))
print("total gas bill for {} km is {}".format(total_distance, round(total_distance * gas_rate, 2)))
print("grand total price is {}".format(int(obj_func + total_time * hourly_rate + total_distance * gas_rate)))

annual_demand_rest = dict(annual_demand_1)
for key in annual_demand_rest:
    annual_demand_rest[key] -= supply_dict[key]
    annual_demand_rest[key] = round(annual_demand_rest[key], 2)
print(annual_demand_rest)

rest_acid_routes = [tuple(r) for r in acid_routes]
rest_combos = [tuple(c) for c in allcombinations(rest_acid_routes, 5)]
rest_valid_combos = []

for combo in rest_combos:
    a, b, c, g, h, min_delivery, max_delivery = 0, 0, 0, 0, 0, 1000, 0
    for r in combo:
        current_delivery = 0
        temp_list = r[1:-1]
        a += temp_list.count('Anvers')
        b += temp_list.count('Bruxelles')
        c += temp_list.count('Charleroi')
        g += temp_list.count('Gand')
        h += temp_list.count('Hasselt')
        for s in temp_list:
            current_delivery += annual_demand_rest[s]
        if current_delivery > max_delivery:
            max_delivery = current_delivery
        if current_delivery < min_delivery:
            min_delivery = current_delivery
    if a == b == c == g == h == 1 and max_delivery <= 16.5 and min_delivery >= 5:
        rest_valid_combos.append(combo)

best_acid_combo, best_acid_time = 0, 100
for combo in rest_valid_combos:
    total_time = 0
    for r in combo:
        total_time += calc_time(r)
    if total_time < best_acid_time:
        best_acid_combo = combo
        best_acid_time = total_time

best_base_combo = ('Anvers', 'Liege', 'Anvers')
best_base_time = calc_time(best_base_combo[0])

total_extra_time = best_acid_time + best_base_time + cleaning_time + factory_switch
total_extra_combo = [best_base_combo]
for combo in best_acid_combo:
    total_extra_combo.append(combo)

print(total_extra_combo, round(total_extra_time, 2), "hours")
