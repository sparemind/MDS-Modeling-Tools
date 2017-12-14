import sys
import csv
import operator
from fuzzywuzzy import fuzz

# v1.0.1
# Reads in a file with items listed from top ranked to lowest ranked and
# generates RGBA values for each item based on its rank or lack of rank. Colors
# will be generated for all items found in a given data file. Fuzzy matching is
# used to connect names from the rankings file to the canonical names in the
# data file.
#
# Should be run with Python 3. Required packages:
# - fuzzywuzzy
# - (optional) python-Levenshtein
#
# Changelog v1.0.1
# - Added HIGHLIGHT functionality

# The rankings file to use
RANKINGS = 'ranks.txt'
#RANKINGS = 'r.txt'
# If True, all names in the rankings file will be given brightest color
# If False, names will be colored less bright the lower their ranking
HIGHLIGHT = False
# The data file to read from. The names are assumed to be in the first column
DATA = 'filtered.csv'
# The file to write the colors data to
OUTFILE = 'colors.csv'
# The top ranking item will have a color of MAX_COLOR, the bottom ranking item
# will have a color of MIN_COLOR. Items inbetween will have a linearly
# interpolated color. Items not in the rankings file will have color OTHER.
MAX_COLOR = (0, 0, 1, 1)
MIN_COLOR = (0, 0, 0.3, 1)
OTHER = (0, 0, 0, 1)

canon_names = []
with open(DATA) as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    next(reader) # Skip header

    for row in reader:
        canon_names.append(row[0])

raw_ranking_names = []
with open(RANKINGS) as rankfile:
    for row in rankfile:
        raw_ranking_names.append(row.strip())

canon_ranking_names = []
for rank_name in raw_ranking_names:
    best_match = ('N/A', -1)
    for data_name in canon_names:
        match_value = fuzz.partial_ratio(rank_name, data_name)
        if(match_value > best_match[1]):
            best_match = (data_name, match_value)

    # Name corrections
    if(rank_name == "University of Pennsylvania"):
        canon_ranking_names.append("University of Pennsylvania")
    elif(rank_name == "University of Virginia"):
        canon_ranking_names.append("University of Virginia-Main Campus")
    elif(rank_name == "Pennsylvania State University--University Park"):
        canon_ranking_names.append("Pennsylvania State University-Main Campus")
    elif(rank_name == "Ohio State University--Columbus"):
        canon_ranking_names.append("Ohio State University-Main Campus")
    elif(rank_name == "Purdue University--West Lafayette"):
        canon_ranking_names.append("Purdue University-Main Campus")
    elif(rank_name == "Southern Methodist University"):
        canon_ranking_names.append("Southern Methodist University")
    elif(rank_name == "Virginia Tech"):
        canon_ranking_names.append("Virginia Polytechnic Institute and State University")
    elif(rank_name == "University of Pittsburgh"):
        canon_ranking_names.append("University of Pittsburgh-Pittsburgh Campus")
    elif(rank_name == "Binghamton University--SUNY"):
        canon_ranking_names.append("SUNY at Binghamton")
    elif(rank_name == "Brown University"):
        canon_ranking_names.append("Brown University")
    else:
        canon_ranking_names.append(best_match[0])

#for i in range(len(canon_ranking_names)):
#    print(raw_ranking_names[i] + '\t\t' + canon_ranking_names[i])
#print(len(canon_ranking_names), len(raw_ranking_names))

diff = tuple(map(operator.sub, MAX_COLOR, MIN_COLOR))
STEP = tuple(x/len(canon_ranking_names) for x in diff)

out_file = open(OUTFILE, 'w')
for name in canon_names:
    try:
        rank = canon_ranking_names.index(name)
        if(HIGHLIGHT):
            color = MAX_COLOR
        else:
            step_amount = []
            for i in range(len(STEP)):
                step_amount.append(MAX_COLOR[i] - STEP[i] * rank)
            color = tuple(step_amount)
    except ValueError:
        color = OTHER
    out_file.write('%f, %f, %f, %f\n' % color)

