"""
program.py

Description:
    Tools and utilities for managing various workout programs
"""
# Python standard libraries
import datetime


# ==============================================================================
# constnts/globals
# ==============================================================================
PROGRAMS = {
    "bls" : (
        "normal",
        "normal",
        "normal",
        "strength_a",
        "normal",
        "normal",
        "normal",
        "strength_b",
        "deload"
    ),
    "bbls": (
        "normal",
        "normal",
        "normal",
        "normal",
        "power",
        "deload"
    ),
    "default":  (
        ("normal", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest")),
        ("normal", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest")),
        ("normal", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest")),
        ("normal", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest")),
        ("strength", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest")),
        ("deload", ("shoulders", "back", "chest", "legs", "arms", "rest", "rest"))
    )
}


# ==============================================================================
# general
# ==============================================================================
def print_program(start, end, mesocycle, date_format="[%a] %m/%d/%Y"):
    """
    Displays a week by breakdown of an exercise program

    :param start: program start date
    :type start: instance of <class 'datetime.datetime'>
    :param end: program end date
    :type end: instance of <class 'datetime.datetime'>
    :param mesocycle: list of mesocycle week types like: [normal, normal, strength, delaod]
    :type mesocycle: list
    :return: n/a
    :rtype: n/a
    """
    duration = end - start
    num_weeks = duration.days / 7

    # get the number of weeks in the mesocycle
    meso_length = len(mesocycle)
    delta_week = datetime.timedelta(days=7)
    delta_day = datetime.timedelta(days=1)

    # display information
    print("-" * 80)
    for i in range(num_weeks):
        index = divmod(i, meso_length)[1]
        week_type, days = mesocycle[index]
        for workout_type in days:
            date_str = start.strftime(date_format)
            line = "{}: [{}] {}".format(date_str, week_type, workout_type)
            print(line)
            start = start + delta_day
        print("-" * 80)
        if index == (meso_length - 1):
            print(" ** ")
            print("-" * 80)
        

if __name__ == "__main__":
    start = datetime.datetime(year=2018, month=03, day=05)
    end = start + datetime.timedelta(days=365)
    print_program(start, end, PROGRAMS["default"], date_format="[%a] %m/%d/%Y")
