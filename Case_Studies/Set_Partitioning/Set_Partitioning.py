"""
A set partitioning model of a wedding seating problem

Author: Diego Rubas 2021
"""

from pulp import *



max_tables = 5
max_table_size = 4
guests = "A B C D E F G H I J K L M N O P Q R".split()


def happiness(table):
    """
    Find the happiness of the table by calculating the maximum distance between the letters
    """
    print(abs(ord(table[0]) - ord(table[-1])))
    return abs(ord(table[0]) - ord(table[-1]))


# create list of all possible tables
possible_tables = [tuple(c) for c in allcombinations(guests, max_table_size)]

# create a binary variable to state that  table setting is used
table_vars = LpVariable.dicts("table", possible_tables, lowBound=0, upBound=1, cat=LpInteger)

seating_model = LpProblem("Wedding Seating Model", LpMinimize)

seating_model += lpSum([happiness(table) * table_vars[table] for table in possible_tables])

# Specify the maximum number of tables
seating_model += (
    lpSum([table_vars[table] for table in possible_tables]) <= max_tables,
    "Maximum number of tables"
)

# A guest must be seated at one and only one table
for guest in guests:
    seating_model += (
        lpSum([table_vars[table] for table in possible_tables if guest in table]) == 1,
        "Must_seat_%s" % guest,
    )

seating_model.solve()

print("The chosen tables are out of a total of %s:" % len(possible_tables))
for table in possible_tables:
    if table_vars[table].value() == 1.0:
        print(table)
