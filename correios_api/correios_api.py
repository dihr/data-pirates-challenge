from abc import ABC, abstractmethod

import requests


class CorreiosApi(ABC):

    def __init__(self) -> None:
        self.base_url = "https://www2.correios.com.br/sistemas/buscacep"

    @abstractmethod
    def _get_end_point(self, **kwargs):
        pass

    def get_home(self, **kwargs) -> str:
        endpoint = self._get_end_point(**kwargs)
        response = requests.get(url=endpoint)
        response.raise_for_status()
        return response.text

    def get_data(self, **kwargs) -> str:
        start_page = kwargs.get('start', None)
        end_page = kwargs.get('end', None)
        uf = kwargs.get('uf', None)
        payload = {
            'UF': uf,
            'Localidade': '**',
            'qtdrow': 50,
        }

        if start_page and end_page:
            payload['pagini'] = start_page
            payload['pagfim'] = end_page

        endpoint = self._get_end_point(**kwargs)
        response = requests.post(url=endpoint, data=payload)
        response.raise_for_status()
        return response.text


class BuscaFaixaCepApi(CorreiosApi):
    def _get_end_point(self, **kwargs):
        return f"{self.base_url}/resultadoBuscaFaixaCEP.cfm"
