import sys
import csv
import operator

# v1.3
# This program analyzes an N-dimensional MDS model using an associated .csv
# data file and prints out the axis correlations for each specified attribute.
#
# Usage:
# Attributes to analyze are read in via STDIN, one per line
#
# Should be run with Python 3
#
# Changelog v1.3
# - Attributes to analyze are now read in via STDIN
# Changelog v1.2
# - Added alternate output format for sorting in order of correlation magnitude
# - Changed previous output format to sort by correlation magnitude
# - Added header labels for output columns
# Changelog v1.1.1
# - Added output column for difference between positive and negative groups
# Changelog v1.1
# - Added ability to analyze adjustable upper and lower percentage ranges
# - Added adjustable factor to make output more readable

# These columns will be analyzed. The first column is assumed to be the
# item's name, and will be skipped. All others are assumed to specify
# numerical data. 
ATTRIBUTES = []
for line in sys.stdin:
    line = line.lstrip()
    if(line.startswith('#')):
        continue
    ATTRIBUTES.append(line.split(None, 1)[0])

# The data file to read from
DATA = 'filtered.csv'
#DATA = 'nonstd_filtered.csv'
# The MDS points file to read from. Should have no headers and be in the form:
# NAME, DIM_1, DIM_2, ..., DIM_N
POINTS = 'points.csv'
# Multiplication factor to make numbers more readable
FACTOR = 100
# Percent of items that each upper and lower bound will contain. Should be <= 0.5
PERCENT = 0.1
# How the results should be printed. Options:
# 0 = Print negative and positive results separately
# 1 = Print in descending order of correlation magnitude
OUTPUT_TYPE = 1

# Read in MDS points
points = {}
with open(POINTS) as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')

    for row in reader:
        coords = []
        for i in range(1, len(row)):
            coords.append(float(row[i]))
        points[row[0]] = tuple(coords)
        # Dimension of the MDS model
        dim = len(coords)

# Determine the upper and lower bounds that determine whether a point is
# "positive" or "negative"
sorted_points = []
lower_bounds = []
upper_bounds = []
for i in range(dim):
    sorted_points.append([])
    for name, point in points.items():
        sorted_points[i].append(point[i])
    sorted_points[i].sort()
    lower_bound_index = int(len(sorted_points[i]) * PERCENT)
    upper_bound_index = len(sorted_points[i]) - lower_bound_index
    lower_bounds.append(sorted_points[i][lower_bound_index])
    upper_bounds.append(sorted_points[i][upper_bound_index])

print("Analyzing lower %d%% and upper %d%%..." % (100 * PERCENT, 100 * PERCENT))
with open(DATA, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Each index in these lists represents a dimension of the model.
    # At each index is stored a map which contains the running sum of the
    # attribute values of the points that are either below or above the center.
    negative_points = []
    positive_points = []
    # Holds the number of positive/negative points in each dimension
    num_negative_points = []
    num_positive_points = []
    for i in range(dim):
        dim_data_pos = {}
        dim_data_neg = {}
        for attr in ATTRIBUTES[1:]:
            dim_data_pos[attr] = 0
            dim_data_neg[attr] = 0
        positive_points.append(dim_data_pos)
        negative_points.append(dim_data_neg)
        num_positive_points.append(0)
        num_negative_points.append(0)

    # Read in data and put into column lists
    for row in reader:
        # Skip rows that don't have associated points or don't have data for
        # the desired attributes
        if(not row['INSTNM'] in points):
            continue
        skip_row = False
        for attr in ATTRIBUTES:
            if(row[attr] == 'NULL'):
                skip_row = True
                break
        if(skip_row):
            continue

        # Process data, depending on whether this point is positive or negative
        point_is_positive = [False] * dim
        point_is_negative = [False] * dim
        for attr in ATTRIBUTES[1:]:
            value = float(row[attr])

            for i in range(dim):
                if(points[row['INSTNM']][i] >= upper_bounds[i]):
                    positive_points[i][attr] += value
                    point_is_positive[i] = True
                elif(points[row['INSTNM']][i] <= lower_bounds[i]):
                    negative_points[i][attr] += value
                    point_is_negative[i] = True
        for i in range(dim):
            if(point_is_positive[i]):
                num_positive_points[i] += 1
            elif(point_is_negative[i]):
                num_negative_points[i] += 1

# Turn each sum into a mean
for attr in ATTRIBUTES[1:]:
    for i in range(dim):
        negative_points[i][attr] /= num_negative_points[i];
        positive_points[i][attr] /= num_positive_points[i];

# Prints the results of given attributes and the difference in their interval
# means along with the sign of the difference.
# @param results A list of tuples in the form (attribute, difference) where
#                "attribute" is the name of the attribute and "difference" is
#                the difference between the positive and negative interval means.
def print_interval_results(results):
    for result in results:
        attr_name = result[0].ljust(pad_len)
        neg_mean = negative_points[i][result[0]] * FACTOR
        pos_mean = positive_points[i][result[0]] * FACTOR
        diff = result[1] * FACTOR
        corr = 'POSITIVE' if(diff > 0) else 'NEGATIVE'
        print('\t%s\t%s\t%f\t%f\t%f' % (attr_name, corr, neg_mean, pos_mean, diff))

# Print results
pad_len = len(max(ATTRIBUTES, key=len))
for i in range(dim):
    print('Dimension ' + str(i + 1) + ' Correlations:')
    header = '\t%s\t%s\t%s\t%s\t%s' % ('Attribute'.ljust(pad_len), 'Direction', '- Interval Avg', '+ Interval Avg', 'Interval Diff')
    print(header)
    print('\t' + ('=' * len(header.expandtabs())))

    if(OUTPUT_TYPE == 0):
        positive_correlation = []
        negative_correlation = []
        for attr in ATTRIBUTES[1:]:
            diff = positive_points[i][attr] - negative_points[i][attr]
            if(diff > 0):
                positive_correlation.append((attr, diff))
            else:
                negative_correlation.append((attr, diff))
        sorted_positive_correlation = sorted(positive_correlation, key=lambda x: abs(x[1]), reverse=True)
        sorted_negative_correlation = sorted(negative_correlation, key=lambda x: abs(x[1]), reverse=True)
        print_interval_results(sorted_positive_correlation, True)
        print()
        print_interval_results(sorted_negative_correlation, False)
    else:
        results = {}
        for attr in ATTRIBUTES[1:]:
            diff = positive_points[i][attr] - negative_points[i][attr]
            results[attr] = diff
        sorted_results = sorted(results.items(), key=lambda x: abs(x[1]), reverse=True)
        for result in sorted_results:
            attr_name = result[0].ljust(pad_len)
            diff = result[1] * FACTOR
            corr = 'POSITIVE' if(diff > 0) else 'NEGATIVE'
            neg_mean = negative_points[i][result[0]] * FACTOR
            pos_mean = positive_points[i][result[0]] * FACTOR
            print('\t%s\t%s\t%f\t%f\t%f' % (attr_name, corr, neg_mean, pos_mean, diff))
   


