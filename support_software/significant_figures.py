# -*- coding: utf-8 -*-
"""
Function to preserve significant figures during mathematical conversions,
including an anti-logarithm
"""


def significant_figures(str_orig, conversion_type, conversion_factor=1.):
    """
        Function to convert an input number (as a string) via
        relevant conversions, then return a string that preserves the
        number of significant figures according to the appropriate
        significant-figure rules based on the input number and any
        transformations.

        Note: for base-10 logarithms, the rule is:
           Logarithm with N significant figures to the right of the
           decimal yields an antilog with N significant figures.

        The purpose of this function is to prevent a converted number
        from carrying more significant figures than the source. Conversion
        factors are assumed to carry infinite number of significant figures.

        str_orig: the input number, as a string
        conversion_type: (multiply, log10) - defines the mathematical manipulation
        conversion_factor: multiplication factor applied after manipulation (default = 1.0)

        Note: conversion_factor is assumed to have infinite significant figures
    """

    if conversion_type == 'multiply':
        float_out = float(str_orig) * conversion_factor
        str_mod = str_orig.strip().replace('.', '').replace('-',
                                                            '').lstrip('0')
        sig_digits = len(str_mod)
        str_out = '{num:.{decimals}e}'.format(num=float_out,
                                              decimals=sig_digits - 1)
    elif conversion_type == 'log10':
        float_out = (10.**(float(str_orig))) * conversion_factor
        str_mod = str_orig.replace('-', '')
        if str_mod[0] == '0':
            str_mod = str_mod.split('.')[1].lstrip('0')
        else:
            str_mod = str_mod.split('.')[1]
        sig_digits = len(str_mod)
        str_out = '{num:.{decimals}e}'.format(num=float_out,
                                              decimals=sig_digits - 1)
    else:
        raise ValueError('Unknown conversion_type: ', conversion_type)
    return str_out
