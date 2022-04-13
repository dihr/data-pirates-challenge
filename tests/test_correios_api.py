from unittest import mock
from unittest.mock import Mock

import pytest

from correios_api.correios_api import BuscaFaixaCepApi


class TestBuscaFaixaCepApi:
    # Checks if the endpoint was generated correctly.
    @pytest.mark.parametrize(
        "expected",
        [
            "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
        ]
    )
    def test_get_endpoint(self, expected):
        api = BuscaFaixaCepApi()
        actual = api._get_end_point()
        assert actual == expected

    # Checks if the GET method is called within the method that loads the initial HTML
    @mock.patch('requests.get', return_value=Mock(status_code=200, json=lambda: {"data": {"id": "test"}}))
    def test_get_home(self, mock_request):
        api = BuscaFaixaCepApi()
        api.get_home()
        mock_request.assert_called_once()

    # Checks if the POST method is called within the method that loads the HTML with the data of each location
    @mock.patch('requests.post', return_value=Mock(status_code=200, json=lambda: {"data": {"id": "test"}}))
    def test_get_data(self, mock_request):
        api = BuscaFaixaCepApi()
        api.get_data()
        mock_request.assert_called_once()
