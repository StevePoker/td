class DataFormatter:
    def __init__(self, data, data_type, market):
        self.full_data = dict(data)
        print(self.full_data)
        self.meta_data = self.full_data['Meta Data']
        self.data_type = data_type
        self.market = market

        if data_type == 'CRYPTO_INTRADAY':
            self.candles_data = self.full_data[f'Time Series Crypto ({self.meta_data.get("7. Interval")})']
        else:
            self.candles_data = self.full_data.get(
                f'Time Series ({self.data_type.replace("_", " ").title()})'
            )

    def alpha_to_plot_format(self) -> dict:
        if self.data_type == 'CRYPTO_INTRADAY':
            open, close, high, low, volume = \
                "1. open", \
                "4. close", \
                "2. high", \
                "3. low", \
                "5. volume"
        else:
            open, close, high, low, volume = \
                f"1a. open ({self.market})", \
                f"4a. close ({self.market})", \
                f"2a. high ({self.market})", \
                f"3a. low ({self.market})", \
                f"5. volume"

        formatted = {"Date": {}, "Open": {}, "Close": {}, "High": {}, "Low": {}, "Volume": {}}
        for index, period in enumerate(self.candles_data.keys()):
            formatted["Date"][f"{index}"] = period
            formatted["Open"][f"{index}"] = self.candles_data[period][open]
            formatted["Close"][f"{index}"] = self.candles_data[period][close]
            formatted["High"][f"{index}"] = self.candles_data[period][high]
            formatted["Low"][f"{index}"] = self.candles_data[period][low]
            formatted["Volume"][f"{index}"] = self.candles_data[period][volume]

        return formatted
