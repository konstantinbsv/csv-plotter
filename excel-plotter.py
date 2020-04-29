import os.path, sys
import csv, itertools
import re

# input/output definitions
RAW_DATA_FILE = 'data.txt'
CSV_DATA_FILE = 'csv_data.csv'
FIELDNAMES = ['Nº', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

# check if data.txt exists
if not os.path.exists(RAW_DATA_FILE):
    print('No data.txt file in current directory.')
    sys.exit()

with open(RAW_DATA_FILE, 'r') as raw_data:
    clean = [line.strip().replace('(', '') for line in raw_data]    # remove extraneous characters
    lines = [line.split(')') for line in clean if line]             # split at ')' and remove empty lines

    with open(CSV_DATA_FILE, 'w') as csv_file:
        # create csv (overwrite if it already exists)
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES ,delimiter='\t')
        csv_writer.writeheader()


