"""
skulpt.py

Description:
    Skulpt-Chzl body fat data parsing
"""
import datetime
import os
import re
import pprint

import python.resources as resources


def get_csv_data(cache):
    """
    Time,Muscle,Side,MQ(0-100),MQ(raw),Fat %
    2018-04-01T06:55:01.050Z, upper_back, l, 98.59659, 154.39984, 8

    :param cache:
    :type cache:
    :return:
    :rtype:
    """
    data = {}
    date = None
    for line in open(cache, "r"):
        line = re.sub("\s", "", line)
        if not line or line .startswith("Time"):
            continue

        ts,muscle,side,mqa,mqb,bfp = line.split(",")
        muscle_name = "{}_{}".format(side, muscle)

        date = ts.split(":", 1)[0][:-3]
        if date not in data:
            data[date] = {}
        data[date][muscle_name] = float(bfp)

    return data


def get_bf(cache, date=None):
    if not date:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
    data = get_csv_data(cache)

    bf_data = data[date]
    bf_min = None
    bf_max = None
    count = 0
    bf_avg = 0
    for name, value in bf_data.iteritems():
        bf_avg += value
        if count == 0:
            bf_min = value
            bf_max = value

        if value < bf_min:
            bf_min = value
        if value > bf_max:
            bf_max = value

        count += 1
    bf_avg /= count
    min_max_avg = (bf_min + bf_max) / 2.0

    return bf_min, bf_max, min_max_avg, bf_avg


if __name__ == "__main__":
    date = datetime.datetime.today()
    date_str = date.strftime("%Y-%m-%d")
    msg = """{}\n\t{} - {} ~ {}\n\tAvg: {}
    """.format(
        date_str,
        *get_bf(resources.SKULPT_CACHE, date=date_str)
        )
    print(msg)