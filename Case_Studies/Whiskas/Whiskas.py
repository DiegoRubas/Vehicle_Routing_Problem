"""
The Full Whiskas Model Python Formulation for the PuLP Modeller

Author: Diego Rubas, 2021
"""

# Import PuLP modeler functions
from pulp import *

# Creates a list of the Ingredients
Ingredients = ["CHICKEN", "BEEF", "MUTTON", "RICE", "WHEAT", "GEL"]

# A dictionary of the costs of each of the Ingredients is created
costs = {
    "CHICKEN": 0.013,
    "BEEF": 0.008,
    "MUTTON": 0.010,
    "RICE": 0.002,
    "WHEAT": 0.005,
    "GEL": 0.001
}

# A dictionary of the of the protein percent in each of the Ingredients is created
protein_percent = {
    "CHICKEN": 0.100,
    "BEEF": 0.200,
    "MUTTON": 0.150,
    "RICE": 0.000,
    "WHEAT": 0.040,
    "GEL": 0.000
}

# A dictionary of the fat percent in each of the Ingredients is created
fat_percent = {
    "CHICKEN": 0.080,
    "BEEF": 0.100,
    "MUTTON": 0.110,
    "RICE": 0.010,
    "WHEAT": 0.010,
    "GEL": 0.000
}

# A dictionary of the fiber percent in each of the Ingredients is created
fiber_percent = {
    "CHICKEN": 0.001,
    "BEEF": 0.005,
    "MUTTON": 0.003,
    "RICE": 0.100,
    "WHEAT": 0.150,
    "GEL": 0.000
}

# A dictionary of the salt percent in each of the Ingredients is created
salt_percent = {
    "CHICKEN": 0.002,
    "BEEF": 0.005,
    "MUTTON": 0.007,
    "RICE": 0.002,
    "WHEAT": 0.008,
    "GEL": 0.000
}

# A dictionary called 'ingredient_vars' is created to contain the referenced variables
ingredient_vars = LpVariable.dict("Ingredient", Ingredients, 0)

# Create the problem variable to contain the problem data
prob = LpProblem("The Whiskas Problem", LpMinimize)

# The objective function is added to the problem first
prob += 0.013 * ingredient_vars[Ingredients[0]] + 0.008 * ingredient_vars[Ingredients[1]] \
        + 0.010 * ingredient_vars[Ingredients[2]] + 0.002 * ingredient_vars[Ingredients[3]] \
        + 0.005 * ingredient_vars[Ingredients[4]] + 0.001 * ingredient_vars[Ingredients[5]], \
        "Total Cost of Ingredients per can"

# The constraints are entered
prob += lpSum(ingredient_vars[ing] for ing in Ingredients) == 100, "Percentages Sum"
prob += lpSum(protein_percent[ing] * ingredient_vars[ing] for ing in Ingredients) >= 8, "Protein Requirement"
prob += lpSum(fat_percent[ing] * ingredient_vars[ing] for ing in Ingredients) >= 6, "Fat Requirement"
prob += lpSum(fiber_percent[ing] * ingredient_vars[ing] for ing in Ingredients) <= 4, "Fiber Requirement"
prob += lpSum(salt_percent[ing] * ingredient_vars[ing] for ing in Ingredients) <= 0.2, "Salt Requirement"

# The problem data is written to an .lp file
prob.writeLP("Whiskas_Model.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status: ", LpStatus[prob.status])

# Each of the variables is printed with its resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("The Total Cost of Ingredients per can =", value(prob.objective))
