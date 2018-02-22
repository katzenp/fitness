"""
skulpt.py

Description:
    Module description
"""
import re


SKULPT_CACHE = r"/Users/paulk/Desktop/skulpt.csv"


def parse_data(cache=SKULPT_CACHE):
    # parse csv data
    data = {}
    previous_date = None
    fat_total = 0.0
    muscle_count = 1.0
    for line in open(cache, "r"):
        line = re.sub("\s|T.+Z", "", line)
        
        date, muscle, side, mq_percent, mq_raw, fat = line.lower().split(",")
        if not re.search("^[0-9]", date):
            continue

        if date not in data:
            if previous_date:
                data[previous_date]["fat_average"] = fat_total / muscle_count
            data[date] = {}
            previous_date = date
            fat_total = 0.0
            muscle_count = 1
            
        muscle = "{}_{}".format(muscle, side)
        fat = eval(fat)
        data[date][muscle] = fat
        fat_total += fat
        muscle_count += 1

    return data


def iter_bf_data(cache=SKULPT_CACHE, margin=2.0):
    data = parse_data(cache=SKULPT_CACHE)
    for date, metrics in sorted(data.iteritems()):
        fat = metrics.get("fat_average", 0.0)
        low = round(fat, 2)
        high = low + margin
        mid = (low + high) / 2.0
        yield date, low, high, mid


if __name__ == "__main__":
    # display data
    for date, low, high, avg in iter_bf_data(SKULPT_CACHE):
        print "{}: {}% - {}% [{}%]".format(date, low, high, avg)

