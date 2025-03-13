import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import csv
import time
import urllib
import zipfile

# Set start date and end date
start_date = '2018-01-01'
end_date = dt.datetime.now().strftime("%Y-%m-%d")

# Fetch the data from the cryptocurrency exchange
url = 'https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1d'
data = requests.get(url).json()

# Read the data and convert it into a dataframe
df = pd.DataFrame(data, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
# Plot the data
plt.plot(df['Close'])
plt.title('XRP/USDT Price Over 5 Years')
plt.xlabel('Time')
plt.ylabel('Price (USD)')

# Manipulate and analyse the data
df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
print(df['Date'])
df['Returns'] = np.log(pd.to_numeric(df['Close'])/pd.to_numeric(df['Close'].shift(1)))
print(len(df.index))
# Save the data in CSV format


df1 = df.iloc[:250,:]
df2 = df.iloc[250:,:]
print(df1)
print(df2)

df1.to_csv('cryptocurrency_data.csv', index=False)
df2.to_csv('new_cryptocurrency_data.csv', index=False)

# Compress the data into a zip file
with zipfile.ZipFile('cryptocurrency_data.zip', 'w') as zp:
    zp.write('cryptocurrency_data.csv')