import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# This line lets us plot on our ipython notebook
%matplotlib inline

# Read in the data

df = pd.read_csv('week-03/data/skyhook_2017-07.csv', sep=',')

# Create a new date column formatted as datetimes.
df['date_new'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Determine which weekday a given date lands on, and adjust it to account for the fact that '0' in our hours field corresponds to Sunday, but .weekday() returns 0 for Monday.
df['weekday'] = df['date_new'].apply(lambda x: x.weekday() + 1)
df['weekday'].replace(7, 0, inplace = True)

# Remove hour variables outside of the 24-hour window corresponding to the day of the week a given date lands on.
for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    ( (df['hour'] < j) & (df['hour'] > i + 18) ) |
    ( (df['hour'] > i + 18 ) & (df['hour'] < j) )
    )
    ].index, inplace = True)
  else:
    df.drop(df[
    (df['weekday'] == (i/24)) &
    (
    (df['hour'] < j) | (df['hour'] > i + 18 )
    )
    ].index, inplace = True)

##PROBLEM 1
groupby_date = df.groupby('date')['count']
groupby_date_agg = groupby_date.sum()
groupby_date_agg.plot.bar(color='b', title='Total GPS Pings by Date')



## PROBLEM 2
'''
replace all hours from 0 to 23
replace method

.replace(value 1, value 2, inplace)
use similar code structure to the one above

for i in range(0, 168, 24): --> looking at every 24 hours from the 0-168 block
but cos in GMT, have to put in adjustment factor but can't just put i-5 if not get negative values

j = range(0,168,1)[i-5] -- adjust the first hour of each day - set up the boundaries for each week

now to call out the instance when j > i -- need to replace values at the end and beginning of the list cos Day 0 is split over the edge
if (j>i):
    df['hour'].replace(range(i,i+19,1), range(5,24,1), inplace = true) --> replaces the values at the beginning
    df['hour'].replace(range(i+163,i+168,1), range(5,24,1), inplace = true) --> try this out
else:
    df['hour'].replace(range(j,i+19,1), range(0,24,1), inplace = true)

'''

for i in range(0, 168, 24):
  j = range(0,168,1)[i - 5]
  if (j > i):
    df['hour'].replace(range(i,i+19,1), range(5,24,1), inplace = True)
    df['hour'].replace(range(i+163,i+168,1),range(0,5,1), inplace = True)
  else:
    df['hour'].replace(range(j,i+19,1), range(0,24,1), inplace = True)

df['hour'].unique()

print(df['hour'].unique())

df['new_hour'] = pd.to_timedelta(df['hour'], unit = 'H')

df['timestamp'] = df['date'].astype(str) + ' ' + df['new_hour'].astype(str)

groupby_timestamp = df.groupby('timestamp')['count']
lineplot = groupby_timestamp.sum()
lineplot.plot.line(color='b', title='Total GPS Pings by Timestamp')

groupby_hour = df.groupby('new_hour')['count']
barchart = groupby_hour.sum()
barchart.plot.bar(color='b', title="Total GPS Pings by Hour")


"""
PROBLEM 5
pick three time ranges
based on locations
size of dot correspond to GPS pings
set a mask
"""


timestamp_hour = pd.Timestamp(df['new_hour'])
first_hour = df[(df['timestamp_hour'] == "14:00:00")]

first_hour.plot.scatter(x = df['latitude'], y = df['longitude'], s=df['count']*200)

test = df[(df['new_hour'] == "14:00:00")]
test_sum = test.groupby(['lat', 'lon'])['count'].sum()
test_sum.plot.scatter(x=df['lat'] & df['lon'], y=test_sum, s=df['count']*200)
