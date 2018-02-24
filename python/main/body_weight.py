"""
body_weight.py

Description:
    Tools and utilities for calcluating various body weight metrics
    with a focus on tracking personal fitness goals.
    The algorithms in this module use the metric system
"""
# Python libraries
import datetime
import json
import os
import time


# ==============================================================================
# Constants/Globals
# ==============================================================================
RECORDS_DIR = os.path.dirname(__file__)
RECORDS_DIR = os.path.join(RECORDS_DIR, "database", "records")
RECORD_FILE = os.path.join(RECORDS_DIR, "weigh_in.json")
LOG_FILE = os.path.join(RECORDS_DIR, "weight.log")

BMR_EQUATIONS = ["harrisBenedict",
                 "mifflinStJeor",
                 "katchMcArdle"]
MODIFIERS = {"inactive": 1.00,
             "light": 1.20,
             "moderate": 1.35,
             "heavy": 1.50}


# ==============================================================================
# General
# ==============================================================================
def getMacrosData(weight_kg):
    """
    Calculates macronitrient and total calorie intake for cutting, maintaining,
    and bulking based on the given body weight

    :param weight_kg: current bodyweight in kilograms
    :type weight_kg: float
    :return: macronutrient calorie intake values
    :rtype: dictionary
            {"cut": {"protein": float,
                     "carbs": float,
                     "fat": float,
                     "total": float},
             "maintain": {"protein": float,
                          "carbs": float,
                          "fat": float,
                          "total": float},
             "bulk": {"protein": float,
                      "carbs": float,
                      "fat": float,
                      "total": float}}
    """
    # convert weight from metric
    weight_lbs = weight_kg * 2.2

    # define data structures
    macros = ("protein", "carbs", "fat")
    macro_cals = (4, 4, 9)
    macros_data = dict()

    # calculate cutting calories -----------------------------------------------
    data = {"total": 0.0}
    factors = (1.2, 1.0, 0.2)
    for i, each in enumerate(factors):
        # add grams of macros
        grams = weight_lbs * each
        data[macros[i]] = round(grams, 2)

        # calculate total calories
        cals = grams * macro_cals[i]
        cals = round(cals, 2)
        data["total"] += cals
    macros_data["cut"] = data

    # calculate maintenance calories -------------------------------------------
    data = {"total": 0.0}
    factors = (1.0, 1.6, 0.35)
    for i, each in enumerate(factors):
        # add grams of macros
        grams = weight_lbs * each
        data[macros[i]] = round(grams, 2)

        # calculate total calories
        cals = grams * macro_cals[i]
        cals = round(cals, 2)
        data["total"] += cals
    macros_data["maintain"] = data

    # calculate bulking calories -----------------------------------------------
    data = {"total": 0.0}
    factors = (1.0, 2.0, 0.4)
    for i, each in enumerate(factors):
        # add grams of macros
        grams = weight_lbs * each
        data[macros[i]] = round(grams, 2)

        # calculate total calories
        cals = grams * macro_cals[i]
        cals = round(cals, 2)
        data["total"] += cals
    macros_data["bulk"] = data

    data["total"] = round(data.get('total'))

    return macros_data


def getBmi(weight_kg, height_cm, precision=2):
    """
    Returns a Body Mass INdex value based on the weight and height

    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param height_cm: your height in centimeters
    :type height_cm: float
    :param precision: number of digits after the decimal point
    :type precision: int
    :return: body mas index value
    :rtype: float
    """
    bmi = weight_kg / ((height_cm * 0.01)**2)
    return round(bmi, precision)


def getBmr_harrisBenedict(height_cm, weight_kg, age, male=True):
    """
    Returns the basal metabolic rate calculated using the Harris-Benedict equation

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :return: basal metabolic rate
    :rtype: float
    """
    if male:
        bmr = (13.7 * weight_kg) + (5.0 * height_cm) - (6.8 * age) + 66
    else:
        bmr = (9.6 * weight_kg) + (1.8 * height_cm) - (4.7 * age) + 655

    return bmr


def getBmr_mifflinStJeor(height_cm, weight_kg, age, male=True):
    """
    Returns the basal metabolic rate calculated using the Mifflin-StJeor equation

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :return: basal metabolic rate
    :rtype: float
    """
    if male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + -161

    return bmr


def getBmr_katchMcArdle(weight_kg, body_fat):
    """
    Returns the basal metabolic rate calculated using the Katch-McArdle equation

    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param body_fat: your body fat percentage expressed as an integer
    :type body_fat: int
    :return: basal metabolic rate
    :rtype: float
    """
    leanBodyMass = weight_kg * ((100.00 - body_fat) / 100.00)
    bmr = (21.6 * leanBodyMass) + 370
    return bmr


def getBmr(height_cm, weight_kg, age, body_fat, male=True, equation=None):
    """
    Returns the basal metabolic rate calculated using one of the following equations:
        Harris-Benedict
        Mifflin-StJeor
        Katch-McArdle
    If no equation is specified then an average of all 3 equations is returned

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param body_fat: your body fat percentage expressed as an integer
    :type body_fat: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :param equation: name of  basal metabolic rate equation to use.
                     Must be one of the following:
                     'harrisBenedict', 'mifflinStJeor', 'katchMcArdle', or None
                     if None, an average value will be used 
    :type equation: string, None
    :return: basal metabolic rate
    :rtype: float
    """
    if equation == 'harrisBenedict':
        return getBmr_harrisBenedict(height_cm, weight_kg, age, male)
    elif equation == 'mifflinStJeor':
        return  getBmr_mifflinStJeor(height_cm, weight_kg, age, male)
    elif equation == 'katchMcArdle':
        return getBmr_katchMcArdle(weight_kg, body_fat)
    else:
        average = getBmr_harrisBenedict(height_cm, weight_kg, age, male)
        average += getBmr_mifflinStJeor(height_cm, weight_kg, age, male)
        average += getBmr_katchMcArdle(weight_kg, body_fat)
        return average / 3.0


def getWeightData(height_cm, weight_kg, age, body_fat, male=True, equation=None, modifier=1.2, precision=2):
    """
    Retruns a dictionary of weight data containing the following information:
        weight: your body weight expressed in kilograms
        bf: body fat percentage
        lbm: non-fat body weight expressecd in kilograms
        bmr: number of calories you burn each day EXCLUDING exercise
              based on the Katch McArdle formula.
        tdee: number of calories you burn each day INCLUDING exercise
             bmr * modifier

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param body_fat: your body fat percentage expressed as an integer
    :type body_fat: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :param equation: name of  basal metabolic rate equation to use.
                     Must be one of the following:
                     'harrisBenedict', 'mifflinStJeor', 'katchMcArdle', or None
                     if None, an average value will be used 
    :type equation: string, None
    :param modifier: number representing how physically active you are
                     Adjusts your basal metabolic rate to reflect the number of 
                     calories burned through exercise (total daily energy expenditure)
    :type modifier: float in range 1.0 - 1.50
    :param precision: number of digits after the decimal point for all data values
    :type precision: int
    :return: weight management data
    :rtype: dictionary
            {'weight': float,
             'bf': float,
             'lbm': float,
             'bmr': float,
             'tdee': float}
    """
    # calculate lean body mass
    lbm_kg = weight_kg * ((100.00 - body_fat) / 100.00)

    # calculate basal metabolic rate
    bmr = getBmr(height_cm, weight_kg, age, body_fat, male, equation)

    # calculate total daily energy expenditure
    tdee = bmr * modifier

    return {'weight': round(weight_kg, precision),
            'bf': round(body_fat, precision),
            'lbm': round(lbm_kg, precision),
            'bmr': round(bmr, precision),
            'activeness': round(modifier, precision),
            'tdee': round(tdee, precision)}


def recordWeightData(height_cm, weight_kg, age, body_fat, male=True, equation='katchMcArdle', modifier=1.2, precision=2, rec_file=None):
    """
    Records today's weight data to the specified file
    Weight data is collected into a dictionary containing the following information:
        weight: your body weight expressed in kg
        bf: body fat percentage
        lbm: lean/ non-fat body mass expressecd in kg
        bmr: number of calories you burn each day EXCLUDING exercise
        tdee: number of calories you burn each day INCLUDING exercise
              based on the Katch McArdle formula.
              tdee = bmr * km_factor/factor

    :param height_cm: your height in centimeters
    :type height_cm: float
    :param weight_kg: your current weight in kilograms
    :type weight_kg: float
    :param age: your age in years
    :type age: int
    :param body_fat: your body fat percentage expressed as an integer
    :type body_fat: int
    :param male: is the calculation being performed for a male?
    :type male: bool
    :param equation: name of  basal metabolic rate equation to use.
                     Must be one of the following:
                     'harrisBenedict', 'mifflinStJeor', 'katchMcArdle', or None
                     if None, an average value will be used 
    :type equation: string, None
    :param modifier: number representing how physically active you are
                     Adjusts your basal metabolic rate to reflect the number of 
                     calories burned through exercise (total daily energy expenditure)
    :type modifier: float in range 1.0 - 1.50
    :param precision: number of digits after the decimal point for all data values
    :type precision: int
    :param rec_file: name of the metadata file to write data out to
    :type rec_file: string
    :return: today's weight data and the name of the metadata file
    :rtype: tuple
            ({}, "weight_record_filepath")
    """
    # check parameters
    if not rec_file:
        raise IOError("No weight record file specified.")

    # get current weight data records
    data = {}
    if os.path.isfile(rec_file):
        with open(rec_file, 'r') as infile:
            try:
                data = json.load(infile)
            except Exception:
                data = {}

    # update weight data records
    weight_data = {}
    timestamp = time.time()
    with open(rec_file, 'w') as outfile:
        weight_data = getWeightData(height_cm,
                                    weight_kg,
                                    age,
                                    body_fat,
                                    male,
                                    equation,
                                    modifier,
                                    precision)
        data[timestamp] = weight_data
        json.dump(data, outfile, indent=4)

    return (weight_data, rec_file)


def main(height_cm, weight_kg, age, body_fat, male=True, equation='katchMcArdle', modifier=1.2, precision=2, recFile=RECORD_FILE, logFile=LOG_FILE):
    # create weight record -----------------------------------------------------
    data, filepath = recordWeightData(height_cm,
                                      weight_kg,
                                      age,
                                      body_fat,
                                      male,
                                      equation,
                                      modifier,
                                      precision,
                                      recFile)
    print("Weight record written to:\n\t{0}".format(filepath))

    # create weight log --------------------------------------------------------
    with open(LOG_FILE, "w") as ofile:
        msg = "{0}\n".format("-" * 30)
        msg += "{0}\n".format(datetime.date.today())
        msg += "{0}\n".format("-" * 30)

        # build weight metrics data
        for k in ["weight", "bf", "lbm", "bmr", "activeness", "tdee"]:
            tmp = "{0:12s}: {1}\n".format(k.upper(), data.get(k))
            msg += tmp

        # build calorie data
        macros_data = getMacrosData(weight_kg)
        msg += "{0}\n".format("-" * 30)

        cut = macros_data.get("cut", {}).get("total", 0.0)
        msg += "{0:12s}: {1}\n".format("CUT", cut)

        maintain = macros_data.get("maintain", {}).get("total", 0.0)
        msg += "{0:12s}: {1}\n".format("MAINTAIN", maintain)

        gain = macros_data.get("bulk", {}).get("total", 0.0)
        msg += "{0:12s}: {1}\n".format("GAIN", gain)

        msg += "{0}\n".format("-" * 30)

        ofile.write(msg)
    print("Weight log written to:\n\t{0}".format(LOG_FILE))


# ==============================================================================
# Interactive session
# ==============================================================================
if __name__ == '__main__':
    # weight_kg = weight_lbs * 0.454
    weight_kg = 129.6 * 0.454
    main(height_cm=162.56,
         weight_kg=weight_kg,
         age=40.0,
         body_fat=10.0,
         male=True,
         equation=None,
         modifier=1.2,
         precision=2,
         recFile=RECORD_FILE,
         logFile=LOG_FILE)
