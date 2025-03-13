import requests

from common_errors.exceptions import MissedParam, UnexpectedParam

from api_manager.alpha_api.utils.DataFormatter import DataFormatter
from api_manager.alpha_api.errors.exceptions import ResourceNotSetted
from api_manager.alpha_api.resources import Resources


class AlphaApi:

    def __init__(self, api_key):
        self._resource = None
        self._resource_url = None
        self._resource_name = None
        self._api_key = api_key

    def set_resource(self, resource):
        self._resource = Resources[f'{resource}']
        self._resource_url = self._resource.value['url']
        self._resource_name = self._resource.name

    def get(self, **params):
        if self._resource:
            self._params_checker(**params)

            full_url = self._resource_url(apikey=self._api_key, **params)
            r = requests.get(full_url)
            data = DataFormatter(data=r.json(), data_type=self._resource_name, market=params.get('market'))

            return data
        else:
            raise ResourceNotSetted(message='Please, set the resource before requesting data.')

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
