"""
Name:  Baby Names Data Utility Functions
Author:  Brandon M. Burroughs
Description:  Various utilities to manipulate the baby names data file in a 
    structured way.
"""

import os
import pandas as pd

# Define locations of data
data_dir = './data/'
baby_names_data_file = 'baby_names.csv'

# Load baby names data file
baby_names_df = pd.read_csv(os.path.join(data_dir, baby_names_data_file))

def load_baby_names_data():
    """
    Loads the baby names data

    Parameters
    ----------
    N/A

    Returns
    -------
    The baby names dataset
    """
    return pd.read_csv(os.path.join(data_dir, baby_names_data_file))

# Utilities
def segment_data(segment_dict, sort_by_column='year', baby_names_data_frame=baby_names_df):
    """ 
    Return the data with the desired baby name sorted by year

    Parameters
    ----------
    segment_dict : dict
        Key-value pairs for attribute values to segment on

    baby_name_data_frame : Pandas DataFrame
        The dataframe containing the baby names data

    Returns
    -------
    baby_names_segment : Pandas DataFrame
        The segmented dataframe
    
    """
    # Create empty dataframe
    baby_name_segment = baby_names_data_frame

    # Iterate through dictionary and do segmentation
    for key, value in segment_dict.iteritems():

        try: 
            # Check for strings
            if isinstance(value, str):
                baby_name_segment = baby_name_segment[baby_name_segment['%s' % key]=='%s' % value]
            
            # Check for integers
            elif isinstance(value, int):
                baby_name_segment = baby_name_segment[baby_name_segment['%s' % key]==int('%s' % value)]
            
            # Otherwise print out message about skipping
            else:
                print "Values of type %s are not accepted.  Please use values of type str or int." % type(value)
        except:
            print "The key %s is not recognized.  Please use keys %s." % (key, baby_names_data_frame.columns.values)

    # Sort
    baby_name_segment.sort_values(by=sort_by_column, inplace=True)

    return baby_name_segment