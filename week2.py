#!/usr/bin/env python3

#### Starting with data ####

#### Before class ####

# share URL to hack.md with link to zipped dataset file to download

#### Objectives ####

# review previous week's objectives
# Today:
#   using packages
#   tidy data and importing data to python
#   selecting data using labels (columns) and rows
#   slicing subsets of rows and columns
#   calculating summary statistics

#### Using packages ####

# make sure everyone is working in project directory
# create new notebook for this week's material (name week2)

# introduction to packages
#   collection of functions
#   community contributed (anyone can write a package!)
# describe pandas
#   python data analysis library

# make packages available to use in this notebook
import os
import urllib.request
import pandas as pd # pd is alias, or shortcut, to specify we're using a function from it

#### Importing data ####

# create data directory
os.mkdir("data")

# download dataset (url on HackMD page)
urllib.request.urlretrieve("https://raw.githubusercontent.com/fredhutchio/R_intro/master/extra/clinical.csv", "data/clinical.csv")
# can preview data file by opening in web browser, or opening CSV file in spreadsheet program
# overview of tidy data principles
#   columns: variables (demographic and health information)
#   rows: observations (patients)
#   one piece of info per cell
# csv: comma separated values (other things besides commas can have separators too though)
# data from The Cancer Genome Atlas (from NIH), several cancer types in one file

# backup option for downloading data, if above code doesn't work:
#   show where to download data
#   emphasize unzipping directory and moving data to appropriate location

# import data as csv
pd.read_csv("data/clinical.csv")
# this only prints it to the screen!

# assign data to object
clinical_df = pd.read_csv("data/clinical.csv")

# preview data import
clinical_df.head() # print top few rows, 10 by default
clinical_df.head(8) # print top n rows
clinical_df.tail(20) # print last n rows
clinical_df.info() # print a summary of all columns, entries, data types and non-null values

## Challenge: What do you need to do to download and import the following files correctly:
# example1: https://raw.githubusercontent.com/fredhutchio/R_intro/master/extra/clinical.tsv
pd.read_csv("../data/clinical.tsv", sep="\t")
# example2: https://raw.githubusercontent.com/fredhutchio/R_intro/master/extra/clinical.txt
pd.read_csv("../data/clinical.txt", sep=" ")

# examine data import
type(clinical_df) # look at data type
clinical_df.columns # view column names
clinical_df.dtypes # look at type of data in each column

# can enter following as markdown cell (* render as bullet points)
## Data types: pandas vs native python
# * object = string
# * int64 = integer (64 bit)
# * float64 = float
# * datetime64 = N/A

#### Selecting data using labels (columns) and row ranges ####

# select a "subset" of the data using the column name
clinical_df["tumor_stage"]
# show only the first few rows of output
clinical_df["tumor_stage"].head()
# show data type for this row
clinical_df["tumor_stage"].dtype # single column, O stands for "object"

# use the column name as an "attribute"; gives the same output
clinical_df.tumor_stage
# head still works here!
clinical_df.tumor_stage.head()

# What happens if you ask for a column that doesn't exist?
#clinical_df["tumorstage"]

# Select two columns at once
clinical_df[["tumor_stage", "vital_status"]]
# can't use .column_name because there are multiple columns!
# double brackets are part of normal python syntax;
# they reference parts of lists, which can represent more complex data structures

## Challenge: does the order of the columns you list matter?

# Select rows 0, 1, 2 (row 3 is not selected)
clinical_df[0:3]

# Select row 2 to the end
clinical_df[1:]

# Select the last element in the list
clinical_df[-1:] # what does this mean in the context of indexing?

## BREAK

## Challenge: how would you extract the last 10 rows of the dataset?

#### Slicing subsets of rows and columns ####

# iloc is integer indexing [row slicing, column slicing]
# locate specific data element
clinical_df.iloc[2, 6]

# select range of data
clinical_df.iloc[0:3, 1:4]
# stop/end bound is NOT inclusive (e.g., up to but not including 3)
# can use empty stop boundary to indicate end of data
clinical_df.iloc[0:, 1:4]

# loc is for label indexing (integers interpreted as labels)
# start and stop bound are inclusive
clinical_df.loc[1:4]
# can use empty stop boundary to indicate end of data
clinical_df.loc[1: ]

# Select all columns for rows of index values specified
clinical_df.loc[[0, 10, 6831], ]

# select first row for specified columns
clinical_df.loc[0, ["primary_diagnosis", "tumor_stage", "age_at_diagnosis"]]

## Challenge: why doesn't the following code work?
#clinical_df.loc[2, 6]

## Challenge: how would you extract the last 100 rows for only vital status and days to death?
clinical_df.loc[6732:, ["vital_status", "days_to_death"]]
clinical_df.iloc[-100:, [3,5]]

clinical_df.info()
# Say you have a dataframe with a lot of columns and you want to grab alot of them
# for your analysis but not all. You can use numpy's R_ to make it easer

import numpy as np # imports numpy and aliases it as "np"
# Now say you want to get all the rows and columns but 'bcr_patient_barcode'

# clinical_df.iloc[0:, 0:18, 19:20] # this WONT work
clinical_df.iloc[0:, np.r_[0:18, 19:20] ] # but this does

# We are using numpy's R- which translates slice objects to concatenate along the first axis
np.r_[0:18, 19:20] # this takes the slices objects and makes an array

# You can then pass that array to iloc like so:
clinical_df.iloc[0:, np.r_[0:18, 19:20] ].head()
# This is just an easy way to quickly wrangle large dataframes by columns if need be

# You can also employ this when reading in files as dataframes using the `usecols` parameter like so
pd.read_csv("data/clinical.txt", sep=" ", usecols=np.r_[0:18, 19:20])

#### Calculating summary statistics ####

# calculate basic stats for all records in single column
clinical_df.age_at_diagnosis.describe()

# each metric one at a time (only prints last if all executed in one cell!)
clinical_df.age_at_diagnosis.min()

# convert columns
clinical_df.age_at_diagnosis/365
# convert min to days
clinical_df.age_at_diagnosis.min()/365

## Challenge: What type of summary stats do you get for object data?
clinical_df.site_of_resection_or_biopsy.describe()

## Challenge: How would you extract only the standard deviation for days to death?
clinical_df.days_to_death.std()

#### Copying vs referencing objects ####

# Using the "=" operator references the previous object
ref_clinical_df = clinical_df

# Using the "copy() method": actually creates another object
true_copy_clinical_df = clinical_df.copy()

# Assign the value `0` to the first three rows of data in the DataFrame
ref_clinical_df[0:3] = 0
# note: you probably wouldn't want to actually *do* this to your data!

## Challenge: How and why are the following three objects different?
# Hint: try applying head()
clinical_df.head() # has been modified because ref_clinical_df referenced it
ref_clinical_df.head() # was actually altered
true_copy_clinical_df.head() # actual copy of original, unaltered
# reinforce that the order of operations matters!

#### Wrapping up ####

# review objectives
# preview next week's objectives
# demo of spyder IDE, if time allows
