"""
bodyWeight.py

Description:
    tools and utilities for calcluating various body weight metrics
    used for tracking personal fitness goals
"""
# ==============================================================================
# Dependencies
# ==============================================================================
import datetime
import json
import os


# ==============================================================================
# Constants/Globals
# ==============================================================================
KATCH_MCARDLE_MODIFIERS = {"inactive": 1.00,
                           "light": 1.20,
                           "moderate": 1.35,
                           "heavy": 1.50}


# ==============================================================================
# General Functions
# ==============================================================================
def getWeightData(weight, body_fat, km_factor=1.35, weight_units='lbs'):
    """
    Retruns a dictionary of weight data containing the following information:
        weight: your body weight expressed in kg
        bf: body fat percentage
        lbm: lean/ non-fat body mass expressecd in kg
        bmr: number of calories you burn each day EXCLUDING exercise
        tdee: number of calories you burn each day INCLUDING exercise
              based on the Katch McArdle formula.
              tdee = bmr * km_factor/factor

    :param weight: your weight given in the units specified by `weight_units`
    :type weight: float
    :param body_fat: your body fat percentage
    :type body_fat: int
    :param km_factor: number used to adjust your basal metabolic rate to reflect
                      calories burned through exercise
    :type km_factor: float in range 1.0 - 1.50
    :param weight_units: the unit of measurement for calculating your weight
                         Must be either 'lbs' or 'kg'. Please note that all
                         weight data returned by this algorithm will be in kg
    :type weight_units: {'lbs', 'kg'}
    :return: weight management data
    :rtype: dictionary
            {'weight': float,
             'bf': float,
             'lbm': float,
             'bmr': float,
             'tdee': float}
    """
    # convert weight to kg if necessary
    if weight_units == 'lbs':
        weight /= 2.2

    # calculate lean body mass
    lbm = weight * ((100.00 - body_fat) / 100.00)

    # calculate basal metabolic rate
    bmr = 370 + (21.6 * lbm)

    # calculate total daily energy expenditure
    if not 1.00 <= km_factor <= 1.50:
        raise ValueError("Katct McArdle factor must be in range 1.00 - 1.50")
    tdee = bmr * km_factor

    return {'weight': round(weight, 2),
            'bf': round(body_fat, 2),
            'lbm': round(lbm, 2),
            'bmr': round(bmr, 2),
            'activeness': round(km_factor, 2),
            'tdee': round(tdee, 2)}


def recordWeightData(weight, body_fat, km_factor=1.35, weight_units='lbs', rec_file=None):
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

    :param weight: your weight given in the units specified by `weight_units`
    :type weight: float
    :param body_fat: your body fat percentage
    :type body_fat: int
    :param km_factor: number used to adjust your basal metabolic rate to reflect
                      calories burned through exercise
    :type km_factor: float in range 1.0 - 1.50
    :param weight_units: the unit of measurement for calculating your weight
                         Must be either 'lbs' or 'kg'. Please note that all
                         weight data returned by this algorithm will be in kg
    :type weight_units: {'lbs', 'kg'}
    :param rec_file: name of the metadata file to write data out to
    :type rec_file: string
    :return: today's weight data and the name of the metadata file
    :rtype: tuple
            ({}, "weight_record_filepath")
    """
    # check parameters
    if not rec_file:
        raise IOError("No weight record specified.")

    # get current weight data records
    data = {}
    if os.path.isfile(rec_file):
        with open(rec_file, 'r') as infile:
            try:
                data = json.load(infile)
            except:
                data = {}

    # update weight data records
    with open(rec_file, 'w') as outfile:
        weight_data = getWeightData(weight, body_fat, km_factor, weight_units)
        today = datetime.date.today().strftime("%Y-%m-%d")
        data[today] = weight_data
        json.dump(data, outfile, indent=4)

    return weight_data, rec_file


# ==============================================================================
# Interactive session
# ==============================================================================
if __name__ == '__main__':
    # create weight record
    RECORD_FILE = r"C:\Users\pkatzen\Desktop\weigh_in.json"
    data, filepath = recordWeightData(134.2, 5, 1.35, "lbs", RECORD_FILE)
    print("Weight record written to:\n\t{0}".format(filepath))

    # create weight log
    LOG_FILE = r"C:\Users\pkatzen\Desktop\weight.log"
    with open(LOG_FILE, "w") as ofile:
        msg = "{0}\n".format("-" * 30)
        msg += "{0}\n".format(datetime.date.today())
        msg += "{0}\n".format("-" * 30)
        for k in ["weight", "bf", "lbm", "bmr", "activeness", "tdee"]:
            tmp = "{0:12s}: {1}\n".format(k.upper(), data.get(k))
            msg += tmp
        msg += "{0}\n".format("-" * 30)
        msg += "{0:12s}: {1}\n".format("CUT  (-500)", data.get('tdee') - 500)
        msg += "{0:12s}: {1}\n".format("GAIN (+500)", data.get('tdee') + 500)
        msg += "{0}\n".format("-" * 30)
        print msg
        ofile.write(msg)
    print("Weight log written to:\n\t{0}".format(LOG_FILE))
