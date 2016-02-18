"""
Name:  Combine Baby Names Data
Author:  Brandon M. Burroughs
Description:  Combine the various baby name data files into a more easily
    searchable dataset.
"""

import os
import pandas as pd

# Define relative data directory from repo root
data_dir = './data'
baby_names_dir = './data/names'

# Get list of data files
files = [f for f in os.listdir(baby_names_dir) if ".txt" in f]

# Create an empty dataframe
baby_names_df = pd.DataFrame(data=[], columns=['year','name','gender', 'count'])

# Loop through data files
for data_file in files:
    # Read in data file
    df = pd.read_table(os.path.join(baby_names_dir, data_file), sep=',', names=['name','gender','count'])

    # Find number of rows
    n_rows = df.shape[0]

    # Extract year from file name
    year = int(data_file.split('.txt')[0][-4:])

    # Add year column
    df['year'] = [year] * n_rows

    # Concatentate the two dataframes
    baby_names_df = pd.concat([baby_names_df, df])

# Write this new file to disk for convienient use later.
baby_names_df.to_csv(os.path.join('./data/', 'baby_names.csv'), index=False)