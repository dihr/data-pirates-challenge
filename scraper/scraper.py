import logging
import uuid
from abc import ABC

from correios_api.correios_api import CorreiosApi
from data_writer.data_writer import DataWriter
from bs4 import BeautifulSoup as soup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataScraper(ABC):
    def __init__(self, writer: DataWriter, api: CorreiosApi) -> None:
        self.api = api
        self.writer = writer

    def start_scraping(self) -> None:
        pass


class ZipCodeRangeScraper(DataScraper):

    def start_scraping(self):
        uf_list = self._scrap_uf_options_from_home_page()

        for uf in uf_list[1:]:
            logger.info(f"getting zip code range of uf: {uf}")
            uf_zip_code_range_list = []

            # Get uf data from home page
            zip_code_range, has_next_page = self._scrap_zip_code_range_from_page(uf=uf)
            for value in zip_code_range:
                uf_zip_code_range_list.append(self._parse_zip_code_range_to_obj(value))

            # Goes through next pages
            start_page_param = 51
            end_page_param = 100
            while has_next_page:
                zip_code_range, has_next_page = self._scrap_zip_code_range_from_page(uf=uf, start=start_page_param,
                                                                                     end=end_page_param)
                for value in zip_code_range:
                    uf_zip_code_range_list.append(self._parse_zip_code_range_to_obj(value))

                start_page_param += 50
                end_page_param += 50

            # Remove duplicates
            unique_values = self.remove_duplicates(uf_zip_code_range_list)

            # Generate unique id
            for u_values in unique_values:
                u_values['id'] = uuid.uuid4().hex

            # Save data into file
            logger.info(f"{len(uf_zip_code_range_list)} locations founded to uf: {uf}")
            self.writer.write_location_data(file_name=uf, data=unique_values)

    def _scrap_uf_options_from_home_page(self) -> list:
        uf_list = []
        page_soup = soup(self.api.get_home(), "html.parser")
        for uf in page_soup.find("select", {"class": "f1col"}).findAll("option"):
            uf_list.append(uf.text)
        return uf_list

    def _scrap_zip_code_range_from_page(self, uf, **kwargs):
        start_page = kwargs.get('start', None)
        end_page = kwargs.get('end', None)

        zip_code_range = []
        page_soup = soup(self.api.get_data(uf=uf, start=start_page, end=end_page), "html.parser")
        founded_tables = page_soup.findAll("table", {"class": "tmptabela"})
        if len(founded_tables) == 1:
            for row in founded_tables[0].findAll("tr"):
                cols = row.findAll("td")
                if cols:
                    cols = [ele.text.strip() for ele in cols]
                    zip_code_range.append([ele for ele in cols if ele])
        else:
            for row in founded_tables[1].findAll("tr"):
                cols = row.findAll("td")
                if cols:
                    cols = [ele.text.strip() for ele in cols]
                    zip_code_range.append([ele for ele in cols if ele and cols])

        # Check if there is next page
        has_next_page = page_soup.find("div", {"class": "ctrlcontent"}).find('form', {"name": "Proxima"})

        return zip_code_range, has_next_page

    def _parse_zip_code_range_to_obj(self, data) -> dict:
        return {
            'location': data[0],
            'zip_code_range': data[1],
        }

    def remove_duplicates(self, data):
        new_list = [data[0]]
        for e in data:
            if e not in new_list:
                new_list.append(e)
        return new_list
