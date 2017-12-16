# MDS Modeling Tools #

This project provides several tools for creating and analyzing multidimensional
scaling (MDS) models.

## Overview ##

This project was created to assist modeling similarities between U.S.
universities, and contains tools to assist with three primary tasks:
* **Parsing data**
* **Creating an MDS model**
* **Analysing the model**

Data is filtered from an input `.csv` file, producing another `.csv` file with
only the columns specified in an `attributes.txt` file and the rows that
contain data for those columns. All values in this output will also be
normalized to have a mean of 0 and standard deviation of 1.

A 2D MDS model is then created, with both a wordcloud and unlabeled scatter
plot being produced alongn with plots of goodness-of-fit vs. different model
dimensions and Minkowski p-values. A `colors.csv` file can optionally be given
to color points in the unlabeled plot. A `ranks.txt` can also be used to
generate this file automatically based on an ordered ranking. 1D and 3D models
can also be created by editing `MDS.R`.

The `points.csv` output of the model can then be analyzed to determine the
correlation direction and magnitue for each direction for each dimension.
n-dimensional inputs are supported. The reuslts are then printed and saved to a
file, with the attribute ordered from most correlated to least for each
dimension.

## Running ##
To parse, run, and analyse everything from scratch, run the default make
target:
```
make
```

To include coloring based on a `ranks.txt` file, run:
```
make color
```

Programs can also be run separately:
* `python3 filter.py [data.csv] < [attributes.txt]`
* `python3 color.py`
* `Rscript MDS.R <colors.csv>`
* `python3 analyze.py < [attributes.txt]`
