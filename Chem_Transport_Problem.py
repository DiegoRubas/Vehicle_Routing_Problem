from pulp import *
from math import ceil, floor


def min_trips(city):
    if after_18_months:
        result = ceil(annual_demand_2[city] / truck_max_capacity)
    else:
        result = ceil(annual_demand_1[city] / truck_max_capacity)
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
after_18_months = False

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

truck_no = range(1, 21)
month_type = "buy sell".split()
truck_sale = [(n, t) for n in truck_no for t in month_type]
truck_sale_vars = LpVariable.dicts("Truck", (truck_no, month_type), 0, 12, LpInteger)

acid_routes = [(seller, client) for seller in acid_factories for client in acid_clients]
base_routes = [(seller, client) for seller in base_factories for client in base_clients]
routes = acid_routes + base_routes
route_info = [(n, r) for n in truck_no for r in routes]
route_info_vars = LpVariable.dicts("Route", (truck_no, routes), 0, None, LpInteger)
# todo: add month index to keep more details

prob = LpProblem("Chemical_Products_Transportation_Problem")

maintenance_vector = [(truck_sale_vars[n]["sell"] - truck_sale_vars[n]["buy"]) * 167 for n in truck_no]
gas_vector = [(route_info_vars[n][route]) * distances[route[0]][route[1]] * 2 for route in routes for n in truck_no]
# purchase_vector = [floor(truck_sale_vars[n]["sell"] * 0.084) * 40000 for n in truck_no]

prob += lpSum(
    # gas_vector
    # +
    maintenance_vector
    # +
    # purchase_vector
), "Maintenance costs"

prob += lpSum(route_info_vars[n][("Anvers", "Liege")] for n in truck_no) >= min_trips("Liege") - 1, "Liege Acid Trips"
for b_c in base_clients:
    prob += lpSum(route_info_vars[n][("Liege", b_c)] for n in truck_no) >= min_trips(b_c) - 1, "{} Base Trips".format(
        b_c)

for n in truck_no:
    # todo: add washing time for trucks delivering acids and bases
    # todo: add travel time for trucks going from the base factory to the acid factory and vice versa
    tot_hours = 0
    for a_f in acid_factories:
        for a_c in acid_clients:
            tot_hours += route_info_vars[n][(a_f, a_c)] * round_trip_time(a_f, a_c)
    for b_f in base_factories:
        for b_c in base_clients:
            tot_hours += route_info_vars[n][(b_f, b_c)] * round_trip_time(b_f, b_c)
    prob += (truck_sale_vars[n]["sell"] - truck_sale_vars[n]["buy"]) * hours_in_month >= tot_hours, \
            "Truck {} time check".format(n)

# todo: preferably purchase the trucks as late as possible to use them the following year with minimal downtime

# todo: add a way to be able to carry over trucks to the next year without selling and buying again, we could possibly
#  sell it at full price at the end of the year and buy it again after new year, which would be equivalent to
#  never having sold it at all

# todo: add type 2 trucks for round trips between antwerp and liege

# todo: add another algorithm going through all the cities and supplying the remaining tonnes

prob.writeLP("Chem_Transport_Problem.lp")
status = prob.solve(solver=GLPK(msg=True, keepFiles=True))

for route in routes:
    product = ""
    if route[0] == "Anvers":
        product = "acid"
    else:
        product = "base"
    print("{} demand for {} is {} tonnes.".format(route[1], product, annual_demand_1[route[1]]))
    total_delivered = 0
    for no in truck_no:
        if route_info_vars[no][route].varValue > 0:
            no_tonnes = int(floor(truck_max_capacity * route_info_vars[no][route].varValue))
            no_trips = route_info_vars[no][route].varValue
            time_trip = int(2 * (distances[route[0]][route[1]] / truck_speed + 1))
            no_hours = int(no_trips * time_trip)
            avail_months = truck_sale_vars[no]["sell"].varValue - truck_sale_vars[no]["buy"].varValue
            avail_hours = avail_months * 4 * 5 * 8
            print("Truck", no, "delivers", no_tonnes, "tonnes of", product, "over", no_trips,
                  str(time_trip) + "-hour round trips, taking", no_hours,
                  "hours over its available", avail_hours, "hours.")
            total_delivered += truck_max_capacity * route_info_vars[no][route].varValue
    print("Total delivered to", route[1], "is", total_delivered, "\n")

total_idle_hours = 0
total_avail_hours = 0

for no in truck_no:
    hybrid = False
    if truck_sale_vars[no]["sell"].varValue != truck_sale_vars[no]["buy"].varValue:
        acid, base = False, False
        no_total_hours = 0
        for route in routes:
            if route[0] == "Anvers" and route_info_vars[no][route].varValue > 0:
                acid = True
            if route[0] == "Liege" and route_info_vars[no][route].varValue > 0:
                base = True
            no_trips = route_info_vars[no][route].varValue
            time_trip = (2 * ((distances[route[0]][route[1]] / truck_speed) + 1))
            no_hours = (no_trips * time_trip)
            no_total_hours += no_hours
        hybrid = acid and base
        if hybrid:
        #     no_total_hours = cleaning_time
            print("Truck no {} delivers both acids and bases.".format(no))
        no_avail_months = truck_sale_vars[no]["sell"].varValue - truck_sale_vars[no]["buy"].varValue
        no_avail_hours = no_avail_months * 4 * 5 * 8
        no_idle_hours = no_avail_hours - no_total_hours
        efficiency = (no_total_hours / no_avail_hours) * 100
        # print(
        #     "Truck number {} will use {} hours of its available {} hours, i.e. {}%. Total idle time is {} hours.".format(
        #         no, round(no_total_hours, 2),
        #         round(no_avail_hours, 2),
        #         round(efficiency, 2), round(no_idle_hours, 2)))
        print(
            "Truck number {} will use {} hours of its available {} hours.\nTotal idle time is {} hours.\nTime efficiency is {}%.\n".format(
                no, round(no_total_hours, 2), int(no_avail_hours), round(no_idle_hours, 2), round(efficiency, 2))
        )
        total_idle_hours += no_idle_hours
        total_avail_hours += no_avail_hours

idle_percent = int((total_idle_hours / total_avail_hours) * 100)

print("Total number of idle hours is {} out of {} available hours, i.e. {}%.\n".format(
    round(total_idle_hours, 2), total_avail_hours, round(idle_percent, 2))
)

trucks_to_buy = len(truck_no)
for no in truck_no:
    if truck_sale_vars[no]["sell"].varValue == truck_sale_vars[no]["buy"].varValue:
        trucks_to_buy -= 1

print("In order to achieve these results, you must buy", trucks_to_buy, "trucks.")

for no in truck_no:
    if truck_sale_vars[no]["sell"].varValue != truck_sale_vars[no]["buy"].varValue:
        print("You must buy truck number", no, "at month", truck_sale_vars[no]["buy"].varValue, "and sell it at month",
              str(truck_sale_vars[no]["sell"].varValue) + ".")
