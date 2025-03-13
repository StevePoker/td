from binance.client import Client
from api_manager.hepler.TimeFormatter import TimeConverter


class BinanceAPI:

    def __init__(self):
        self.client = Client(api_key='S6FYO34BAW0W0JC7W574', api_secret='fg59nFCPOIDZdQIiYZO0jicVT9LmDDfXLtZUKTA9')

    @staticmethod
    def __add_headers(candles):
        candles_dict = dict(ot=[], o=[], h=[],
                            l=[], c=[], ct=[])
        for i in candles:
            candles_dict['ot'].append(i[0])
            candles_dict['o'].append(i[1])
            candles_dict['h'].append(i[2])
            candles_dict['l'].append(i[3])
            candles_dict['c'].append(i[4])
            candles_dict['ct'].append(i[6])

        return candles_dict

    def get_candles(self, symbol, starttime=None, endtime=None, interval=None, limit=None):

        starttime = str(TimeConverter.date_to_sec(starttime)) + '000' if starttime else starttime
        endtime = str(TimeConverter.date_to_sec(endtime)) + '000' if endtime else endtime

        candles = self.client.get_klines(symbol=symbol,
                                         interval=interval,
                                         startTime=int(starttime) if starttime else None,
                                         endTime=int(endtime) if endtime else None,
                                         limit=limit)
        candles = self.__add_headers(candles)

        return candles
