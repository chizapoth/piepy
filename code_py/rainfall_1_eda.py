# import kagglehub

# Download latest version
# path = kagglehub.dataset_download("poojag718/rainfall-timeseries-data")

# print("Path to dataset files:", path)

import pandas as pd
import numpy as np

project_path = '/Users/chizhang/Documents/GitHub/piepy/'
path = 'data/Rainfall_data.csv'

# load data
df = pd.read_csv(project_path + path)
df

# get the columns and rows
len(df)
len(df.columns)

# or get both together (like dim() in r)
df.shape

# column names
df.columns.to_list()

# check data types for each column
df.dtypes
df.info()

# by row index 
df[0:1]
df[0:2]

df.iloc[0]
df.iloc[2:4]
df.iloc[:, 0]
df.iloc[:, 0:2]
df.iloc[:2, 0:2]
df.iloc[:, [0, 3]]

# this is more intuitive
df.loc[2:4] # entire row
df.loc[2:4, ['Year', 'Month']]


# list comprehension
colname = df.columns[[0, 2]]
colname
df[colname]

# to print out the first lines
df.head()
df.head(6)


# basic manipulation -----

df['Timestamp'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df.head(1)

len(df.columns) # now it's 7

df = df.set_index('Timestamp')
df = df.sort_values(by = 'Timestamp')
# drop the first three
df = df.drop(['Year', 'Month', 'Day'], axis = 1)

df.head()

# check na
df.isna()
df.isna().sum()




# visualization -------
import seaborn as sns # Visualization
import matplotlib.pyplot as plt



# if want to plot one by one, 
sns.lineplot(x="Timestamp", y="Temperature", data=df, color = 'cornflowerblue')
plt.title("Time Series of Temperature")
plt.xlabel("Date")
plt.ylabel("Values")
plt.xticks(rotation=45)

plt.show()





# subplots ------
f, ax = plt.subplots(nrows=4, ncols=1, figsize=(15, 25))

for i, column in enumerate(df.columns):
    sns.lineplot(x=df.index, y=df[column], 
    ax=ax[i], 
    color='dodgerblue')
    ax[i].set_ylabel(ylabel=column, fontsize=14)

# without plt.show() the figure does not show
plt.show()



