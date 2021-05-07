"""
The Sudoku Problem Formulation for the PuLP Modeller

Author: Diego Rubas 2021
"""

from pulp import *

VALS = ROWS = COLS = range(1, 10)

Boxes = [
    [(3 * i + k + 1, 3 * j + l + 1) for k in range(3) for l in range(3)]
    for i in range(3) for j in range(3)
]

prob = LpProblem("Sudoku Problem")

choices = LpVariable.dicts("Choice", (VALS, ROWS, COLS), cat="Binary")

for r in ROWS:
    for c in COLS:
        prob += lpSum([choices[v][r][c] for v in VALS]) == 1

for v in VALS:
    for r in ROWS:
        prob += lpSum([choices[v][r][c] for c in COLS]) == 1
    for c in COLS:
        prob += lpSum([choices[v][r][c] for r in ROWS]) == 1
    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1

input_data = [
    (5, 1, 1),
    (6, 2, 1),
    (8, 4, 1),
    (4, 5, 1),
    (7, 6, 1),
    (3, 1, 2),
    (9, 3, 2),
    (6, 7, 2),
    (8, 3, 3),
    (1, 2, 4),
    (8, 5, 4),
    (4, 8, 4),
    (7, 1, 5),
    (9, 2, 5),
    (6, 4, 5),
    (2, 6, 5),
    (1, 8, 5),
    (8, 9, 5),
    (5, 2, 6),
    (3, 5, 6),
    (9, 8, 6),
    (2, 7, 7),
    (6, 3, 8),
    (8, 7, 8),
    (7, 9, 8),
    (3, 4, 9),
    (1, 5, 9),
    (6, 6, 9),
    (5, 8, 9),
]

for (v, r, c) in input_data:
    prob += choices[v][r][c] == 1

prob.writeLP("Sudoku.lp")

prob.solve()

print("Status:", LpStatus[prob.status])

sudoku_out = open("sudoku_out.txt", "w")

for r in ROWS:
    if r in [1, 4, 7]:
        sudoku_out.write("+-------+-------+-------+\n")
    for c in COLS:
        for v in VALS:
            if value(choices[v][r][c]) == 1:
                if c in [1, 4, 7]:
                    sudoku_out.write("| ")
                sudoku_out.write(str(v) + " ")
                if c == 9:
                    sudoku_out.write("|\n")
sudoku_out.write("+-------+-------+-------+")
sudoku_out.close()
