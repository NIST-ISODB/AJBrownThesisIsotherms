# -*- coding: utf-8 -*-
"""Functions to aid extraction and plotting of scanning isotherms"""
import pandas as pd
import matplotlib.pyplot as plt
# pylint: disable-msg=invalid-name   #because I use snake_case


def extract_scan(source_df, runid, segmentid, branch='AD', bounds=None):
    """Extract a single scanning isotherm from the flat CSV isotherm file"""
    block = source_df.loc[source_df['run_id'] == runid]
    block = block.loc[block['segment_id'] == segmentid]
    if branch in ['A', 'D']:
        block = block.loc[block['branch'] == branch]
    if bounds is not None:
        block = block[bounds]
    x = list(block['pressure'].astype(float))
    y = list(block['adsorption'].astype(float))

    if segmentid > 0:
        #Add the last point of the previous segment
        point = source_df.loc[source_df['run_id'] == runid]
        point = point.loc[point['segment_id'] == (segmentid - 1)]
        x = [float(point['pressure'].iloc[-1])] + x
        y = [float(point['adsorption'].iloc[-1])] + y

    output_df = pd.DataFrame({'pressure': x, 'adsorption': y})

    return output_df


def plot_scan_group(source_df, scan_list):
    """Based on a list of dictionaries identifying scans, plot the group"""
    fig = plt.figure(figsize=(8, 8))  # pylint: disable-msg=unused-variable

    # Boundary Isotherm
    boundary = extract_scan(source_df, 1, 0, 'AD')
    plt.plot(boundary['pressure'],
             boundary['adsorption'],
             '.-',
             label='Boundary Isotherm')

    # Plot the specified scanning isotherms
    for segment in scan_list:
        # Identify the segment
        run_id = segment['run']
        segment_id = segment['segment']
        branch = segment['type']
        if 'bounds' in segment:
            bounds = segment['bounds']
        else:
            bounds = None
        # Extract the segment
        scan = extract_scan(source_df,
                            run_id,
                            segment_id,
                            branch=branch,
                            bounds=bounds)
        plt.plot(scan['pressure'],
                 scan['adsorption'],
                 '.-',
                 label=str(run_id) + '-' + str(segment_id))

    plt.legend()
    plt.show()
