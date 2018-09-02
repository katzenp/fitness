"""
bodyweight.py

Description:
    Tools and utilities for managing the body weight statistics used to track
    personal fitness goals. All algorithms in this module use the metric system
"""
# Python standard libraries
import datetime
import json
import os
import time

# local libraries
from fitness import SETTINGS


# ==============================================================================
# macronutrients
# ==============================================================================
def macro_calories(carbohydrate, fat, protein):
    """
    returns a list of macronutrient calories based on the specified
    macronutrient gram amounts.
        
    :param carbohydrate: amount of carbohydrate given grams
    :type carbohydrate: float, int
    :param fat: amount of fat given grams
    :type fat: float, int
    :param protein: amount of protein given grams
    :type protein: float, int
    :return: macronutrient calories like: (carb_calories, fat_calories, protein_calories)
    :rtype: tuple
    """
    carbohydrate *= SETTINGS["macro_calories"]["carbohydrate"]    
    fat *= SETTINGS["macro_calories"]["fat"]    
    protein *= SETTINGS["macro_calories"]["protein"]
    return (carbohydrate, fat, protein)


def goal_macros(weight_kg):
    """
    Returns the amount of each macronutrient that should be consumed daily
    for each of the following weight management goals:
        cut, maintain, bulk

    Return Value Details
        {   
            "goal": {
                "carbohydrate": amount_grams,
                "fat": amount_grams,
                "protein": amount_grams
            },
            ...
        }

    :param weight_kg: weight in kilograms
    :type weight_kg: float
    :return: macronutrient grams by goal
    :rtype: dict
    """
    macro_multipliers = SETTINGS["macro_multipliers"]
    data = {}
    for goal in ("cut", "maintain", "bulk"):
        data[goal] = {} 
        for macro in ("carbohydrate", "fat", "protein"):
            data[goal][macro] = (weight_kg * 2.2) * macro_multipliers[goal][macro]

    return data
 

def bmi(weight_kg, height_cm):
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
    bmi = weight_kg / ((height_cm * 0.01) ** 2)
    return bmi, precision


# ==============================================================================
# bmr
# ==============================================================================
def bmr_harrisBenedict(height_cm, weight_kg, age, male=True):
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


def bmr_mifflinStJeor(height_cm, weight_kg, age, male=True):
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


def bmr_katchMcArdle(weight_kg, body_fat):
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


def bmr(height_cm, weight_kg, age, body_fat, male=True, equation=None):
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
        return bmr_harrisBenedict(height_cm, weight_kg, age, male)
    elif equation == 'mifflinStJeor':
        return  bmr_mifflinStJeor(height_cm, weight_kg, age, male)
    elif equation == 'katchMcArdle':
        return bmr_katchMcArdle(weight_kg, body_fat)
    else:
        average = bmr_harrisBenedict(height_cm, weight_kg, age, male)
        average += bmr_mifflinStJeor(height_cm, weight_kg, age, male)
        average += bmr_katchMcArdle(weight_kg, body_fat)
        return average / 3.0


# ==============================================================================
# weight
# ==============================================================================
def get_weight_data(height_cm, weight_kg, age, body_fat, male=True, equation=None, modifier=1.2):
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
    bmr = bmr(height_cm, weight_kg, age, body_fat, male, equation)

    # calculate total daily energy expenditure
    tdee = bmr * modifier

    return {'weight': weight_kg,
            'bf': body_fat,
            'lbm': lbm_kg,
            'bmr': bmr,
            'activeness': modifier,
            'tdee': tdee}


def update_weight_log(height_cm, weight_kg, age, body_fat, male=True, equation='katchMcArdle', modifier=1.2, outputfile=None):
    """
    Adds the weight data to the specified outputfile file
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
    :param outputfile: name of the file to write data out to
    :type outputfile: string
    :return: today's weight data and the output file name: ({}, "outputfile")
    :rtype: tuple    
    """
    # check parameters
    if not outputfile:
        raise IOError("No weight record file specified.")

    # get current weight data records
    data = {}
    if os.path.isfile(outputfile):
        with open(outputfile, 'r') as infile:
            try:
                data = json.load(infile)
            except Exception:
                data = {}

    # update weight data records
    weight_data = {}
    timestamp = time.time()
    with open(outputfile, 'w') as outfile:
        weight_data = get_weight_data(
            height_cm, weight_kg, age, body_fat, male, equation, modifier
        )
        data[timestamp] = weight_data
        json.dump(data, outfile, indent=4)

    return (weight_data, outputfile)
