# -*- coding: utf-8 -*-
"""Module for conversion of pressure units"""


def torr_conversion(units):
    """Function to provide conversion from torr/mmHg to other pressure units"""
    if units in ['mmHg', 'torr']:
        conversion_factor = 1.
    elif units == 'bar':
        conversion_factor = 1.013250 / 760.
    elif units == 'atm':
        conversion_factor = 1. / 760.
    elif units == 'Pa':
        conversion_factor = 101325. / 760.
    elif units == 'kPa':
        conversion_factor = 101.3250 / 760.
    else:
        raise ValueError('Unknown pressure units for output:', units)
    return conversion_factor
