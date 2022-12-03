import logging
import sys

# local imports
from src.Scraper_ import Scraper

# TODO add logging
# TODO add product parsing to pandas dataframe
logger = logging.getLogger(__name__)
logging.basicConfig(filename='/Users/michaelschaid/GitHub/coffee_scraper/logs/main.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s - %(message)s')


def main(url):
    scraper = Scraper(url, timeout=20, headless=False)
    logger.info('Scraper initialized')

    scraper.get_url()
    logger.info('driver initialized')
    
    scraper.load_all()
    logger.info('all products loaded')

    scraper.retrieve_links()
    scraper.save_data(scraper.href_links, 'href_links')
    
    logger.info(f'total links collected and saved: {len(scraper.href_links)}')
    
    scraper.get_all_product_info()
    scraper.save_data(scraper.products_data, 'products_data')
    logger.info(f'all product info collected and saved to: {scraper.data_path}')

if __name__ == '__main__':
    url = 'https://www.drinktrade.com/coffee/all-coffee'
    main(url)
