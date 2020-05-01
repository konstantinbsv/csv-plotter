import csv
import os.path
import sys

# input/output definitions
RAW_DATA_FILE = 'data.txt'
CSV_DATA_FILE = 'csv_data.csv'
FIELDNAMES = ['0000', '0001', '0010', '0011', '0100', '0101',
              '0110', '0111', '1000', '1001', '1010', '1011', '1100']

# check if data.txt exists
if not os.path.exists(RAW_DATA_FILE):
    print('No data.txt file in current directory.')
    sys.exit()

with open(RAW_DATA_FILE, 'r') as raw_data:
    clean = [line.strip().replace('(', '') for line in raw_data]    # remove extraneous characters
    lines = [line.split(')') for line in clean if line]             # split at ')' and remove empty lines

    data_dict = [{line[0]:line[1]} for line in lines]               # convert to dictionary

    # calculate number of capacitive sensors
    num_sensors = 1
    while lines[0][0] != lines[num_sensors][0]:
        num_sensors = num_sensors + 1

    num_rows = int(len(data_dict) / num_sensors)    # calculate number of rows in CSV
    combined_dict = [{}] * num_rows                 # create list of dictionaries (one dict for each row)

    # combine dictionaries in list for each row
    for row in range(num_rows):
        for i in range(num_sensors):
            combined_dict[row] = {**combined_dict[row], **data_dict[row * num_sensors + i]}

    # create CSV (overwrite if it already exists)
    with open(CSV_DATA_FILE, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
        csv_writer.writeheader()
        csv_writer.writerows(combined_dict)

