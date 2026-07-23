"""
Solar system data used by all the tasks.

I had these numbers copied into every task file and they slowly drifted
apart, so now they live here and everything imports from this one place.

Distances are in AU, periods in years, inclination in degrees.
"""

PLANETS = {
    'mercury': {'au': 0.387, 'period': 0.24,   'ecc': 0.2056, 'inc': 7.0,  'color': 'grey'},
    'venus':   {'au': 0.723, 'period': 0.62,   'ecc': 0.0068, 'inc': 3.4,  'color': 'yellow'},
    'earth':   {'au': 1.000, 'period': 1.00,   'ecc': 0.0167, 'inc': 0.0,  'color': 'blue'},
    'mars':    {'au': 1.523, 'period': 1.88,   'ecc': 0.0934, 'inc': 1.85, 'color': 'red'},
    'jupiter': {'au': 5.20,  'period': 11.86,  'ecc': 0.0489, 'inc': 1.30, 'color': 'orange'},
    'saturn':  {'au': 9.58,  'period': 29.46,  'ecc': 0.0565, 'inc': 2.49, 'color': 'yellow'},
    'uranus':  {'au': 19.29, 'period': 84.01,  'ecc': 0.0457, 'inc': 0.77, 'color': 'cyan'},
    'neptune': {'au': 30.25, 'period': 164.79, 'ecc': 0.0113, 'inc': 1.77, 'color': 'blue'},
    'pluto':   {'au': 39.51, 'period': 248.09, 'ecc': 0.2488, 'inc': 17.2, 'color': 'brown'},
}

# Grouped the way the app lets you choose them
INNER = ['mercury', 'venus', 'earth', 'mars']
OUTER = ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

SUN_COLOR = 'orange'
