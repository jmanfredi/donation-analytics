# Analytics Pipeline for FEC Donation Data

## Table of Contents
1. [Introduction](README.md#introduction)
2. [Dependencies](README.md#dependencies)
3. [Description](README.md#description)
4. [Run Instructions](README.md#run-instructions)

## Introduction
For political campaigns, identifying donors who are likely to donate money multiple times can be extremely useful for maximizing the impact of a limited marketing budget. The project herein takes as input Federal Election Commission individual contribution data and searches for repeat donors. Running tallies of repeat contributions (as well as the nearest-rank percentile for a percent value provided by the user) for a given zip code, contribution year, and recipient are tracked and written to a file. Since the analysis of the data is done line-by-line, this approach could easily be applied to a streaming input rather than a data file.

## Dependencies
This project runs with Python3, which can be downloaded [here](https://www.python.org/download/releases/3.0/), and uses the NumPy scientific computing package, which can be found [here](http://www.numpy.org).

## Approach
Each individual contribution is analyzed as an independent record. For each properly formatted record, a unique donor identification key is created and checked against an existing dictionary of donor keys. If the key does not exist in the dictionary, this is the key for a first-time donor and it is added to the dictionary along with the year corresponding to the contribution. If the key does exist in the dictionary, create a repeat-donor identification key with the recipient ID, the contribution year, and the zip code. Note that this repeat-donor key is NOT unique to an individual donor, but rather corresponds to all donors within a given zip code giving to the same campaign in the same year. Using this key, the transaction amount is then added to a list of similar transactions stored in a dictionary. Then, several calculations are made (total number of transactions, total transaction amount, and the nearest-rank percentile) and written to the output file.

## Limitations

* Only individual contributions are considered.
* Each donor name and zipcode combination is considered unique.
* When a donor is encountered for the first time, this first contribution is considered to be the earliest one. However, the data is not necessarily in chronological order. In the case that a donor is added to the donor dictionary, and a subsequent record is read in with a transaction year earlier than that of the first contribution, this record is ignored.

## Run Instructions
After installing Python3 and Numpy, edit the provided input/percentile.txt file with the desired percent value. Then, execute the run.sh script with the following three arguments:
* The input file path for the percentile input
* The input file path for the FEC data
* The output file path