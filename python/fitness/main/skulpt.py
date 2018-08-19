#! /usr/bin/python
"""
skulpt.py

Description:
    Tools and utilities for managing Skulpt-Chzl body fat scanner data 
"""
# Python standard libraries
import argparse
import datetime
import json
import os
import re

# Local libraries
import fitness


# ==============================================================================
# constants / globals
# ==============================================================================
SKULPT_CACHE = os.path.join(fitness.CACHES, "skulpt.csv")
DATE_FORMAT = fitness.SETTINGS.get("date_format")
REPORT = """{date}
    min       {min_:4.2f}
    max       {max_:4.2f}
    mm_avg    {min_max_avg:4.2f}
    avg       {avg:4.2f}
"""


# ==============================================================================
# general
# ==============================================================================
def get_body_fat_data(sourcefile):
    """
    Returns body fat measurements by date and body part as defined by the given sourcefile file.

    The source file should be a csv file with the following format:
        Time, Muscle, Side, MQ(0-100), MQ(raw), Fat_%
        // 2018-04-01T06:55:01.050Z, upper_back, l, 98.59659, 154.39984, 8

    Body fat data is returned in a dictionary with the following format:
        {
            'YYYY-MM-DD', {
                'body_part': int,
                ...'
                },
            ...
        }
    :param sourcefile: full file path to a body fat measurement data file
    :type sourcefile: string
    :return: date and body part centric body fat measurements
    :rtype: dictionary
    """
    data = {}
    date = None
    for line in open(sourcefile, "r"):
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


def get_body_fat(year, month, day, sourcefile):
    """
    Returns body fat measurement data for a specific date from the given sourcefile file.

    The following values are returned:
        bf_min: lowest body fat value
        bf_max: highest body fat value
        min_max_avg: average of lowest and highest (lowest + highest / 2)
        bf_avg: average of ALL available measurements

    :param year: the year you wish to query
    :type year: int
    :param month: the month you wish to query
    :type month: int
    :param day: the day you wish to query
    :type day: int
    :param sourcefile: full file path to a skulpt.csv file
    :type sourcefile: string
    :return: body fat data like: (bf_min, bf_max, min_max_avg, bf_avg)
    :rtype: tuple
    """
    # get date centric data
    data = get_body_fat_data(sourcefile)
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


# ==============================================================================
# main
# ==============================================================================
def main():
    """
    Command line entry point function

    :return: N/A
    :rvalue: N/A
    """
    # date time
    TODAY = datetime.datetime.today()

    # define argument parser
    DESCRIPTION = """
    Prints out body fat data for the given date based on a Skulpt cache
    """
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION)

    # add command line args
    parser.add_argument(
        "-y", "--year",
        action="store",
        default=TODAY.year,
        type=str,
        help="The year",
        metavar=""
    )

    parser.add_argument(
        "-m", "--month",
        action="store",
        default=TODAY.month,
        type=str,
        help="The month",
        metavar=""
    )

    parser.add_argument(
        "-d", "--day",
        action="store",
        default=TODAY.day,
        type=str,
        help="The day",
        metavar=""
    )

    parser.add_argument(
        "-s", "--sourcefile",
        action="store",
        default=SKULPT_CACHE,
        type=str,
        help="Skulpt cache file (.csv)",
        metavar=""
    )

    # pares arguments
    args = parser.parse_args()
    year = args.year
    month = args.month
    day = args.day

    # print report
    sourcefile = args.sourcefile
    data = get_body_fat(year, month, day, sourcefile)
    date = DATE_FORMAT.format(year=year, month=month, day=day)
    msg = REPORT.format(
        date=date, min_=data[0], max_=data[1], min_max_avg=data[2], avg=data[3]
    )
    print(msg)


if __name__ == "__main__":
    main()
