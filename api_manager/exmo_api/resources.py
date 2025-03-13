from enum import Enum


class Resources(Enum):
    CANDLES_HISTORY = {
        'endpoint': lambda symbol, resolution, from_sec, to_sec:
        f'v1.1/candles_history'
        f'?symbol={symbol}'
        f'&resolution={resolution}'
        f'&from={from_sec}'
        f'&to={to_sec}'
    }
    TICKER = {
        'endpoint': lambda:
            'v1.1/ticker'
    }

    @property
    def params(self):
        resources_list = {
            'CANDLES_HISTORY': {'required': {'symbol', 'resolution', 'from_sec', 'to_sec'},
                                'optional': {}
                                },
            'TICKER': {'required': set(),
                       'optional': set()
                       }
        }

        return resources_list.get(self.name)
