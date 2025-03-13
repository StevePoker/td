from api_manager.binance_api.api import BinanceAPI
from api_manager.hepler.TimeFormatter import TimeConverter

import pandas as pd
import datetime

api = BinanceAPI()
year = 2020
month = 1
day = 1

counter = 0
pd_data = None

today_year = int(datetime.datetime.today().year)
today_month = int(datetime.datetime.today().month)
today_day = int(datetime.datetime.today().day)

while True:
    counter += 1

    starttime = datetime.datetime.strptime(str(datetime.datetime(year, month, day)), '%Y-%m-%d %H:%M:%S')
    endtime = datetime.datetime.strptime(
        str(datetime.datetime(year, month + 1, day)), '%Y-%m-%d %H:%M:%S'
    ) if day != 31 else datetime.datetime.strptime(
        str(datetime.datetime(year + 1, 2, 1)), '%Y-%m-%d %H:%M:%S'
    )

    if endtime.year == today_year and endtime.month > today_month:
        starttime = datetime.datetime.strptime(str(datetime.datetime(year, month, day)), '%Y-%m-%d %H:%M:%S')
        endtime = datetime.datetime.strptime(
            str(datetime.datetime(today_year, today_month, today_day)), '%Y-%m-%d %H:%M:%S'
        )

    print(f'{starttime} starttime')
    print(f'{endtime} endtime')
    data = api.get_candles(symbol='BTCUSDT', interval='1h',
                           starttime=str(starttime), endtime=str(endtime),
                           limit=1000)

    pd_data_from_dict = pd.DataFrame.from_dict(data)
    pd_data = pd_data_from_dict if counter == 1 else pd.concat([pd_data, pd_data_from_dict])

    if endtime.year == today_year and endtime.month == today_month and endtime.day == today_day:
        break

    month += 1
    if month == 13:
        year += 1
        month = 2
        day = 1
    elif month == 12 and day == 1:
        day = 31

pd_data_time = list(map(lambda i: int(str(i)[:-3]) + 1, pd_data['ot']))
pd_data['ot'] = list(map(lambda i: TimeConverter.sec_to_date(i, 7200), pd_data_time))
pd_data['c'] = pd_data['c'].astype(float)
pd_data['o'] = pd_data['o'].astype(float)
pd_data['h'] = pd_data['h'].astype(float)
pd_data['l'] = pd_data['l'].astype(float)
pd_data = pd_data.set_index('ot')
pd_data = pd_data[['o', 'h', 'l', 'c']]
mask = (pd_data.index > '2021-12-31') & (pd_data.index <= '2022-01-02')

print(pd_data.loc[mask])
