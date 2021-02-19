# -*- coding: utf-8 -*-
"""
Functions to support output of a processed isotherm in the JSON format
adopted by the NIST ISODB (https://adsorption.nist.gov)
"""
import json
from decimal import Decimal
import requests
# pylint: disable-msg=invalid-name   #because I use snake_case


class CustomJSONEncoder(json.JSONEncoder):
    """Custom class to preserve decimal structure in output"""
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        # Any other serializer if needed
        return super().default(o)


# Wrapper function for JSON writes to ensure consistency in formatting
def json_writer(filename, data):
    """Format JSON according to ISODB specs"""
    with open(filename, mode='w') as output:
        json.dump(data,
                  output,
                  ensure_ascii=False,
                  sort_keys=True,
                  indent=4,
                  cls=CustomJSONEncoder)  # formatting rules
        output.write('\n')  # new line at EOF


def NIST_ISODB_isotherm(input_isotherm):
    """Convert a processed isotherm to the NIST ISODB JSON format"""
    output_isotherm = {}

    #Resolve the adsorbent
    adsorbent_name = input_isotherm['adsorbent']['name'].replace(' ', '%20')
    URL = 'https://adsorption.nist.gov/matdb/api/material/' + adsorbent_name + '.json'
    adsorbent_JSON = requests.get(URL).json()
    #pprint.pprint(adsorbent_JSON)

    #Resolve the adsorbate
    adsorbate_name = input_isotherm['adsorbate']['name'].replace(' ', '%20')
    URL = 'https://adsorption.nist.gov/isodb/api/gas/' + adsorbate_name + '.json'
    adsorbate_JSON = requests.get(URL).json()
    #pprint.pprint(adsorbate_JSON)

    output_isotherm['temperature'] = Decimal(input_isotherm['temperature'])
    output_isotherm['pressureUnits'] = input_isotherm['pressureUnits']
    output_isotherm['adsorptionUnits'] = input_isotherm['adsorptionUnits']
    output_isotherm['adsorbent'] = adsorbent_JSON
    output_isotherm['adsorbates'] = [adsorbate_JSON]

    isotherm_block = []
    for measurement in input_isotherm['isotherm_data']:
        block = {
            'pressure':
            Decimal(measurement['pressure']),
            'species_data': [{
                'InChIKey': adsorbate_JSON['InChIKey'],
                'composition': 1.0,
                'adsorption': Decimal(measurement['adsorption'])
            }],
            'total_adsorption':
            Decimal(measurement['adsorption'])
        }
        isotherm_block.append(block)

    output_isotherm['isotherm_data'] = isotherm_block
    #output_isotherm[''] = input_isotherm['']

    output_isotherm['category'] = 'exp'
    output_isotherm['compositionType'] = 'molefraction'
    output_isotherm['digitizer'] = 'Daniel W. Siderius'
    output_isotherm['isotherm_type'] = 'excess'
    output_isotherm['articleSource'] = ''
    output_isotherm['tabular'] = 1
    output_isotherm['DOI'] = ''
    output_isotherm['filename'] = ''
    output_isotherm['concentrationUnits'] = ''
    output_isotherm['date'] = '2021-02-19'

    #pprint.pprint(output_isotherm)
    #json_writer('isodb_output.json', output_isotherm)
    return output_isotherm
