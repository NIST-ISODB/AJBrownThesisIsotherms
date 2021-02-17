# -*- coding: utf-8 -*-
"""
Function to process the 'raw' isotherm output from a flat CSV file
and return a structured dictionary with conversion of pressure
to bar units and normalization of the adsorption measurements
"""

from .parse_isotherm import read_isotherm_flat_CSV
from .significant_figures import significant_figures
from .psat_correlations import saturation_pressure

MMHG_TO_BAR = (1. / 760.) * 1.013250  #bar


def process_isotherm(filename, run_id, segment_id=None):
    """Function to process the raw isotherm"""
    isotherm = read_isotherm_flat_CSV(filename, run_id, segment_id)

    # Extract measurement information
    adsorbent_mass = isotherm['adsorbent']['mass']
    # adsorbent_mass_units = isotherm['adsorbent']['mass_units']
    adsorbate_mass = isotherm['adsorbate']['mass']
    # adsorbate_mass_units = isotherm['adsorbate']['mass_units']

    if isotherm['pressureUnits'] == 'relative':
        conversion = 'multiply'
        factor = saturation_pressure(isotherm['adsorbate']['name'],
                                     isotherm['temperature'],
                                     output_units='bar')  #relative -> bar
    elif isotherm['pressureUnits'] == 'mmHg':
        conversion = 'multiply'
        factor = MMHG_TO_BAR  #mmHg -> bar
    elif isotherm['pressureUnits'] == 'log10(mmHg)':
        conversion = 'log10'  #log_10(p)
        factor = MMHG_TO_BAR  #mmHg -> bar
    else:
        raise ValueError('Unknown pressure units: ', isotherm['pressureUnits'])

    processed_isotherm = {}
    processed_isotherm['run_id'] = isotherm['run_id']
    processed_isotherm['run_description'] = isotherm['run_description']
    processed_isotherm['adsorbent'] = {}
    processed_isotherm['adsorbent']['name'] = isotherm['adsorbent']['name']
    processed_isotherm['adsorbate'] = {}
    processed_isotherm['adsorbate']['name'] = isotherm['adsorbate']['name']
    processed_isotherm['temperature'] = isotherm['temperature']

    processed_isotherm_data = []
    for measurement in isotherm['isotherm_data']:
        mg_to_mmolpg = 1000. / float(adsorbent_mass) / float(
            adsorbate_mass)  #mmol/g
        processed_isotherm_data.append({
            # Issues: should not have to pass string to SF module
            #   -remember that SF returns a string
            #   -this should be documented
            'pressure':
            significant_figures(measurement['pressure'], conversion, factor),
            'adsorption':
            significant_figures(measurement['adsorption'], 'multiply',
                                mg_to_mmolpg),
            'branch':
            measurement['branch'],
            'notes':
            measurement['notes']
        })

    processed_isotherm['adsorptionUnits'] = 'mmol/g'
    processed_isotherm['pressureUnits'] = 'bar'
    processed_isotherm['isotherm_data'] = processed_isotherm_data

    return processed_isotherm
