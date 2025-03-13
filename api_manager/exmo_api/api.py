import requests

from common_errors.exceptions import MissedParam, UnexpectedParam
from api_manager.exmo_api.resources import Resources


class ExmoAPI:
    __exmo_base_url = 'https://api.exmo.com/'

    def __init__(self, api_key=None):
        self._api_key = api_key
        self._resource = None
        self.url = None

    def _get(self, url, params):
        response = self._session.get(url, params=params)
        return response

    @property
    def _session(self):
        session = requests.Session()
        # session.headers.update({})

        return session

    def _set_resource(self, resource_name):
        self._resource = Resources[resource_name]

    def _generate_url(self, **params):
        endpoint = self._resource.value.get('endpoint')(**params)
        self.url = f'{self.__exmo_base_url}{endpoint}'

    def _params_checker(self, **params):
        required_params = self._resource.params.get('required')
        optional_params = self._resource.params.get('optional')

        check1 = required_params.difference(set(params.keys()))
        if check1:
            message = f'Missed parameters: {check1}'
            raise MissedParam(message)

        check2 = set(params.keys()).difference(required_params)
        check3 = check2.difference(optional_params)
        if check3:
            message = f'Unexpected parameters: {check3}'
            raise UnexpectedParam(message)

        return True

    def get_candles_history(self, **params):
        self._set_resource('CANDLES_HISTORY')
        state = self._params_checker(**params)

        if state:
            self._generate_url(**params)

            response = self._session.get(self.url)

            return response.json()

    def get_ticker(self, **params):
        self._set_resource('TICKER')
        state = self._params_checker(**params)

        if state:
            self._generate_url(**params)

            response = self._session.get(self.url)

            return response.json()
