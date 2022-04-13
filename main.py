import logging

from correios_api.correios_api import BuscaFaixaCepApi
from data_writer.data_writer import DataWriter
from scraper.scraper import ZipCodeRangeScraper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logger.info("Starting the api services...")
    api = BuscaFaixaCepApi()

    logger.info("Starting the writer services...")
    writer = DataWriter(file_extension='jsonl')

    logger.info("Starting the scraper services...")
    scraper = ZipCodeRangeScraper(writer=writer, api=api)

    logger.info("Data scraping...")
    scraper.start_scraping()
