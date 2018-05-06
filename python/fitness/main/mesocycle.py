import datetime

MESOCYCLES = {
        
    "bls" :[
        "normal",
        "normal",
        "normal",
        "strength_a",
        "normal",
        "normal",
        "normal",
        "strength_b",
        "deload"],
    "bbls": [
        "normal",
        "normal",
        "normal",
        "normal",
        "power",
        "deload"],
    "custom": [
        "normal",
        "normal",
        "normal",
        "normal",
        "body_build",
        "deload"]
}


def print_program(start, end, mesocycle, euro_date=False):
    """
    Displays a week by breakdown of an exercise program

    :param start: program start date
    :type start: instance of <class 'datetime.datetime'>
    :param end: program end date
    :type end: instance of <class 'datetime.datetime'>
    :param mesocycle: list of mesocycle week types like:
        [normal, normal, strength, delaod]
    :type mesocycle: list
    :param euro_date: option to use european date displays
    :type euro_date: bool
    :return: n/a
    :rtype: n/a
    """
    duration = end - start
    num_weeks = duration.days / 7

    # get the number of weeks in the mesocycle
    meso_length = len(mesocycle)
    delta_week = datetime.timedelta(days=7)

    # display information
    for i in range(num_weeks):

        index = divmod(i, meso_length)[1]
        week_type = mesocycle[index]
        
        week_str = start.strftime("[%a] %m/%d/%Y")
        if euro_date:            
            week_str = start.strftime("[%a] %d/%m/%Y")
        if index == 0:
            print
        print "{}:  {}".format(week_str, week_type)
        
        # increment
        start = start + delta_week

if __name__ == "__main__":
    start = datetime.datetime(year=2018, month=03, day=05)
    end = start + datetime.timedelta(days=365)
    mesocycle = MESOCYCLES.get("bls")
    print_program(start, end, mesocycle)