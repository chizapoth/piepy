# classic time series modeling

import pandas as pd
import numpy as np

project_path = '/Users/chizhang/Documents/GitHub/piepy/'
path = 'data/Rainfall_data.csv'

# load data
df = pd.read_csv(project_path + path)
print(df)

# merge and produce time stamps
df['Timestamp'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
df.head(1)

len(df.columns) # now it's 7

df = df.set_index('Timestamp')
df = df.sort_values(by = 'Timestamp')
# drop the first three
df = df.drop(['Year', 'Month', 'Day'], axis = 1)

df.head()


# -------- 
# ARIMA

# note that this is a bit slow in the Rstudio IDE
# might be faster elsewhere
#import distutils

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.preprocessing import StandardScaler # standard scaler
from sklearn.metrics import mean_squared_error


# Split data into train and test sets
train_size = int(len(df) * 0.8)
print(train_size)
train, test = df[:train_size], df[train_size:]

# Scale the features
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)



features = ['Specific Humidity', 'Relative Humidity', 'Temperature']
target = 'Precipitation'

# ARIMA Model
order = (1, 1, 1)
arima_model = SARIMAX(train[target], order=order)
arima_result = arima_model.fit(disp=False)
arima_pred = arima_result.get_forecast(steps=len(test)).predicted_mean
arima_mse = mean_squared_error(test[target], arima_pred)

print(f'ARIMA MSE: {arima_mse}')


# es

# Exponential Smoothing Model
exp_smoothing_model = ExponentialSmoothing(train[target], trend='add', seasonal='add', seasonal_periods=12)
exp_smoothing_result = exp_smoothing_model.fit()
exp_smoothing_pred = exp_smoothing_result.forecast(steps=len(test))

exp_smoothing_mse = mean_squared_error(test[target], exp_smoothing_pred)
print(f'Exponential Smoothing MSE: {exp_smoothing_mse}')



# Function to visualize predictions vs actual values
import matplotlib.pyplot as plt

def plot_predictions(actual, pred, title):
    plt.figure(figsize=(12, 6))
    plt.plot(actual.index, actual, label='Actual', marker='o')
    plt.plot(pred.index, pred, label='Predicted', linestyle='dashed', marker='o')
    plt.title(title)
    plt.xlabel('Times')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

plot_predictions(test[target], arima_pred, 'ARIMA Model')




