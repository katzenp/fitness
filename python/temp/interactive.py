workout = {
    'curl_barbell': (90, 3, 85, 5, 85, 5),
    'close_grip_bench': (160, 6, 170, 4, 170, 4),
    'curl_dumbell': (35, 6, 35, 6, 40, 3),
    'skull_crusher': (95, 4, 95, 4, 95, 4),
    'curl_bumbell_recline': (25, 10, 25, 9, 25, 8),
    'tricep_extensions_cable': (105, 10, 110, 8, 110, 8)
}

total_volume = 0
for name, set_data in workout.iteritems():
    for i in range(0, len(set_data), 2):
        total_volume += (set_data[i] * set_data[i + 1])
print total_volume