from unittest import mock

import pytest

from correios_api.correios_api import BuscaFaixaCepApi
from data_writer.data_writer import DataWriter
from scraper.scraper import ZipCodeRangeScraper


class TestZipCodeRangeScraper:
    @pytest.mark.parametrize(
        ("data", "expected"),
        [
            (["Amparo", "13550-000 a 13559-999"]
             , {
                 'location': "Amparo",
                 'zip_code_hate': "13550-000 a 13559-999",
             })
        ]
    )
    def test_parse_zip_code_range_to_obj(self, data, expected):
        s = ZipCodeRangeScraper(
            api=BuscaFaixaCepApi(),
            writer=DataWriter(file_extension=',jsonl'),
        )
        actual = s._parse_zip_code_range_to_obj(data=data)
        assert actual['location'] == expected['location']
        assert actual['zip_code_hate'] == expected['zip_code_hate']


    @pytest.mark.parametrize(
        ("data", "expected_location", "expected_zip_code_range"),
        [
            ("AC", "Assis Brasil", "69935-000 a 69939-999")
        ]
    )
    def test_scrap_zip_code_range_from_page(self, data, expected_location, expected_zip_code_range):
        s = ZipCodeRangeScraper(
            api=BuscaFaixaCepApi(),
            writer=DataWriter(file_extension='.jsonl'),
        )
        actual = s._scrap_zip_code_range_from_page(uf=data, start=None, end=None)
        uf_data = actual[0]
        assert uf_data[1][0] == expected_location
        assert uf_data[1][1] == expected_zip_code_range

    @mock.patch('scraper.scraper.ZipCodeRangeScraper._scrap_uf_options_from_home_page', return_value=['AC'])
    @mock.patch('correios_api.correios_api.CorreiosApi.get_data', return_value="")
    def test_start_scrapping(self, mock_api_home_ufs, mock_api_get_data):
        s = ZipCodeRangeScraper(
            api=BuscaFaixaCepApi(),
            writer=DataWriter(file_extension='.jsonl'),
        )
        s.start_scraping()
        mock_api_get_data.assert_called_once()