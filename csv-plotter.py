#! python3
import csv
import os.path
import sys
import re
import matplotlib.pyplot as plt

# regex data format definition
RE_DATA = r'(\(\d{4}\))(\d.\d+)'
# input/output definitions
RAW_DATA_FILE = 'data.txt'
CSV_DATA_FILE = 'csv_data.csv'
FIELDNAMES = ['=\"(0000)\"', '=\"(0001)\"', '=\"(0010)\"', '=\"(0011)\"', '=\"(0100)\"', '=\"(0101)\"',
              '=\"(0110)\"', '=\"(0111)\"', '=\"(1000)\"', '=\"(1001)\"', '=\"(1010)\"', '=\"(1011)\"', '=\"(1100)\"']
# plot definitions
PLOT_SIZE = (10, 6)     # in hundreds of pixels
OFFSET = 0.025            # offset from max/min value to top/bottom of y-scale
Y_LABEL = 'picoFarads'
X_LABEL = 'sample #'

# check if data.txt exists
if not os.path.exists(RAW_DATA_FILE):
    print('No data.txt file in current directory.')
    sys.exit()

with open(RAW_DATA_FILE, 'r') as raw_data:
    print('Reading ' + RAW_DATA_FILE + '...')
    clean = [line.strip() for line in raw_data]                       # remove extraneous characters
    # lines = [line.split(')') for line in clean if line]             # split at ')' and remove empty lines

    lines = []
    for line in clean:
        re_groups = re.search(RE_DATA, line)
        if re_groups:
            designator = '=\"' + re_groups.group(1) + '\"'
            data = re_groups.group(2)
            lines.append([designator, data])

    data_dict = [{line[0]:line[1]} for line in lines]               # convert to dictionary

    # calculate number of capacitive sensors
    num_sensors = 1
    while lines[0][0] != lines[num_sensors][0]:
        num_sensors = num_sensors + 1

    num_rows = int(len(data_dict) / num_sensors)    # calculate number of rows in CSV
    list_of_dicts = [{}] * num_rows                 # create list of dictionaries (one dict for each row)

    # combine dictionaries in list for each row
    for row in range(num_rows):
        for i in range(num_sensors):
            list_of_dicts[row] = {**list_of_dicts[row], **data_dict[row * num_sensors + i]}

    # create CSV (overwrite if it already exists)
    with open(CSV_DATA_FILE, 'w', newline='') as csv_file:
        print('Creating CSV...')
        csv_writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
        csv_writer.writeheader()
        csv_writer.writerows(list_of_dicts)

# create plots
print('Creating plots', end='')
for idx, field in enumerate(FIELDNAMES, start=1):
    sens = [float(line.get(field, 0)) for line in list_of_dicts if line]
    title = field.strip('="')   # get plot title from fieldnames
    fig = plt.figure(figsize=PLOT_SIZE)
    # calculate y scale
    plt.ylim(ymin=min(sens) - OFFSET, ymax=max(sens) + OFFSET)
    plt.plot(sens)
    plt.title(title)
    plt.ylabel(Y_LABEL)
    plt.xlabel(X_LABEL)
    plt.savefig(title)          # saves as PNG by default
    sys.stdout.write('.')
    sys.stdout.flush()

print('\nDone!')
