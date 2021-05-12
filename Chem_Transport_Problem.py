from pulp import *
from math import ceil, floor


def min_trips(city, year):
    if year < 3:
        result = ceil(annual_demand_1[city] / truck_max_capacity)
    else:
        result = ceil(annual_demand_2[city] / truck_max_capacity)
    return result


def round_trip_time(city_1, city_2):
    travel_time = distances[city_1][city_2] / truck_speed
    delivery_time = travel_time + unloading_time
    total_time = delivery_time * 2
    return total_time


Cities = "Anvers Bruxelles Charleroi Gand Hasselt Liege".split()

acid_factories = ["Anvers"]
base_factories = ["Liege"]

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
distances = makeDict([Cities, Cities], distances, 0)

truck_no = range(15)
years = range(2)
months = range(len(years) * 12)
truck_status = LpVariable.dicts("truck_status", (truck_no, months), cat='Binary')
truck_buy = LpVariable.dicts("truck_buy", (truck_no, months), 0, 1, LpInteger)
truck_sell = LpVariable.dicts("truck_sell", (truck_no, months), 0, 1, LpInteger)
truck_type = LpVariable.dicts("truck_type", truck_no, 0, 1, LpInteger)
# truck_switch = LpVariable.dicts

acid_routes = [(seller, client) for seller in acid_factories for client in acid_clients]
base_routes = [(seller, client) for seller in base_factories for client in base_clients]
routes = acid_routes + base_routes
# supply of one truck on one route during one year
route_info_vars = LpVariable.dicts("Route", (truck_no, routes, years), 0, None, LpInteger)
# todo: add month index to keep more details

prob = LpProblem("Chemical_Products_Transportation_Problem", LpMinimize)

maintenance_vector = [(truck_status[n][m] * 166.67 for n in truck_no for m in months)]
gas_vector = [(route_info_vars[n][route][y]) * distances[route[0]][route[1]] * 2 for route in routes for n in truck_no
              for y in years]
purchase_vector = [truck_buy[n][m] * 40000 for n in truck_no for m in months]
sell_vector = [-truck_sell[n][m] * 20000 for n in truck_no for m in months]

prob += lpSum(
    maintenance_vector
    +
    purchase_vector
    +
    sell_vector
), "Maintenance costs"

for y in years:
    prob += lpSum(route_info_vars[n][("Anvers", "Liege")][y] for n in truck_no) == min_trips("Liege", y) - 1, \
            "Liege acid supply during year {}".format(y)
    for b_c in base_clients:
        prob += lpSum(route_info_vars[n][("Liege", b_c)][y] for n in truck_no) == min_trips(b_c, y) - 1, \
                "{} base supply during year {}".format(b_c, y)

for n in truck_no:
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
            prob += truck_sell[t][m] <= truck_status[t][m - 1]

# todo: preferably purchase the trucks as late as possible to use them the following year with minimal downtime

# todo: add a way to be able to carry over trucks to the next year without selling and buying again, we could possibly
#  sell it at full price at the end of the year and buy it again after new year, which would be equivalent to
#  never having sold it at all

# todo: add type 2 trucks for round trips between antwerp and liege

# todo: add another algorithm going through all the cities and supplying the remaining tonnes

prob.writeLP("Chem_Transport_Problem.lp")
status = prob.solve(solver=GLPK(msg=True, keepFiles=True, options=["--tmlim", "10"]))

for route in routes:
    product = ""
    if route[0] == "Anvers":
        product = "acid"
    else:
        product = "base"
    print("{} demand for {} is {} tonnes.".format(route[1], product, annual_demand_1[route[1]]))
    total_delivered = 0
    for y in years:
        year_delivered = 0
        for no in truck_no:
            if route_info_vars[no][route][y].varValue > 0:
                no_tonnes = int(floor(truck_max_capacity * route_info_vars[no][route][y].varValue))
                no_trips = route_info_vars[no][route][y].varValue
                time_trip = int(2 * (distances[route[0]][route[1]] / truck_speed + 1))
                no_hours = int(no_trips * time_trip)
                avail_months = sum([truck_status[no][m].varValue for m in range(y * 12, (y + 1) * 12)])
                avail_hours = avail_months * 4 * 5 * 8
                print("Truck {} delivers {} tonnes during year {}.".format(no, no_tonnes, y))
                year_delivered += truck_max_capacity * route_info_vars[no][route][y].varValue
        total_delivered += year_delivered
        print("Total delivered to {} during year {} is {}.".format(route[1], y, year_delivered))
    print("")

for no in truck_no:
    hybrid = False
    for y in years:
        if sum([truck_status[no][m].varValue for m in range(y * 12, (y + 1) * 12)]) > 0:
            acid, base = False, False
            for route in routes:
                if route[0] == "Anvers" and route_info_vars[no][route][y].varValue > 0:
                    acid = True
                if route[0] == "Liege" and route_info_vars[no][route][y].varValue > 0:
                    base = True
            hybrid = acid and base
            if hybrid:
                print("Truck no {} delivers both acids and bases.".format(no))

for no in truck_no:
    months_list = []
    for m in months:
        if truck_status[no][m].varValue == 1:
            months_list.append(m)
    if len(months_list) > 0:
        print("You must have truck number {} available during the following months: {}.".format(no, months_list))

for t in truck_no:
    rent_list, buy_list, sell_list = [], [], []
    for m in months:
        rent_list.append(truck_status[t][m].varValue)
        buy_list.append(truck_buy[t][m].varValue)
        sell_list.append(truck_sell[t][m].varValue)
    print("truck no {} rent: {}\n buy: {}\nsell: {}".format(
        t, rent_list, buy_list, sell_list))

obj_func = 0

for t in truck_no:
    rent_list, buy_list, sell_list = [], [], []
    rent_price, buy_price, sell_price = 0, 0, 0
    for m in months:
        rent_list.append(truck_status[t][m].varValue)
        buy_list.append(truck_buy[t][m].varValue)
        sell_list.append(truck_sell[t][m].varValue)
    buy_price += buy_list.count(1) * 40000
    sell_price += sell_list.count(1) * 20000
    rent_price += rent_list.count(1) * 166.67
    total_price = buy_price + rent_price - sell_price
    obj_func += total_price
    print("truck number {}: purchase price = {} ; rent price = {} ; sell price = {} ; total price = {}".format(
        t, buy_price, int(rent_price), sell_price, int(total_price)
    ))

print("total cost is {}.".format(int(obj_func)))
