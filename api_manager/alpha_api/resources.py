from enum import Enum


class Resources(Enum):
    CRYPTO_INTRADAY = {
        'url': lambda symbol, market, interval, apikey, outputsize=None:
        f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY'
        f'&symbol={symbol}'
        f'&market={market}'
        f'&interval={interval}'
        f'&apikey={apikey}'
        f'&outputsize={outputsize}'
    }

    DIGITAL_CURRENCY_DAILY = {
        'url': lambda symbol, market, apikey:
        f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY'
        f'&symbol={symbol}'
        f'&market={market}'
        f'&apikey={apikey}'
    }

    DIGITAL_CURRENCY_WEEKLY = {
        'url': lambda symbol, market, apikey:
        f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY'
        f'&symbol={symbol}'
        f'&market={market}'
        f'&apikey={apikey}'
    }

    DIGITAL_CURRENCY_MONTHLY = {
        'url': lambda symbol, market, apikey:
        f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY'
        f'&symbol={symbol}'
        f'&market={market}'
        f'&apikey={apikey}'
    }

    @property
    def params(self):
        resources_list = {
            'CRYPTO_INTRADAY': {'required': {'symbol', 'market', 'interval'},
                                'optional': {'outputsize'}
                                },
            'DIGITAL_CURRENCY_DAILY': {'required': {'symbol', 'market'},
                                       'optional': {}
                                       },
            'DIGITAL_CURRENCY_WEEKLY': {'required': {'symbol', 'market'},
                                        'optional': {}
                                        },
            'DIGITAL_CURRENCY_MONTHLY': {'required': {'symbol', 'market'},
                                         'optional': {}
                                         }
        }

        return resources_list.get(self.name)
