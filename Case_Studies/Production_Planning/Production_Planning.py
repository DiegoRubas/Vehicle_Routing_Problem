"""
Two Stage Production Planning Problem with PuLP Modeller

Author: Diego Rubas 2021
"""

from pulp import *

products = "wrenches pliers".split()
price = [130, 100]
steel = [1.5, 1]
molding = [1, 1]
assembly = [0.3, 0.5]
cap_steel = 27
cap_molding = 21
LB = [0, 0]
capacity_ub = [15, 16]
steel_price = 58

scenarios = range(4)
prob_scenario = [0.25, 0.25, 0.25, 0.25]
wrench_earnings = [160, 160, 90, 90]
pliers_earnings = [100, 100, 100, 100]
cap_assembly = [8, 10, 8, 10]

production = [(j, i) for j in scenarios for i in products]
prices_scenario = [[wrench_earnings[j], pliers_earnings[j]] for j in scenarios]
price_items = [item for sublist in prices_scenario for item in sublist]

price_dict = dict(zip(production, price_items))
capacity_dict = dict(zip(products, capacity_ub * 4))
steel_dict = dict(zip(products, steel))
molding_dict = dict(zip(products, molding))
assembly_dict = dict(zip(products, assembly))

production_vars = LpVariable.dicts(
    "production", (scenarios, products), lowBound=0, cat="Continuous"
)
steel_purchase = LpVariable("steel_purchase", lowBound=0, cat="Continuous")

gemstone_problem = LpProblem("The Gemstone Tool Problem", LpMaximize)

gemstone_problem += (
    lpSum(
        [
            prob_scenario[j] * (price_dict[(j, i)] * production_vars[j][i])
            for (j, i) in production
        ]
        - steel_purchase * steel_price
    ),
    "Total cost"
)

for j in scenarios:

    gemstone_problem += lpSum(
        [steel_dict[i] * production_vars[j][i] for i in products]
    ) - steel_purchase <= 0, ("Steel capacity", str(j))

    gemstone_problem += lpSum(
        [molding_dict[i] * production_vars[j][i] for i in products]
    ) <= cap_molding, ("Molding capacity", str(j))

    gemstone_problem += lpSum(
        [assembly_dict[i] * production_vars[j][i] for i in products]
    ) <= cap_assembly[j], ("Assembly capacity", str(j))

    for i in products:
        gemstone_problem += production_vars[j][i] <= capacity_dict[i], (
            "Capacity", str(i), str(j)
        )

print(gemstone_problem)

gemstone_problem.writeLP("Gemstone_Problem.lp")
gemstone_problem.solve()
print("Status", LpStatus(gemstone_problem))

for v in gemstone_problem.variables():
    print(v.name, "=", v.varValue)
production = [v.varValue for v in gemstone_problem.variables()]

print("Total price =", value(gemstone_problem.objective))
