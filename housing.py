# -*- coding: utf-8 -*-
"""housing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NtiuvNIRR9TFleP33a0KzgeDci7KNJx9
"""

# Commented out IPython magic to ensure Python compatibility.
! pip install opendatasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import seaborn as sns
import opendatasets as od #import opendatasets library

od.download("https://www.kaggle.com/datasets/darshanprabhu09/california-housing-dataset")
#andylyy , ff520ec7edf98cff0f0d10e926de3567

from sklearn.linear_model import LinearRegression

df = pd.read_csv('/content/california-housing-dataset/housing.csv')

df.head()

"""# 1. EDA Process"""

df.isna().sum()

df['total_bedrooms'] = df['total_bedrooms'].fillna(0)

df.isna().sum()

df.describe()

"""# **2. Descriptive Statistic**"""

numeric_df = df[['median_income','median_income','median_house_value']].astype(int)
for column in numeric_df:
    mean = numeric_df[column].mean()
    std = numeric_df[column].std()
    maximum = numeric_df[column].max()
    minimum = numeric_df[column].min()
    
    print(f'Mean value of {column}: {mean}')
    print(f'Standard Deviation of {column}: {std}')
    print(f'Max value of {column}: {maximum}')
    print(f'Min value of {column}: {minimum}')
    print('\n')

correlation = df.corr()['median_house_value']

correlation #not very strong correlation with house value

df

"""# **3. Data Visualization**"""

plt.figure(figsize = (8,6))
heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True)
heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12); 
#strong relationship for total_rooms, total_bedrooms, population, households
#and relationship between median_income and median_house_value

import plotly.express as px
housing_age = df['housing_median_age'].value_counts() #we have 1273 houses are 52 years old
fig = px.bar(x = housing_age.index, y = housing_age.values)
fig.update_layout(
    xaxis_title='Housing Median Age',
    yaxis_title='Counts'
)

px.histogram(df, x='housing_median_age', histnorm = 'density', nbins = 6)

px.scatter(df, x='total_rooms', y='total_bedrooms')

px.scatter(df,x='median_income', y='median_house_value' ) #not clear correlation

fig = px.box (df, x = 'housing_median_age', y= 'median_house_value')
fig.show()

px.box(df, x = 'ocean_proximity', y = 'housing_median_age')

ocean = df['ocean_proximity'].value_counts().reset_index()
ocean.columns = ['ocean_proximity', 'count']

fig = px.pie(ocean, values='count', names='ocean_proximity')
fig.show()
#44% housing fall in <1h Ocean

# Create scatter mapbox plot
fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color = 'median_house_value',
                        hover_data = ['total_rooms', 'total_bedrooms', 'population', 'median_income'], 
                        mapbox_style='open-street-map',
                        zoom = 5)

fig.show()

"""# **3.Model:**"""

lm = LinearRegression()

X = df[['housing_median_age']]
y = df['median_house_value']

lm.fit(X,y)

lm.score(X,y)

#a intercept
lm.intercept_

#b slope
lm.coef_

"""$$
Yhat = a + b  X
$$

**House value** = 179119.92 + 968.45 * housing_median_age
"""

y = 179119.92 + 968.45*X