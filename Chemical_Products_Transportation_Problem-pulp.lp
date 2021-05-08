\* Chemical_Products_Transportation_Problem *\
Minimize
Maintenance_costs: - 167 Truck_10_buy + 167 Truck_10_sell - 167 Truck_11_buy
 + 167 Truck_11_sell - 167 Truck_12_buy + 167 Truck_12_sell - 167 Truck_13_buy
 + 167 Truck_13_sell - 167 Truck_14_buy + 167 Truck_14_sell - 167 Truck_15_buy
 + 167 Truck_15_sell - 167 Truck_16_buy + 167 Truck_16_sell - 167 Truck_17_buy
 + 167 Truck_17_sell - 167 Truck_18_buy + 167 Truck_18_sell - 167 Truck_19_buy
 + 167 Truck_19_sell - 167 Truck_1_buy + 167 Truck_1_sell - 167 Truck_20_buy
 + 167 Truck_20_sell - 167 Truck_2_buy + 167 Truck_2_sell - 167 Truck_3_buy
 + 167 Truck_3_sell - 167 Truck_4_buy + 167 Truck_4_sell - 167 Truck_5_buy
 + 167 Truck_5_sell - 167 Truck_6_buy + 167 Truck_6_sell - 167 Truck_7_buy
 + 167 Truck_7_sell - 167 Truck_8_buy + 167 Truck_8_sell - 167 Truck_9_buy
 + 167 Truck_9_sell
Subject To
Anvers_Base_Trips: Route_10_('Liege',_'Anvers') + Route_11_('Liege',_'Anvers')
 + Route_12_('Liege',_'Anvers') + Route_13_('Liege',_'Anvers')
 + Route_14_('Liege',_'Anvers') + Route_15_('Liege',_'Anvers')
 + Route_16_('Liege',_'Anvers') + Route_17_('Liege',_'Anvers')
 + Route_18_('Liege',_'Anvers') + Route_19_('Liege',_'Anvers')
 + Route_1_('Liege',_'Anvers') + Route_20_('Liege',_'Anvers')
 + Route_2_('Liege',_'Anvers') + Route_3_('Liege',_'Anvers')
 + Route_4_('Liege',_'Anvers') + Route_5_('Liege',_'Anvers')
 + Route_6_('Liege',_'Anvers') + Route_7_('Liege',_'Anvers')
 + Route_8_('Liege',_'Anvers') + Route_9_('Liege',_'Anvers') >= 545
Bruxelles_Base_Trips: Route_10_('Liege',_'Bruxelles')
 + Route_11_('Liege',_'Bruxelles') + Route_12_('Liege',_'Bruxelles')
 + Route_13_('Liege',_'Bruxelles') + Route_14_('Liege',_'Bruxelles')
 + Route_15_('Liege',_'Bruxelles') + Route_16_('Liege',_'Bruxelles')
 + Route_17_('Liege',_'Bruxelles') + Route_18_('Liege',_'Bruxelles')
 + Route_19_('Liege',_'Bruxelles') + Route_1_('Liege',_'Bruxelles')
 + Route_20_('Liege',_'Bruxelles') + Route_2_('Liege',_'Bruxelles')
 + Route_3_('Liege',_'Bruxelles') + Route_4_('Liege',_'Bruxelles')
 + Route_5_('Liege',_'Bruxelles') + Route_6_('Liege',_'Bruxelles')
 + Route_7_('Liege',_'Bruxelles') + Route_8_('Liege',_'Bruxelles')
 + Route_9_('Liege',_'Bruxelles') >= 375
Charleroi_Base_Trips: Route_10_('Liege',_'Charleroi')
 + Route_11_('Liege',_'Charleroi') + Route_12_('Liege',_'Charleroi')
 + Route_13_('Liege',_'Charleroi') + Route_14_('Liege',_'Charleroi')
 + Route_15_('Liege',_'Charleroi') + Route_16_('Liege',_'Charleroi')
 + Route_17_('Liege',_'Charleroi') + Route_18_('Liege',_'Charleroi')
 + Route_19_('Liege',_'Charleroi') + Route_1_('Liege',_'Charleroi')
 + Route_20_('Liege',_'Charleroi') + Route_2_('Liege',_'Charleroi')
 + Route_3_('Liege',_'Charleroi') + Route_4_('Liege',_'Charleroi')
 + Route_5_('Liege',_'Charleroi') + Route_6_('Liege',_'Charleroi')
 + Route_7_('Liege',_'Charleroi') + Route_8_('Liege',_'Charleroi')
 + Route_9_('Liege',_'Charleroi') >= 727
Gand_Base_Trips: Route_10_('Liege',_'Gand') + Route_11_('Liege',_'Gand')
 + Route_12_('Liege',_'Gand') + Route_13_('Liege',_'Gand')
 + Route_14_('Liege',_'Gand') + Route_15_('Liege',_'Gand')
 + Route_16_('Liege',_'Gand') + Route_17_('Liege',_'Gand')
 + Route_18_('Liege',_'Gand') + Route_19_('Liege',_'Gand')
 + Route_1_('Liege',_'Gand') + Route_20_('Liege',_'Gand')
 + Route_2_('Liege',_'Gand') + Route_3_('Liege',_'Gand')
 + Route_4_('Liege',_'Gand') + Route_5_('Liege',_'Gand')
 + Route_6_('Liege',_'Gand') + Route_7_('Liege',_'Gand')
 + Route_8_('Liege',_'Gand') + Route_9_('Liege',_'Gand') >= 121
Hasselt_Base_Trips: Route_10_('Liege',_'Hasselt')
 + Route_11_('Liege',_'Hasselt') + Route_12_('Liege',_'Hasselt')
 + Route_13_('Liege',_'Hasselt') + Route_14_('Liege',_'Hasselt')
 + Route_15_('Liege',_'Hasselt') + Route_16_('Liege',_'Hasselt')
 + Route_17_('Liege',_'Hasselt') + Route_18_('Liege',_'Hasselt')
 + Route_19_('Liege',_'Hasselt') + Route_1_('Liege',_'Hasselt')
 + Route_20_('Liege',_'Hasselt') + Route_2_('Liege',_'Hasselt')
 + Route_3_('Liege',_'Hasselt') + Route_4_('Liege',_'Hasselt')
 + Route_5_('Liege',_'Hasselt') + Route_6_('Liege',_'Hasselt')
 + Route_7_('Liege',_'Hasselt') + Route_8_('Liege',_'Hasselt')
 + Route_9_('Liege',_'Hasselt') >= 21
Liege_Acid_Trips: Route_10_('Anvers',_'Liege') + Route_11_('Anvers',_'Liege')
 + Route_12_('Anvers',_'Liege') + Route_13_('Anvers',_'Liege')
 + Route_14_('Anvers',_'Liege') + Route_15_('Anvers',_'Liege')
 + Route_16_('Anvers',_'Liege') + Route_17_('Anvers',_'Liege')
 + Route_18_('Anvers',_'Liege') + Route_19_('Anvers',_'Liege')
 + Route_1_('Anvers',_'Liege') + Route_20_('Anvers',_'Liege')
 + Route_2_('Anvers',_'Liege') + Route_3_('Anvers',_'Liege')
 + Route_4_('Anvers',_'Liege') + Route_5_('Anvers',_'Liege')
 + Route_6_('Anvers',_'Liege') + Route_7_('Anvers',_'Liege')
 + Route_8_('Anvers',_'Liege') + Route_9_('Anvers',_'Liege') >= 1818
Truck_10_time_check: - 5 Route_10_('Anvers',_'Liege')
 - 5 Route_10_('Liege',_'Anvers')
 - 4.85714285714 Route_10_('Liege',_'Bruxelles')
 - 4.85714285714 Route_10_('Liege',_'Charleroi')
 - 6 Route_10_('Liege',_'Gand') - 3.71428571429 Route_10_('Liege',_'Hasselt')
 - 160 Truck_10_buy + 160 Truck_10_sell >= 0
Truck_11_time_check: - 5 Route_11_('Anvers',_'Liege')
 - 5 Route_11_('Liege',_'Anvers')
 - 4.85714285714 Route_11_('Liege',_'Bruxelles')
 - 4.85714285714 Route_11_('Liege',_'Charleroi')
 - 6 Route_11_('Liege',_'Gand') - 3.71428571429 Route_11_('Liege',_'Hasselt')
 - 160 Truck_11_buy + 160 Truck_11_sell >= 0
Truck_12_time_check: - 5 Route_12_('Anvers',_'Liege')
 - 5 Route_12_('Liege',_'Anvers')
 - 4.85714285714 Route_12_('Liege',_'Bruxelles')
 - 4.85714285714 Route_12_('Liege',_'Charleroi')
 - 6 Route_12_('Liege',_'Gand') - 3.71428571429 Route_12_('Liege',_'Hasselt')
 - 160 Truck_12_buy + 160 Truck_12_sell >= 0
Truck_13_time_check: - 5 Route_13_('Anvers',_'Liege')
 - 5 Route_13_('Liege',_'Anvers')
 - 4.85714285714 Route_13_('Liege',_'Bruxelles')
 - 4.85714285714 Route_13_('Liege',_'Charleroi')
 - 6 Route_13_('Liege',_'Gand') - 3.71428571429 Route_13_('Liege',_'Hasselt')
 - 160 Truck_13_buy + 160 Truck_13_sell >= 0
Truck_14_time_check: - 5 Route_14_('Anvers',_'Liege')
 - 5 Route_14_('Liege',_'Anvers')
 - 4.85714285714 Route_14_('Liege',_'Bruxelles')
 - 4.85714285714 Route_14_('Liege',_'Charleroi')
 - 6 Route_14_('Liege',_'Gand') - 3.71428571429 Route_14_('Liege',_'Hasselt')
 - 160 Truck_14_buy + 160 Truck_14_sell >= 0
Truck_15_time_check: - 5 Route_15_('Anvers',_'Liege')
 - 5 Route_15_('Liege',_'Anvers')
 - 4.85714285714 Route_15_('Liege',_'Bruxelles')
 - 4.85714285714 Route_15_('Liege',_'Charleroi')
 - 6 Route_15_('Liege',_'Gand') - 3.71428571429 Route_15_('Liege',_'Hasselt')
 - 160 Truck_15_buy + 160 Truck_15_sell >= 0
Truck_16_time_check: - 5 Route_16_('Anvers',_'Liege')
 - 5 Route_16_('Liege',_'Anvers')
 - 4.85714285714 Route_16_('Liege',_'Bruxelles')
 - 4.85714285714 Route_16_('Liege',_'Charleroi')
 - 6 Route_16_('Liege',_'Gand') - 3.71428571429 Route_16_('Liege',_'Hasselt')
 - 160 Truck_16_buy + 160 Truck_16_sell >= 0
Truck_17_time_check: - 5 Route_17_('Anvers',_'Liege')
 - 5 Route_17_('Liege',_'Anvers')
 - 4.85714285714 Route_17_('Liege',_'Bruxelles')
 - 4.85714285714 Route_17_('Liege',_'Charleroi')
 - 6 Route_17_('Liege',_'Gand') - 3.71428571429 Route_17_('Liege',_'Hasselt')
 - 160 Truck_17_buy + 160 Truck_17_sell >= 0
Truck_18_time_check: - 5 Route_18_('Anvers',_'Liege')
 - 5 Route_18_('Liege',_'Anvers')
 - 4.85714285714 Route_18_('Liege',_'Bruxelles')
 - 4.85714285714 Route_18_('Liege',_'Charleroi')
 - 6 Route_18_('Liege',_'Gand') - 3.71428571429 Route_18_('Liege',_'Hasselt')
 - 160 Truck_18_buy + 160 Truck_18_sell >= 0
Truck_19_time_check: - 5 Route_19_('Anvers',_'Liege')
 - 5 Route_19_('Liege',_'Anvers')
 - 4.85714285714 Route_19_('Liege',_'Bruxelles')
 - 4.85714285714 Route_19_('Liege',_'Charleroi')
 - 6 Route_19_('Liege',_'Gand') - 3.71428571429 Route_19_('Liege',_'Hasselt')
 - 160 Truck_19_buy + 160 Truck_19_sell >= 0
Truck_1_time_check: - 5 Route_1_('Anvers',_'Liege')
 - 5 Route_1_('Liege',_'Anvers')
 - 4.85714285714 Route_1_('Liege',_'Bruxelles')
 - 4.85714285714 Route_1_('Liege',_'Charleroi') - 6 Route_1_('Liege',_'Gand')
 - 3.71428571429 Route_1_('Liege',_'Hasselt') - 160 Truck_1_buy
 + 160 Truck_1_sell >= 0
Truck_20_time_check: - 5 Route_20_('Anvers',_'Liege')
 - 5 Route_20_('Liege',_'Anvers')
 - 4.85714285714 Route_20_('Liege',_'Bruxelles')
 - 4.85714285714 Route_20_('Liege',_'Charleroi')
 - 6 Route_20_('Liege',_'Gand') - 3.71428571429 Route_20_('Liege',_'Hasselt')
 - 160 Truck_20_buy + 160 Truck_20_sell >= 0
Truck_2_time_check: - 5 Route_2_('Anvers',_'Liege')
 - 5 Route_2_('Liege',_'Anvers')
 - 4.85714285714 Route_2_('Liege',_'Bruxelles')
 - 4.85714285714 Route_2_('Liege',_'Charleroi') - 6 Route_2_('Liege',_'Gand')
 - 3.71428571429 Route_2_('Liege',_'Hasselt') - 160 Truck_2_buy
 + 160 Truck_2_sell >= 0
Truck_3_time_check: - 5 Route_3_('Anvers',_'Liege')
 - 5 Route_3_('Liege',_'Anvers')
 - 4.85714285714 Route_3_('Liege',_'Bruxelles')
 - 4.85714285714 Route_3_('Liege',_'Charleroi') - 6 Route_3_('Liege',_'Gand')
 - 3.71428571429 Route_3_('Liege',_'Hasselt') - 160 Truck_3_buy
 + 160 Truck_3_sell >= 0
Truck_4_time_check: - 5 Route_4_('Anvers',_'Liege')
 - 5 Route_4_('Liege',_'Anvers')
 - 4.85714285714 Route_4_('Liege',_'Bruxelles')
 - 4.85714285714 Route_4_('Liege',_'Charleroi') - 6 Route_4_('Liege',_'Gand')
 - 3.71428571429 Route_4_('Liege',_'Hasselt') - 160 Truck_4_buy
 + 160 Truck_4_sell >= 0
Truck_5_time_check: - 5 Route_5_('Anvers',_'Liege')
 - 5 Route_5_('Liege',_'Anvers')
 - 4.85714285714 Route_5_('Liege',_'Bruxelles')
 - 4.85714285714 Route_5_('Liege',_'Charleroi') - 6 Route_5_('Liege',_'Gand')
 - 3.71428571429 Route_5_('Liege',_'Hasselt') - 160 Truck_5_buy
 + 160 Truck_5_sell >= 0
Truck_6_time_check: - 5 Route_6_('Anvers',_'Liege')
 - 5 Route_6_('Liege',_'Anvers')
 - 4.85714285714 Route_6_('Liege',_'Bruxelles')
 - 4.85714285714 Route_6_('Liege',_'Charleroi') - 6 Route_6_('Liege',_'Gand')
 - 3.71428571429 Route_6_('Liege',_'Hasselt') - 160 Truck_6_buy
 + 160 Truck_6_sell >= 0
Truck_7_time_check: - 5 Route_7_('Anvers',_'Liege')
 - 5 Route_7_('Liege',_'Anvers')
 - 4.85714285714 Route_7_('Liege',_'Bruxelles')
 - 4.85714285714 Route_7_('Liege',_'Charleroi') - 6 Route_7_('Liege',_'Gand')
 - 3.71428571429 Route_7_('Liege',_'Hasselt') - 160 Truck_7_buy
 + 160 Truck_7_sell >= 0
Truck_8_time_check: - 5 Route_8_('Anvers',_'Liege')
 - 5 Route_8_('Liege',_'Anvers')
 - 4.85714285714 Route_8_('Liege',_'Bruxelles')
 - 4.85714285714 Route_8_('Liege',_'Charleroi') - 6 Route_8_('Liege',_'Gand')
 - 3.71428571429 Route_8_('Liege',_'Hasselt') - 160 Truck_8_buy
 + 160 Truck_8_sell >= 0
Truck_9_time_check: - 5 Route_9_('Anvers',_'Liege')
 - 5 Route_9_('Liege',_'Anvers')
 - 4.85714285714 Route_9_('Liege',_'Bruxelles')
 - 4.85714285714 Route_9_('Liege',_'Charleroi') - 6 Route_9_('Liege',_'Gand')
 - 3.71428571429 Route_9_('Liege',_'Hasselt') - 160 Truck_9_buy
 + 160 Truck_9_sell >= 0
Bounds
0 <= Route_10_('Anvers',_'Liege')
0 <= Route_10_('Liege',_'Anvers')
0 <= Route_10_('Liege',_'Bruxelles')
0 <= Route_10_('Liege',_'Charleroi')
0 <= Route_10_('Liege',_'Gand')
0 <= Route_10_('Liege',_'Hasselt')
0 <= Route_11_('Anvers',_'Liege')
0 <= Route_11_('Liege',_'Anvers')
0 <= Route_11_('Liege',_'Bruxelles')
0 <= Route_11_('Liege',_'Charleroi')
0 <= Route_11_('Liege',_'Gand')
0 <= Route_11_('Liege',_'Hasselt')
0 <= Route_12_('Anvers',_'Liege')
0 <= Route_12_('Liege',_'Anvers')
0 <= Route_12_('Liege',_'Bruxelles')
0 <= Route_12_('Liege',_'Charleroi')
0 <= Route_12_('Liege',_'Gand')
0 <= Route_12_('Liege',_'Hasselt')
0 <= Route_13_('Anvers',_'Liege')
0 <= Route_13_('Liege',_'Anvers')
0 <= Route_13_('Liege',_'Bruxelles')
0 <= Route_13_('Liege',_'Charleroi')
0 <= Route_13_('Liege',_'Gand')
0 <= Route_13_('Liege',_'Hasselt')
0 <= Route_14_('Anvers',_'Liege')
0 <= Route_14_('Liege',_'Anvers')
0 <= Route_14_('Liege',_'Bruxelles')
0 <= Route_14_('Liege',_'Charleroi')
0 <= Route_14_('Liege',_'Gand')
0 <= Route_14_('Liege',_'Hasselt')
0 <= Route_15_('Anvers',_'Liege')
0 <= Route_15_('Liege',_'Anvers')
0 <= Route_15_('Liege',_'Bruxelles')
0 <= Route_15_('Liege',_'Charleroi')
0 <= Route_15_('Liege',_'Gand')
0 <= Route_15_('Liege',_'Hasselt')
0 <= Route_16_('Anvers',_'Liege')
0 <= Route_16_('Liege',_'Anvers')
0 <= Route_16_('Liege',_'Bruxelles')
0 <= Route_16_('Liege',_'Charleroi')
0 <= Route_16_('Liege',_'Gand')
0 <= Route_16_('Liege',_'Hasselt')
0 <= Route_17_('Anvers',_'Liege')
0 <= Route_17_('Liege',_'Anvers')
0 <= Route_17_('Liege',_'Bruxelles')
0 <= Route_17_('Liege',_'Charleroi')
0 <= Route_17_('Liege',_'Gand')
0 <= Route_17_('Liege',_'Hasselt')
0 <= Route_18_('Anvers',_'Liege')
0 <= Route_18_('Liege',_'Anvers')
0 <= Route_18_('Liege',_'Bruxelles')
0 <= Route_18_('Liege',_'Charleroi')
0 <= Route_18_('Liege',_'Gand')
0 <= Route_18_('Liege',_'Hasselt')
0 <= Route_19_('Anvers',_'Liege')
0 <= Route_19_('Liege',_'Anvers')
0 <= Route_19_('Liege',_'Bruxelles')
0 <= Route_19_('Liege',_'Charleroi')
0 <= Route_19_('Liege',_'Gand')
0 <= Route_19_('Liege',_'Hasselt')
0 <= Route_1_('Anvers',_'Liege')
0 <= Route_1_('Liege',_'Anvers')
0 <= Route_1_('Liege',_'Bruxelles')
0 <= Route_1_('Liege',_'Charleroi')
0 <= Route_1_('Liege',_'Gand')
0 <= Route_1_('Liege',_'Hasselt')
0 <= Route_20_('Anvers',_'Liege')
0 <= Route_20_('Liege',_'Anvers')
0 <= Route_20_('Liege',_'Bruxelles')
0 <= Route_20_('Liege',_'Charleroi')
0 <= Route_20_('Liege',_'Gand')
0 <= Route_20_('Liege',_'Hasselt')
0 <= Route_2_('Anvers',_'Liege')
0 <= Route_2_('Liege',_'Anvers')
0 <= Route_2_('Liege',_'Bruxelles')
0 <= Route_2_('Liege',_'Charleroi')
0 <= Route_2_('Liege',_'Gand')
0 <= Route_2_('Liege',_'Hasselt')
0 <= Route_3_('Anvers',_'Liege')
0 <= Route_3_('Liege',_'Anvers')
0 <= Route_3_('Liege',_'Bruxelles')
0 <= Route_3_('Liege',_'Charleroi')
0 <= Route_3_('Liege',_'Gand')
0 <= Route_3_('Liege',_'Hasselt')
0 <= Route_4_('Anvers',_'Liege')
0 <= Route_4_('Liege',_'Anvers')
0 <= Route_4_('Liege',_'Bruxelles')
0 <= Route_4_('Liege',_'Charleroi')
0 <= Route_4_('Liege',_'Gand')
0 <= Route_4_('Liege',_'Hasselt')
0 <= Route_5_('Anvers',_'Liege')
0 <= Route_5_('Liege',_'Anvers')
0 <= Route_5_('Liege',_'Bruxelles')
0 <= Route_5_('Liege',_'Charleroi')
0 <= Route_5_('Liege',_'Gand')
0 <= Route_5_('Liege',_'Hasselt')
0 <= Route_6_('Anvers',_'Liege')
0 <= Route_6_('Liege',_'Anvers')
0 <= Route_6_('Liege',_'Bruxelles')
0 <= Route_6_('Liege',_'Charleroi')
0 <= Route_6_('Liege',_'Gand')
0 <= Route_6_('Liege',_'Hasselt')
0 <= Route_7_('Anvers',_'Liege')
0 <= Route_7_('Liege',_'Anvers')
0 <= Route_7_('Liege',_'Bruxelles')
0 <= Route_7_('Liege',_'Charleroi')
0 <= Route_7_('Liege',_'Gand')
0 <= Route_7_('Liege',_'Hasselt')
0 <= Route_8_('Anvers',_'Liege')
0 <= Route_8_('Liege',_'Anvers')
0 <= Route_8_('Liege',_'Bruxelles')
0 <= Route_8_('Liege',_'Charleroi')
0 <= Route_8_('Liege',_'Gand')
0 <= Route_8_('Liege',_'Hasselt')
0 <= Route_9_('Anvers',_'Liege')
0 <= Route_9_('Liege',_'Anvers')
0 <= Route_9_('Liege',_'Bruxelles')
0 <= Route_9_('Liege',_'Charleroi')
0 <= Route_9_('Liege',_'Gand')
0 <= Route_9_('Liege',_'Hasselt')
0 <= Truck_10_buy <= 12
0 <= Truck_10_sell <= 12
0 <= Truck_11_buy <= 12
0 <= Truck_11_sell <= 12
0 <= Truck_12_buy <= 12
0 <= Truck_12_sell <= 12
0 <= Truck_13_buy <= 12
0 <= Truck_13_sell <= 12
0 <= Truck_14_buy <= 12
0 <= Truck_14_sell <= 12
0 <= Truck_15_buy <= 12
0 <= Truck_15_sell <= 12
0 <= Truck_16_buy <= 12
0 <= Truck_16_sell <= 12
0 <= Truck_17_buy <= 12
0 <= Truck_17_sell <= 12
0 <= Truck_18_buy <= 12
0 <= Truck_18_sell <= 12
0 <= Truck_19_buy <= 12
0 <= Truck_19_sell <= 12
0 <= Truck_1_buy <= 12
0 <= Truck_1_sell <= 12
0 <= Truck_20_buy <= 12
0 <= Truck_20_sell <= 12
0 <= Truck_2_buy <= 12
0 <= Truck_2_sell <= 12
0 <= Truck_3_buy <= 12
0 <= Truck_3_sell <= 12
0 <= Truck_4_buy <= 12
0 <= Truck_4_sell <= 12
0 <= Truck_5_buy <= 12
0 <= Truck_5_sell <= 12
0 <= Truck_6_buy <= 12
0 <= Truck_6_sell <= 12
0 <= Truck_7_buy <= 12
0 <= Truck_7_sell <= 12
0 <= Truck_8_buy <= 12
0 <= Truck_8_sell <= 12
0 <= Truck_9_buy <= 12
0 <= Truck_9_sell <= 12
Generals
Route_10_('Anvers',_'Liege')
Route_10_('Liege',_'Anvers')
Route_10_('Liege',_'Bruxelles')
Route_10_('Liege',_'Charleroi')
Route_10_('Liege',_'Gand')
Route_10_('Liege',_'Hasselt')
Route_11_('Anvers',_'Liege')
Route_11_('Liege',_'Anvers')
Route_11_('Liege',_'Bruxelles')
Route_11_('Liege',_'Charleroi')
Route_11_('Liege',_'Gand')
Route_11_('Liege',_'Hasselt')
Route_12_('Anvers',_'Liege')
Route_12_('Liege',_'Anvers')
Route_12_('Liege',_'Bruxelles')
Route_12_('Liege',_'Charleroi')
Route_12_('Liege',_'Gand')
Route_12_('Liege',_'Hasselt')
Route_13_('Anvers',_'Liege')
Route_13_('Liege',_'Anvers')
Route_13_('Liege',_'Bruxelles')
Route_13_('Liege',_'Charleroi')
Route_13_('Liege',_'Gand')
Route_13_('Liege',_'Hasselt')
Route_14_('Anvers',_'Liege')
Route_14_('Liege',_'Anvers')
Route_14_('Liege',_'Bruxelles')
Route_14_('Liege',_'Charleroi')
Route_14_('Liege',_'Gand')
Route_14_('Liege',_'Hasselt')
Route_15_('Anvers',_'Liege')
Route_15_('Liege',_'Anvers')
Route_15_('Liege',_'Bruxelles')
Route_15_('Liege',_'Charleroi')
Route_15_('Liege',_'Gand')
Route_15_('Liege',_'Hasselt')
Route_16_('Anvers',_'Liege')
Route_16_('Liege',_'Anvers')
Route_16_('Liege',_'Bruxelles')
Route_16_('Liege',_'Charleroi')
Route_16_('Liege',_'Gand')
Route_16_('Liege',_'Hasselt')
Route_17_('Anvers',_'Liege')
Route_17_('Liege',_'Anvers')
Route_17_('Liege',_'Bruxelles')
Route_17_('Liege',_'Charleroi')
Route_17_('Liege',_'Gand')
Route_17_('Liege',_'Hasselt')
Route_18_('Anvers',_'Liege')
Route_18_('Liege',_'Anvers')
Route_18_('Liege',_'Bruxelles')
Route_18_('Liege',_'Charleroi')
Route_18_('Liege',_'Gand')
Route_18_('Liege',_'Hasselt')
Route_19_('Anvers',_'Liege')
Route_19_('Liege',_'Anvers')
Route_19_('Liege',_'Bruxelles')
Route_19_('Liege',_'Charleroi')
Route_19_('Liege',_'Gand')
Route_19_('Liege',_'Hasselt')
Route_1_('Anvers',_'Liege')
Route_1_('Liege',_'Anvers')
Route_1_('Liege',_'Bruxelles')
Route_1_('Liege',_'Charleroi')
Route_1_('Liege',_'Gand')
Route_1_('Liege',_'Hasselt')
Route_20_('Anvers',_'Liege')
Route_20_('Liege',_'Anvers')
Route_20_('Liege',_'Bruxelles')
Route_20_('Liege',_'Charleroi')
Route_20_('Liege',_'Gand')
Route_20_('Liege',_'Hasselt')
Route_2_('Anvers',_'Liege')
Route_2_('Liege',_'Anvers')
Route_2_('Liege',_'Bruxelles')
Route_2_('Liege',_'Charleroi')
Route_2_('Liege',_'Gand')
Route_2_('Liege',_'Hasselt')
Route_3_('Anvers',_'Liege')
Route_3_('Liege',_'Anvers')
Route_3_('Liege',_'Bruxelles')
Route_3_('Liege',_'Charleroi')
Route_3_('Liege',_'Gand')
Route_3_('Liege',_'Hasselt')
Route_4_('Anvers',_'Liege')
Route_4_('Liege',_'Anvers')
Route_4_('Liege',_'Bruxelles')
Route_4_('Liege',_'Charleroi')
Route_4_('Liege',_'Gand')
Route_4_('Liege',_'Hasselt')
Route_5_('Anvers',_'Liege')
Route_5_('Liege',_'Anvers')
Route_5_('Liege',_'Bruxelles')
Route_5_('Liege',_'Charleroi')
Route_5_('Liege',_'Gand')
Route_5_('Liege',_'Hasselt')
Route_6_('Anvers',_'Liege')
Route_6_('Liege',_'Anvers')
Route_6_('Liege',_'Bruxelles')
Route_6_('Liege',_'Charleroi')
Route_6_('Liege',_'Gand')
Route_6_('Liege',_'Hasselt')
Route_7_('Anvers',_'Liege')
Route_7_('Liege',_'Anvers')
Route_7_('Liege',_'Bruxelles')
Route_7_('Liege',_'Charleroi')
Route_7_('Liege',_'Gand')
Route_7_('Liege',_'Hasselt')
Route_8_('Anvers',_'Liege')
Route_8_('Liege',_'Anvers')
Route_8_('Liege',_'Bruxelles')
Route_8_('Liege',_'Charleroi')
Route_8_('Liege',_'Gand')
Route_8_('Liege',_'Hasselt')
Route_9_('Anvers',_'Liege')
Route_9_('Liege',_'Anvers')
Route_9_('Liege',_'Bruxelles')
Route_9_('Liege',_'Charleroi')
Route_9_('Liege',_'Gand')
Route_9_('Liege',_'Hasselt')
Truck_10_buy
Truck_10_sell
Truck_11_buy
Truck_11_sell
Truck_12_buy
Truck_12_sell
Truck_13_buy
Truck_13_sell
Truck_14_buy
Truck_14_sell
Truck_15_buy
Truck_15_sell
Truck_16_buy
Truck_16_sell
Truck_17_buy
Truck_17_sell
Truck_18_buy
Truck_18_sell
Truck_19_buy
Truck_19_sell
Truck_1_buy
Truck_1_sell
Truck_20_buy
Truck_20_sell
Truck_2_buy
Truck_2_sell
Truck_3_buy
Truck_3_sell
Truck_4_buy
Truck_4_sell
Truck_5_buy
Truck_5_sell
Truck_6_buy
Truck_6_sell
Truck_7_buy
Truck_7_sell
Truck_8_buy
Truck_8_sell
Truck_9_buy
Truck_9_sell
End
