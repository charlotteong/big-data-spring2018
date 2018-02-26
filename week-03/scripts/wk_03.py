import pandas as pd
import numpy as np
import matplotlib
%matplotlib inline

newlist = []
df = pd.DataFrame()
print(df)

df['test'] = ['bilbo', 'frodo', 'samwise']
print(df)

df.assign(height = [0.5, 0.4, 0.6])

import os
os.chdir('week-03')
df = pd.read_csv('data/skyhook_2017-07.csv', sep = ',')

df.head()
df.shape
## refers to length and width - ie columns and rows
## to get number of rows: df.shape[0] to get no. of columns df.shape[1]

df.columns ## gives an index of column names
df['cat_name'].unique()

df['hour'] == 158 ## this makes a mask -- an array of true false values -- go through every row to see if hour column = 158
## to actually get the values only is to take the mask and return only the rows that return boolean value true

magic_hour = df[df['hour'] ==158]
magic_hour.shape

df[(df['hour'] == 158) & (df['count']>50)]
## to have two conditions
df[(df['hour'] == 158) & (df['count']>50)].shape

bastille = df[df['date'] == '2017-07-14']
## to get a particular date (ie subset of the dataframe)
bastille.head()

bastille['count'].mean()

fans = bastille[bastille['count'] > bastille['count'].mean()]
## to get greater than average cells.
## this creates a mask that returns rows with values greater than the mean value. the mean method will return a single value

fans.describe()
fans['count'].describe()
## generates summary statistics.

df.groupby('date')['count'].sum()
## looks for unique values of date and sums all values in count column for each unique date

df.groupby('date')['count'].describe()
df.groupby('date')['count'].sum()
df[df['count'] == df['count'].max()] ## only returns values that match with the max value

df['hour'].unique()
jul_sec = df[df['date'] == '2017-07-02']
jul_sec.groupby('hour')['count'].sum().plot()

df['date_new'] = pd.to_datetime(df['date'], format = "%Y-%m-%d")
## takes an input and converts to machine readable timestamp
df['date_new']

## to know what date any day of the week is
df['weekday'] = df['date_new'].apply(lambda x: x.weekday()+1)
df['weekday'].replace(7,0, inplace = True)
## weekday function is a monday to sunday function, for this case the hours data stored is sunday to saturday, therefore +1
## second line adjusts the new value of 7 for sunday to 0 for sunday



## NOT COMPLETED BELOW.
for i in range(0,168,24):
    j = range()
    df.drop(df[df['weekday'] == (i/24) &
    (
    (df['hour']) < i | df['hour'] > j + 18) ## cos hours stored in greenwich mean time
    )
    ])
