"""
The Beer Distribution Problem for the PuLP Modeller

Author: Diego Rubas 2021
"""

from pulp import *

Warehouses = "A B".split()

supply = {
    "A": 1000,
    "B": 4000
}

Bars = "1 2 3 4 5".split()

demand = {
    "1": 500,
    "2": 900,
    "3": 1800,
    "4": 200,
    "5": 700,
}

costs = [
    # 1  2  3  4  5
    [2, 4, 5, 2, 1],    # A
    [3, 1, 3, 2, 3]     # B
]

costs = makeDict([Warehouses, Bars], costs, 0)

prob = LpProblem("Beer Distribution Problem", LpMinimize)

Routes = [(w, b) for w in Warehouses for b in Bars]

route_vars = LpVariable.dicts("Route", (Warehouses, Bars), 0, None, LpInteger)

prob += lpSum([route_vars[w][b] * costs[w][b] for (w, b) in Routes])

for w in Warehouses:
    prob += lpSum([route_vars[w][b] for b in Bars]) <= supply[w], "Sum of Products out of warehouse %s" % w

for b in Bars:
    prob += lpSum([route_vars[w][b]] for w in Warehouses) >= demand[b], "Sum of Products into Bar %s" % b

status = prob.solve(solver=GLPK(msg=True, keepFiles=True))