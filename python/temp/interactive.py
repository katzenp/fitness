import datetime


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

bls = [
    "normal",
    "normal",
    "normal",
    "strength_a",
    "normal",
    "normal",
    "normal",
    "strength_b",
    "deload",
]
bbls = [
    "normal",
    "normal",
    "normal",
    "normal",
    "power",
    "deload",
]

def get_mesocycle(start=None, end=None, mesocyle=bls):
    # get star / end date
    if not start:
        start = datetime.datetime.today()
    if not end:
        end = start + datetime.timedelta(years=1)

    # get mesocycle lendth
    meso_length = len(mesocyle)


    # caclculate it !
    wk_num = 0
    count = 0
    delta = datetime.timedelta(days=1)
    while True:
        if start.date() == end.date():
            break
        
        # get the week number
        w = divmod(count, 7)[0]
        if w != wk_num:
            print '-' * 80
            wk_num = w

        # calculate mesocycle week type
        i = divmod(w, meso_length)[-1]
        wk_type = mesocyle[i]
        
        # report details
        date_str = start.strftime("[%a]%d/%m/%Y")
        print "{date_str} - {week_type}".format(date_str=date_str, week_type=wk_type)
        
        # increment
        start = start + delta
        count += 1

start = datetime.datetime(year=2018, month=01, day=01)
end = datetime.datetime.today()
get_mesocycle(start, end, mesocyle=bls)