"""
workout_utils.py

Description:
    Tools and utilities for managing the various elements of an individual workout
"""


# ==============================================================================
# general
# ==============================================================================
def get_warmup_weights(workweight, set_factors=(0.5, 0.5, 0.7, 0.9), min_plate=1.25):
    """
    Returns the weights to be used for each warmup set based on the specified
    working weight and percentages.

    :param workweight: working set weiht
    :type workweight: float
    :param set_factors: percentages of the working weight used for warm up sets
    :type set_factors: list, tuple
    :param min_plate: minimum plate weight
    :type min_plate: float
    :return: list of warm up set weights
    :rtype: list
    """
    if min_plate:
        min_plate *= 2

    warmups = [0] * len(set_factors)
    for i, f in enumerate(set_factors):
        set_weight = weight * f
        if min_plate:
            set_weight = ((weight * f) // min_plate ) * min_plate
        warmups[i] = set_weight
    return warmups
 

 if __name__ == "__main__":
    for weight in (52.5, 137.5, 90.0, 127.5, 40.0, 77.5):
        warmups = get_warmup_weights(weight, smallest_plate=1.25):
        print "{}: {!r}\n".format(weight, *warmups)
