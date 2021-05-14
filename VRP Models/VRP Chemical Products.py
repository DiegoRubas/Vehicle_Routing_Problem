"""
A set partitioning model of a vehicle routing problem

Authors: Marie Giot, Vladimir Kozlov, Diego Rubas 2021
"""

from pulp import *


def annual_demand(input_site, input_year):
    result = annual_demand_1[input_site] if input_year < 3 else annual_demand_2[input_site]
    return result


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
    stop_time = unload_time * (len(input_route) - 1)
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


def index_to_month(input_index):
    new_index = input_index % 12
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
    return month_dict[new_index]


def index_to_year(input_index):
    return input_index // 12

max_sites = 3  # car distribution de min 5 tonnes par ville
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

truck_buy_price = 40000
truck_sell_price = truck_buy_price * (1/2)
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

# for s1 in sites:
#     for s2 in sites:
#         print("distance between {} and {} is {} and travel time is {}".format(s1, s2, distances[s1][s2], calc_time([s1, s2])))

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
years = range(5)
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (vehicle_numbers, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (vehicle_numbers, months), cat='Binary')
truck_sell = LpVariable.dicts("truck_sell", (vehicle_numbers, months), cat='Binary')
truck_acid = LpVariable.dicts("truck_acid", vehicle_numbers, cat='Binary')
truck_base = LpVariable.dicts("truck_base", vehicle_numbers, cat='Binary')
truck_hybrid = LpVariable.dicts("truck_hybrid", vehicle_numbers, cat='Binary')

truck_routes = [(v, tuple(r)) for v in vehicle_numbers for r in all_routes]

# variable indicating how many times truck takes route
truck_route_vars = LpVariable.dicts("truck_route", (truck_routes, years), 0, None, LpInteger)

# annual demand met
for y in years:
    for s in sites:
        total = 0
        factor = 1
        for t in truck_routes:
            if s in t[1][1:-1]:
                total += truck_route_vars[t][y] * (1/(len(t[1])-2)) * truck_max_cap
        prob += total >= annual_demand(s, y), "Min annual demand {} year {}". format(s, y)

for y in years:
    for t_r in truck_routes:
        if t_r[1][0] == 'Liege':
            prob += truck_route_vars[t_r][y] >= min_delivery * truck_acid[t_r[0]]
            prob += truck_route_vars[t_r][y] <= max_delivery * truck_acid[t_r[0]]
        else:
            prob += truck_route_vars[t_r][y] >= min_delivery * truck_base[t_r[0]]
            prob += truck_route_vars[t_r][y] <= max_delivery * truck_base[t_r[0]]

for y in years:
    for n in vehicle_numbers:
        prob += truck_hybrid[n] >= truck_acid[n] + truck_base[n] - 1
        prob += truck_hybrid[n] <= truck_acid[n]
        prob += truck_hybrid[n] <= truck_base[n]

for y in years:
    for n in vehicle_numbers:
        total = truck_hybrid[n] * (cleaning_time + factory_switch)
        # total = 0
        for t in truck_routes:
            if t[0] == n:
                total += truck_route_vars[t][y] * calc_time(t[1])
        prob += total <= lpSum(truck_status[n][m] * hours_in_month for m in months[y*12:(y+1)*12]), "Max truck {} hours on year {}".format(n, y)

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
        if m == len(months) - 1:
            prob += truck_sell[t][m] == truck_status[t][m]
        elif m == 0:
            prob += truck_sell[t][m] == 0
        else:
            prob += truck_sell[t][m] >= truck_status[t][m - 1] - truck_status[t][m]
            prob += truck_sell[t][m] <= 1 - truck_status[t][m]
            prob += truck_sell[t][m] <= truck_status[t][m]


maintenance_vector = [truck_status[n][m] * truck_maint_price for n in vehicle_numbers for m in months]
purchase_vector = [truck_buy[n][m] * truck_buy_price for n in vehicle_numbers for m in months]
sell_vector = [-truck_sell[n][m] * truck_sell_price for n in vehicle_numbers for m in months]
salary_vector = [truck_route_vars[tr][y] * calc_time(tr[1] * hourly_rate) for tr in truck_routes for y in years]
gas_vector = [truck_route_vars[tr][y] * calc_dist(tr[1]) * gas_rate for tr in truck_routes for y in years]

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
status = prob.solve(solver=GLPK(msg=True, keepFiles=True, options=["--tmlim", "600"]))

obj_func = 0

bought_trucks = {}
for n in vehicle_numbers:
    bought_trucks[n] = 0

for y in years:
    supply_dict = dict(annual_demand_1) if y < 3 else dict(annual_demand_2)
    for key in supply_dict.keys():
        supply_dict[key] = 0
    print("\n----------------Year {}----------------\n".format(y))
    for t in vehicle_numbers:
        rent_list, buy_list, sell_list = [], [], []
        for m in months[y * 12: (y+1) * 12]:
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
        if rent_price > 0:

            bought_trucks[t] = 1

            print("\n----------------Truck no {}----------------\n".format(t))
            t_routes = {}
            for r in all_routes:
                if truck_route_vars[(t, tuple(r))][y].varValue is not None and truck_route_vars[(t, tuple(r))][y].varValue > 0:
                    t_routes[tuple(r)] = truck_route_vars[(t, tuple(r))][y].varValue
            if truck_hybrid[t].varValue == 1:
                print("Truck delivers both products.")
            elif truck_acid[t].varValue == 1:
                print("Truck delivers only acids.")
            else:
                print("Truck delivers only bases.")
            if buy_price > 0:
                if sell_price > 0:
                    print("Bought in {} and sold in {} of year {}".format(index_to_month(buy_list.index(1)), index_to_month(sell_list.index(1)), y))
                else:
                    print("Bought in {} and kept until the end of year {}".format(index_to_month(buy_list.index(1)), y))
            else:
                if sell_price > 0:
                    print("Available from the beginning and kept until {} of year {}".format(index_to_month(sell_list.index(1)), y))
                else:
                    print("Available from the beginning and kept until the end of year {}".format(y))
            print("Total cost: {} (Purchase: {}, Sell: {}, Maintenance: {})".format(
                int(total_price), buy_price, sell_price, int(rent_price))
            )
            for route in t_routes.keys():
                total_time += calc_time(route) * t_routes[route]
                print("{} ({}-hour trip) {} times for a total of {} hours;  {} / {} hours".format(
                    route, round(calc_time(route), 2), t_routes[route], round(calc_time(route) * t_routes[route], 2), round(total_time, 2), avail_time
                ))
                for city in route[1:-1]:
                    print("Supplied {} * {} = {} to {}".format((truck_max_cap/(len(route) - 2)), t_routes[route], truck_max_cap * t_routes[route] / (len(route) - 2), city))
                    supply_dict[city] += (16.5 * t_routes[route] / (len(route) - 2))
            if truck_hybrid[t].varValue == 1:
                total_time += factory_switch + cleaning_time
                print("Additional cleaning time ({}) and travelling to other production center ({}) : {} / {} hours".format(cleaning_time, factory_switch, round(total_time, 2), avail_time))
            print("Current supply")
            for key in supply_dict:
                print("{} : {} / {}".format(key, supply_dict[key], annual_demand(key, y)))
            print("")

    print("Total supply")
    for key in supply_dict:
        print("{} : {} / {}".format(key, supply_dict[key], annual_demand(key, y)))

    print("Vehicle costs for year {} is {}.".format(y, int(obj_func)))
    total_time, total_distance = 0, 0
    for tr in truck_routes:
        total_time += truck_route_vars[tr][y].varValue * calc_time(tr[1])
        total_distance += truck_route_vars[tr][y].varValue * calc_dist(tr[1])
    print("Total pay on year {} for {} hours is {}".format(y, round(total_time, 2), round(total_time * hourly_rate, 2)))
    print("Total gas bill on year {} for {} km is {}".format(y, total_distance, round(total_distance * gas_rate, 2)))
    print("Total costs for year {} is {}".format(y, int(obj_func + total_time * hourly_rate + total_distance * gas_rate)))

for n in bought_trucks.keys():
    if bought_trucks[n] == 1:
        text = "# Truck no. {} details #".format(n)
        header = "#" * len(text)
        print("\n" + header + "\n" + text + "\n" + header + "\n")
        if truck_hybrid[n].varValue == 1:
            print("Delivers both acids and bases.")
        elif truck_acid[n].varValue == 1:
            print("Truck delivers only acids.")
        else:
            print("Truck delivers only bases.")
        buy_index, sell_index = 0, 0
        for m in months:
            if truck_buy[n][m].varValue == 1:
                buy_index = m
            if truck_sell[n][m].varValue == 1:
                sell_index = m
        if truck_status[n][0] == 1 and truck_buy[n][0].varValue == 0 and sell_index == len(months) - 1:
            print("Available from the beginning and sold at the end.")
        elif truck_status[n][0] == 1 and truck_buy[n][0].varValue == 1 and sell_index == len(months) - 1:
            print("Bought at the beginning and sold at the end.")
        elif buy_index == 0:
            print("Bought at the beginning and sold in {}, year {}.".format(index_to_month(sell_index), index_to_year(sell_index)))
        elif sell_index == len(months)-1:
            print("Bought in {}, year {} and sold at the end.".format(index_to_month(buy_index), index_to_year(buy_index)))
        else:
            print("Bought in {}, year {} and sold in {}, year {}.".format(index_to_month(buy_index), index_to_year(buy_index), index_to_month(sell_index), index_to_year(sell_index)))
        for y in years:
            print("During year {}".format(y))
            t_routes, total_time = {}, 0
            for r in all_routes:
                if truck_route_vars[(n, tuple(r))][y].varValue is not None and truck_route_vars[(n, tuple(r))][y].varValue > 0:
                    t_routes[tuple(r)] = truck_route_vars[(n, tuple(r))][y].varValue
            for r in t_routes.keys():
                for s in r[1:-1]:
                    print("Supplied {} tonnes to {}.".format(truck_max_cap * t_routes[r] / (len(r) - 2), s))

