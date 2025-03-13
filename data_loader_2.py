# Import necessary libraries
import pandas as pd
from binance.client import Client

# Set API key and secret
api_key = 'LJSNL9rSJQjC587zl5sYCYwFFFC9mrEajXVzaQJM5zTm2YAupRXJYdvjRSOURK8W'
api_secret = 'cMSGbFRAcwZWCLnW8q3lFJEvRIztslfwhltr5Q5FqbbVxpASjIKpNthFamrKXjlj'

# Set the client
client = Client(api_key, api_secret)

# Get a list of all available symbols
symbols = client.get_all_tickers()

# Set the timeframe
start_date = '2017-01-01'
end_date = '2023-03-04'

# Initialize the dataframe
df = pd.DataFrame()


# Get the data
klines = client.get_historical_klines('XRPUSDT', Client.KLINE_INTERVAL_1DAY, start_date, end_date)
# Convert the data to a dataframe
df_temp = pd.DataFrame(klines, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'])
# Add the symbol column
df_temp['Symbol'] = 'XRPUSDT'
# Merge the dataframes
df = pd.concat([df, df_temp], ignore_index=True)
df = df[['Open_time', 'Symbol', 'Open', 'High', 'Low', 'Close']]
df1 = df.iloc[:1000,:]
df2 = df.iloc[1000:,:]
# Save the dataframe
df1.to_csv('cryptocurrency_data.csv', index=False)
df2.to_csv('new_cryptocurrency_data.csv', index=False)
