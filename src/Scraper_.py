# %%
import pickle
import os


from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Scraper:

    def __init__(self, url, timeout, headless=False):
        self.url = url
        self.timeout = timeout
        self.headless = headless
        self.service = Service('/Users/michaelschaid/app_bins/chromedriver')
        self.options = Options()

        if self.headless == True:
            self.options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            service=self.service, options=self.options)

        self.current_path = os.getcwd()
        self.data_path = self.current_path.replace('src', 'data')

    def get_url(self):
        '''
        initializes driver and gets url connection
        '''
        self.driver.get(self.url)

    def load_all(self):
        '''
        finds loadmore button and clicks it until it is no longer visible
        '''
        while True:
            try:
                load_more = self.driver.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[2]/div/div[4]/div[2]/div/div[3]/button')
                sleep(self.timeout)
                load_more.click()
                sleep(self.timeout)
                return self.load_all()
            except:
                return None

    def retrieve_links(self) -> list:
        '''
        finds all priduct links and stores them in a list href_links
        '''
        a_tags = self.driver.find_elements(By.CLASS_NAME, 'product-link')
        self.href_links = [a_tag.get_attribute('href') for a_tag in a_tags]

    def save_data(self, data, file_name):
        '''
        stores data in a pickle file in data directory
        '''
        with open(f'{self.data_path}/{file_name}.pkl', 'wb') as f:
            pickle.dump(data, f)
            f.close()

    def load_links(self):
        '''
        loads href_links from pickle file in data directory
        '''
        try:
            with open(f'{self.data_path}/href_links.pkl', 'rb') as f:
                self.href_links = pickle.load(f)
                f.close()
        except FileNotFoundError:
            'there is no href_links.pkl file in data directory, did you run the scraper?'

    def get_product_info(self, url):
        """# Summary:
        This function takes a url and returns data scraped from the input url. It uses the instance driver
        The primary purpose of this function is to be used as a helper function when scraping multiple urls, but can be used on its own to scrape a single url

        ## Returns:
            dictioary: returns brand, roaster location product name, notes, product description, and prices
        """

        self.driver.get(url)
        sleep(5)

        product_info = self.driver.find_element(
            By.CLASS_NAME, 'pdp-collections__sidebar-wrapper').text.split("\n")

        process_method = self.driver.find_element(
            By.CLASS_NAME, 'list-value').text

        roaster_notes = self.driver.find_element(
            By.CLASS_NAME, 'roaster-notes-body').text

        product_data = {
            'brand': product_info[0],
            'roaster_location': product_info[1],
            'product_name': product_info[2],
            'product_notes': product_info[3],
            'process_method': process_method,
            'roaster_notes': roaster_notes,
            'product_description': product_info[4],
            'single_purchace_price': product_info[6],
            'single_shipping_price': product_info[7],
            'subscription_price': product_info[9],
            'subscription_shipping_price': product_info[10],
            'roast_collection': product_info[11]
        }
        return (product_data)

    def get_all_product_info(self):
        """# Summary:
        This function calls the get_product_info function on all urls in the href_links list of the instance. Its purpose is to gerenate a data set from the href links of the isntance
        ## Returns:
            dictioary: key is the product id, and value is the dictionary of product info
        """
        self.products_data = {link.split(
            '/')[-1]: self.get_product_info(link) for link in self.href_links}
