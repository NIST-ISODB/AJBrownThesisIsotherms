# -*- coding: utf-8 -*-
"""Functions for reading the flat CSV isotherm files"""
import pandas as pd
# pylint: disable-msg=invalid-name   #because I use snake_case
# pylint: disable-msg=no-else-return


def check_column(dataframe, column):
    """Check if column is single-valued"""
    data = dataframe[column]
    if len(set(data)) > 1:
        print(data)
        raise Exception('ERROR: column should be single-valued: ' + column)


def read_isotherm_flat_CSV(filename, run_id, segment_id=None):
    """Read the flat CSV file, then extract a specific run_id
       Isotherm is returned as a dictionary"""
    isotherm = {}
    # Read the entire CSV file [all as strings to preserve significant figures]
    df = pd.read_csv(filename, keep_default_na=False, dtype=str)

    # Boolean for segmenting
    segmented = isinstance(segment_id, int)

    # Selectively convert columns to integers
    df['run_id'] = df['run_id'].astype(int)
    if 'segment_id' in df:
        df['segment_id'] = df['segment_id'].astype(int)

    # Filter isotherm data to desired run and, if applicable, segment
    iso_data = df.loc[df['run_id'] == run_id]
    if len(iso_data) == 0:
        raise Exception('ERROR: Unable to find `run_id`=' + str(run_id) +
                        ' in ' + filename)
    if 'segment_id' in iso_data:
        if segmented:
            iso_data = iso_data.loc[iso_data['segment_id'] == segment_id]
            if len(iso_data) == 0:
                raise Exception('ERROR: Unable to find `segment_id`=' +
                                str(segment_id) + ' in `run_id`=' +
                                str(run_id) + ' for ' + filename)
        else:
            raise Exception(
                'ERROR: Isotherm data is segmented, but `segment_id` is not specified'
            )

    # Error check the metadata columns to ensure they are single-valued
    columns_to_check = [
        'adsorbent', 'adsorbent_mass', 'adsorbent_mass_units', 'adsorbate',
        'adsorbent_mass', 'adsorbent_mass_units', 'temperature',
        'temperature_units', 'pressure_units', 'adsorption_units',
        'run_description'
    ]
    if segmented:
        columns_to_check.append('segment_description')
    for column_name in columns_to_check:
        check_column(iso_data, column_name)

    # Convert the data rows to a dictionary
    isotherm['run_id'] = iso_data['run_id'].values[0]
    isotherm['run_description'] = iso_data['run_description'].values[0]
    if segmented:
        isotherm['segment_id'] = iso_data['segment_id'].values[0]
        isotherm['segment_description'] = iso_data[
            'segment_description'].values[0]
    isotherm['adsorbent'] = {}
    isotherm['adsorbent']['name'] = iso_data['adsorbent'].values[0]
    isotherm['adsorbent']['mass'] = iso_data['adsorbent_mass'].values[0]
    isotherm['adsorbent']['mass_units'] = iso_data[
        'adsorbent_mass_units'].values[0]
    isotherm['adsorbate'] = {}
    isotherm['adsorbate']['name'] = iso_data['adsorbate'].values[0]
    isotherm['adsorbate']['mass'] = iso_data['adsorbate_mass'].values[0]
    isotherm['adsorbate']['mass_units'] = iso_data[
        'adsorbate_mass_units'].values[0]
    isotherm['temperature'] = iso_data['temperature'].values[0]
    isotherm['pressureUnits'] = iso_data['pressure_units'].values[0]
    isotherm['adsorptionUnits'] = iso_data['adsorption_units'].values[0]
    isotherm['isotherm_data'] = [{
        'pressure': iso_data.pressure.values[i],
        'adsorption': iso_data.adsorption.values[i],
        'uncertainty': iso_data.uncertainty.values[i],
        'branch': iso_data.branch.values[i],
        'notes': iso_data.notes.values[i]
    } for i in range(len(iso_data))]

    return isotherm
