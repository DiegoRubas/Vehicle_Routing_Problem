"""
A set partitioning model of a vehicle routing problem

Authors: Marie Giot, Vladimir Kozlov, Diego Rubas 2021
"""

from pulp import *


def annual_demand(input_site, input_year):
    result = annual_demand_1[input_site] if input_year < 3 else annual_demand_2[input_site]
    return result


def calc_routes(input_depot):
    if input_depot == acid_depot:
        return_routes = []
        for r in poss_routes:
            if input_depot not in r:
                new_r = [input_depot] + r[:] + [input_depot]
                return_routes.append(shortest_route(perm_route(new_r)))
    else:
        return_routes = [['Anvers', 'Liege', 'Anvers']]
    return return_routes


def calc_dist(input_route):
    tot_dist = 0
    for i in range(1, len(input_route)):
        tot_dist += distances[input_route[i]][input_route[i - 1]]
    return tot_dist


def calc_time(input_route):
    stop_time = unload_time * (len(input_route) - 1)
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

max_sites = 3
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

factory_switch = distances['Liege']['Anvers'] / truck_speed

# create lists of all possible routes
poss_routes = [list(c) for c in allcombinations(sites, max_sites)]
acid_routes = calc_routes(acid_depot)
base_routes = calc_routes(base_depot)
all_routes = acid_routes + base_routes

max_yearly_trips = (hours_in_month / calc_time(shortest_route(all_routes))) * 12
min_yearly_trips = 0

prob = LpProblem("Chemical_Products_VRP", LpMinimize)

vehicle_numbers = range(20)
init_trucks = 10
years = range(5)
time_limit = 5 if len(years) == 1 else 1800
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (vehicle_numbers, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (vehicle_numbers, months), cat='Binary')
truck_sell = LpVariable.dicts("truck_sell", (vehicle_numbers, months), cat='Binary')
truck_acid = LpVariable.dicts("truck_acid", vehicle_numbers, cat='Binary')
truck_base = LpVariable.dicts("truck_base", vehicle_numbers, cat='Binary')
truck_hybrid = LpVariable.dicts("truck_hybrid", vehicle_numbers, cat='Binary')

truck_routes = [(v, tuple(r)) for v in vehicle_numbers for r in all_routes]

truck_route_vars = LpVariable.dicts("truck_route", (truck_routes, years), 0, None, LpInteger)

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
            prob += truck_route_vars[t_r][y] >= min_yearly_trips * truck_acid[t_r[0]]
            prob += truck_route_vars[t_r][y] <= max_yearly_trips * truck_acid[t_r[0]]
        else:
            prob += truck_route_vars[t_r][y] >= min_yearly_trips * truck_base[t_r[0]]
            prob += truck_route_vars[t_r][y] <= max_yearly_trips * truck_base[t_r[0]]

for y in years:
    for n in vehicle_numbers:
        prob += truck_hybrid[n] >= truck_acid[n] + truck_base[n] - 1
        prob += truck_hybrid[n] <= truck_acid[n]
        prob += truck_hybrid[n] <= truck_base[n]

for y in years:
    for n in vehicle_numbers:
        total = truck_hybrid[n] * (cleaning_time + factory_switch)
        for t in truck_routes:
            if t[0] == n:
                total += truck_route_vars[t][y] * calc_time(t[1])
        prob += total <= lpSum(truck_status[n][m] * hours_in_month for m in months[y*12:(y+1)*12]), "Max truck {} hours on year {}".format(n, y)

for m in months:
    for t in vehicle_numbers:
        if m == 0 and t not in range(init_trucks):
            prob += truck_buy[t][m] == truck_status[t][m]
        elif m == 0 and t in range(init_trucks):
            prob += truck_status[t][m] == 1
            prob += truck_buy[t][m] == 0
        else:
            prob += truck_buy[t][m] >= truck_status[t][m] - truck_status[t][m - 1]
            prob += truck_buy[t][m] <= 1 - truck_status[t][m - 1]
            prob += truck_buy[t][m] <= truck_status[t][m]

for m in months:
    for t in vehicle_numbers:
        if m == 0:
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
status = prob.solve(solver=GLPK(msg=True, keepFiles=True, options=["--tmlim", "{}".format(time_limit)]))

bought_trucks = {}
for n in vehicle_numbers:
    bought_trucks[n] = 0

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
        buy_index, sell_index = 0, len(months)-1
        truck_list = [truck_status[n][i].varValue for i in months]
        for m in months:
            if truck_buy[n][m].varValue == 1:
                buy_index = m
            if truck_sell[n][m].varValue == 1:
                sell_index = m
        index1, index2 = truck_list.index(1), len(months)
        for m in months[1:]:
            if truck_list[m] == 0 and truck_list[m-1] == 1:
                index2 = m
        print("Available from {} of year {} till {} of year {}.".format(index_to_month(index1), index_to_year(index1), index_to_month(index2), index_to_year(index2)))
        for y in years:
            truck_status_list = truck_list[y*12:(y+1)*12]
            if truck_status_list.count(1) > 0:
                print("During year {}".format(y))
                routes, t_routes, total_time = [], [], 0
                for i in range(len(all_routes)):
                    r = tuple(all_routes[i])
                    if truck_route_vars[(n, tuple(r))][y].varValue is not None and truck_route_vars[(n, tuple(r))][y].varValue > 0:
                        routes.append(r)
                        t_routes.append(truck_route_vars[(n, tuple(r))][y].varValue)
                trips_per_month = []
                for i in range(y*12, (y+1)*12):
                    if truck_status[n][i].varValue == 1:
                        trips_per_month.append([])
                remaining_trips = [truck_route_vars[n, routes[k]][y].varValue for k in range(len(routes))]
                routes_b = list(routes)
                for i in range(1, len(routes_b)):
                    if routes[i][0] != routes[i-1][0]:
                        extra_route = (routes_b[i-1][0], routes_b[i][0])
                        routes_b.insert(i, extra_route)
                        remaining_trips.insert(i, 1)
                i, j, k = truck_status_list.index(1), 0, 0
                total1, total2 = 0, truck_status_list.count(1) * hours_in_month
                while i < truck_status_list.index(1) + truck_status_list.count(1) and j < len(routes_b):
                    available_hours = hours_in_month + 2.5
                    no_trips = 0
                    trip_time = calc_time(routes_b[j])
                    while j < len(routes_b) and trip_time <= available_hours and no_trips < remaining_trips[j]:
                        no_trips += 1
                        trip_time = calc_time(routes_b[j])
                        if routes_b[j] in [['Anvers', 'Liege'], ['Liege', 'Anvers']]:
                            trip_time += cleaning_time
                        available_hours -= trip_time
                        if no_trips == remaining_trips[j] or trip_time > available_hours:
                            if len(routes_b[j]) == 2:
                                print("[{} hours] Cleaning time and travel from {} factory to {} factory in {}".format(round(no_trips * trip_time, 2), routes[j][0], routes[j][1], index_to_month(i)))
                            else:
                                product = "Acid" if routes_b[j][0] == 'Liege' else "Base"
                                print("[{} hours] {}: {} {} times in {}".format(round(no_trips * trip_time, 2), product, routes_b[j], no_trips, index_to_month(i)))
                            trips_per_month[k].append([(routes_b[j], no_trips)])
                            total1 += no_trips * trip_time
                            remaining_trips[j] -= no_trips
                            no_trips = 0
                            if remaining_trips[j] == 0:
                                j += 1
                    i += 1
                    k += 1
                i = truck_status_list.index(1)
                for i in range(len(t_routes)):
                    r, t = routes[i], t_routes[i]
                    p = "acid" if r[0] == "Liege" else "base"
                    pl = 's' if t > 3 else ''
                    if i > 0:
                        r2 = routes[i-1]
                        if (r[0] == "Anvers" and r2[0] == "Liege") or (r[0] == "Liege" and r2[0] == "Anvers"):
                            print("Stops for cleaning time and travels to from {} to {}.".format(r2[0], r[0]))
                    if len(r) == 3:
                        print("Makes {} round trip{} ({} hours per trip) from {} to {}, supplying {} tonnes of {}.".format(
                            t, pl, round(calc_time(r), 2), r[0], r[1], truck_max_cap * t / (len(r) - 2), p)
                        )
                    elif len(r) == 4:
                        print("Makes {} round trip{} ({} hours per trip) from {} to {} and {}, supplying {} tonnes of {} to each.".format(
                            t, pl, round(calc_time(r)),  r[0], r[1], r[2], truck_max_cap * t / (len(r) - 2), p)
                        )
                    else:
                        print("Makes {} round trip{} ({} hours per trip) from {} to {}, {}, and {}, supplying {} tonnes of {} to each.".format(
                            t, pl, round(calc_time(r)),  r[0], r[1], r[2], r[3], truck_max_cap * t / (len(r) - 2), p)
                        )