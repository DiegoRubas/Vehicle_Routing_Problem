\* The_Gemstone_Tool_Problem *\
Maximize
Total_cost: 25 production_0_pliers + 40 production_0_wrenches
 + 25 production_1_pliers + 40 production_1_wrenches + 25 production_2_pliers
 + 22.5 production_2_wrenches + 25 production_3_pliers
 + 22.5 production_3_wrenches - 58 steel_purchase
Subject To
('Assembly_capacity',_'0'): 0.5 production_0_pliers
 + 0.3 production_0_wrenches <= 8
('Assembly_capacity',_'1'): 0.5 production_1_pliers
 + 0.3 production_1_wrenches <= 10
('Assembly_capacity',_'2'): 0.5 production_2_pliers
 + 0.3 production_2_wrenches <= 8
('Assembly_capacity',_'3'): 0.5 production_3_pliers
 + 0.3 production_3_wrenches <= 10
('Capacity',_'pliers',_'0'): production_0_pliers <= 16
('Capacity',_'pliers',_'1'): production_1_pliers <= 16
('Capacity',_'pliers',_'2'): production_2_pliers <= 16
('Capacity',_'pliers',_'3'): production_3_pliers <= 16
('Capacity',_'wrenches',_'0'): production_0_wrenches <= 15
('Capacity',_'wrenches',_'1'): production_1_wrenches <= 15
('Capacity',_'wrenches',_'2'): production_2_wrenches <= 15
('Capacity',_'wrenches',_'3'): production_3_wrenches <= 15
('Molding_capacity',_'0'): production_0_pliers + production_0_wrenches <= 21
('Molding_capacity',_'1'): production_1_pliers + production_1_wrenches <= 21
('Molding_capacity',_'2'): production_2_pliers + production_2_wrenches <= 21
('Molding_capacity',_'3'): production_3_pliers + production_3_wrenches <= 21
('Steel_capacity',_'0'): production_0_pliers + 1.5 production_0_wrenches
 - steel_purchase <= 0
('Steel_capacity',_'1'): production_1_pliers + 1.5 production_1_wrenches
 - steel_purchase <= 0
('Steel_capacity',_'2'): production_2_pliers + 1.5 production_2_wrenches
 - steel_purchase <= 0
('Steel_capacity',_'3'): production_3_pliers + 1.5 production_3_wrenches
 - steel_purchase <= 0
End
