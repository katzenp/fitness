"""
conversions.py

Description:
    Tools and utilities for converting measurements from one system to another

https://en.wikipedia.org/wiki/Imperial_units#Length
Imperial Units
    length
        inch
        foot
        yard
    volume
        ounce
        pint
        quart
        gallon
    mass
        ounce
        pound
        stone
Metric Units
    length
        milimeter
        centimeter
        meter
    volume
        mililitres
        litre
    mass
        gram
        kilogram
"""


# ==============================================================================
# imperial --> imperial
# ==============================================================================
# length
inch_to_foot = lambda value: value / 12.0
inch_to_yard = lambda value: value / 36.0

foot_to_inch = lambda value: value * 12.0
foot_to_yard = lambda value: value / 3.0

yard_to_foot = lambda value: value * 3.0
yard_to_inch = lambda value: value * 36.00

# volume
ounce_to_pint = lambda value: value * 0.0625
ounce_to_quart = lambda value: value * 0.03125
ounce_to_gallon = lambda value: value * 0.0078125

pint_to_ounce = lambda value: value * 16.00
pint_to_quart = lambda value: value * 0.5
pint_to_gallon = lambda value: value * 0.125

quart_to_ounce = lambda value: value * 32.0
quart_to_pint = lambda value: value * 2.0
quart_to_gallon = lambda value: value * 0.25

gallon_to_ounce = lambda value: value * 128.0
gallon_to_pint = lambda value: value * 8.0
gallon_to_quart = lambda value: value * 4.0


# mass


# ==============================================================================
# imperial --> metric
# ==============================================================================
inch_to_centimeter = lambda value: value * 2.54
centimeter_to_inch = lambda value: value / 2.54


# ==============================================================================
# weight
# ==============================================================================
ounce_to_gram = lambda value: value * 28.0
gram_to_ounce = lambda value: value / 28.0
pound_to_kilogram = lambda value: value * 0.454
kilogram_to_pound = lambda value: value / 0.454


# ==============================================================================
# classes
# ==============================================================================
value = 64
source_type = "inch"
destination_type = "centimeter"
