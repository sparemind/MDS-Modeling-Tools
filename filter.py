import sys
import csv
import statistics

# v1.2.1
# This program parses a .csv file and does the following:
# - Filter out only certain columns
# - Filter out only certain rows with entries for these columns
# - Standardizes each column's data (subtracts the mean and divides by the standard deviation)
# - Outputs the results to another .csv file
#
# Usage:
# Takes 1 argument: The .csv file to filter
# Attributes to filter are read in via STDIN, one per line
#
# Should be run with Python 3.4+
# 
# Changelog v1.2.1
# - EXCLUDE_NULLS option now ignore privacy suppressed entries
# Changelog v1.2
# - Attributes to filter are now read in via STDIN
# - Input .csv file now given as a command line argument
# Changelog v1.1
# - Now outputs both a standardized and non-standardized data file

if(len(sys.argv) < 2):
    print('Must specify input .csv to filter')
    sys.exit(1)
# The data file to read from
INFILE = sys.argv[1]

# These columns will be filtered out. It is assumed that the first attribute is
# the column with the item's name, and that all others specify numerical data.
ATTRIBUTES = []
for line in sys.stdin:
    line = line.lstrip()
    if(line.startswith('#')):
        continue
    ATTRIBUTES.append(line.split(None, 1)[0])

# If true, skips any row with missing data in an ATTRIBUTES column
EXCLUDE_NULLS = True
# The file to write the results to
OUTFILE = 'filtered.csv'

with open(INFILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Initialize column lists
    columns = []
    for i in range(len(ATTRIBUTES)):
        columns.append([])

    # Read in data and put into column lists
    for row in reader:
        skip_row = False
        row_data = []
        # Add column data to row_data
        for i in range(len(ATTRIBUTES)):
            # If a desired entry is NULL, invalidate the row (if EXCLUDE_NULLS is true)
            if(EXCLUDE_NULLS and (row[ATTRIBUTES[i]] == 'NULL' or row[ATTRIBUTES[i]] == 'PrivacySuppressed')):
                skip_row = True
                break
            row_data.append(row[ATTRIBUTES[i]])
        if(row['SATVRMID'] == 'NULL' or row['UG25ABV'] == 'NULL' or row['SATMTMID'] == 'NULL' or row['C150_4'] == 'NULL' or row['ADM_RATE'] == 'NULL' or row['SATWRMID'] == 'NULL' or row['COSTT4_A'] == 'NULL'):
            skip_row = True
        # Add the row data to the column lists
        if(not skip_row):
            for i in range(len(row_data)):
                columns[i].append(row_data[i] if(i == 0) else float(row_data[i]))
    count = len(columns[0])

    # Write unstandardized data to output file
    out_file = open('nonstd_' + OUTFILE, 'w')
    out_file.write(','.join(ATTRIBUTES) + '\n') 
    for i in range(count):
        row = []
        for col in columns:
            row.append(col[i])
        out_file.write(','.join(map(str, row)))
        out_file.write('\n')


    # Standardize data by column
    # All columns will now have a mean of 0 and standard deviation of 1
    for i in range(1, len(columns)):
        mean = statistics.mean(columns[i])
        stdev = statistics.stdev(columns[i])
        columns[i][:] = map(lambda x: (x - mean) / stdev, columns[i])
 
    # Write standardized data to output file
    out_file = open(OUTFILE, 'w')
    out_file.write(','.join(ATTRIBUTES) + '\n') 
    for i in range(count):
        row = []
        for col in columns:
            row.append(col[i])
        out_file.write(','.join(map(str, row)))
        out_file.write('\n')

    print(str(count) + " items filtered")





