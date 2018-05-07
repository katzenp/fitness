"""
skulpt.py

Description:
    Skulpt-Chzl body fat data parsing
"""
# Python standard libraries
import datetime
import os
import re
import pprint

# Local libraries
import fitness.resources as resources


# ==============================================================================
# constants / globals
# ==============================================================================
DATE_FORMAT = "{year:04d}-{month:02d}-{day:02d}"


# ==============================================================================
# general
# ==============================================================================
def get_csv_data(cache):
    """
    Returns body fat measurements by date and body part as defined by the given cache file.
    Data is returned as a dictionary with the following format:
    2018-04-01T06:55:01.050Z, upper_back, l, 98.59659, 154.39984, 8
        {
            'YYYY-MM-DD', {'body_part': int, ...'},
            ...
        }
    :param cache: full file path to a skulpt.csv file
    :type cache: string
    :return: date and body part centric body fat measurements
    :rtype: dictionary
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


def get_bf(cache, year, month, day):
    """
    Returns body fat measurement data for a specific date from the given skulpt
    cache file. The following values are returned:
        bf_min: lowest body fat value
        bf_max: highest body fat value
        min_max_avg: average of lowest and highest (lowest + highest / 2)
        bf_avg: average of ALL available measurements

    :param cache: full file path to a skulpt.csv file
    :type cache: string
    :param year: the year you wish to query
    :type year: int
    :param month: the month you wish to query
    :type month: int
    :param day: the day you wish to query
    :type day: int
    :return: body fat data --> (bf_min, bf_max, min_max_avg, bf_avg)
    :rtype: tuple
    """
    # get date centric data
    data = get_csv_data(cache)
    date = DATE_FORMAT.format(year=year, month=month, day=day)
    try:
        bf_data = data[date]
    except KeyError :
        msg = "No body fat measurements exist for date: {}".format(date)
        raise KeyError(msg)
    
    # parse data
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
    today = datetime.datetime.today()
    date = DATE_FORMAT.format(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    bf_data = get_bf(resources.SKULPT_CACHE, year=today.year, month=today.month, day=today.day)
    msg = """{}\n\t{} - {} ~ {}\n\tAvg: {}
    """.format(date, *bf_data)
    print(msg)