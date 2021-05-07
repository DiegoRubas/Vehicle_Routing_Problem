\* The_Whiskas_Problem *\
Minimize
Total_Cost_of_Ingredients_per_can: 0.008 Ingredient_BEEF
 + 0.013 Ingredient_CHICKEN + 0.001 Ingredient_GEL + 0.01 Ingredient_MUTTON
 + 0.002 Ingredient_RICE + 0.005 Ingredient_WHEAT
Subject To
Fat_Requirement: 0.1 Ingredient_BEEF + 0.08 Ingredient_CHICKEN
 + 0.11 Ingredient_MUTTON + 0.01 Ingredient_RICE + 0.01 Ingredient_WHEAT >= 6
Fiber_Requirement: 0.005 Ingredient_BEEF + 0.001 Ingredient_CHICKEN
 + 0.003 Ingredient_MUTTON + 0.1 Ingredient_RICE + 0.15 Ingredient_WHEAT <= 4
Percentages_Sum: Ingredient_BEEF + Ingredient_CHICKEN + Ingredient_GEL
 + Ingredient_MUTTON + Ingredient_RICE + Ingredient_WHEAT = 100
Protein_Requirement: 0.2 Ingredient_BEEF + 0.1 Ingredient_CHICKEN
 + 0.15 Ingredient_MUTTON + 0.04 Ingredient_WHEAT >= 8
Salt_Requirement: 0.005 Ingredient_BEEF + 0.002 Ingredient_CHICKEN
 + 0.007 Ingredient_MUTTON + 0.002 Ingredient_RICE + 0.008 Ingredient_WHEAT
 <= 0.2
End
