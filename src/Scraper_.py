
# %%
import logging
import pickle 
import sys

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#create logger that logs to console
# logger = logging.getLogger(__name__)
# stream_handler = logging.StreamHandler(sys.stdout)
# logger.addHandler(stream_handler)
# logger.setLevel(logging.INFO)



# scrapper class that takes in url and optons and stores all links from product links

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

    def get_url(self):
        '''
        initializes driver and gets url connection
        '''
        self.driver.get(self.url)
        # return self

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
                
    def retrieve_links(self)->list:
        
        '''
        finds all priduct links and stores them in a list href_links
        '''          
        a_tags = self.driver.find_elements(By.CLASS_NAME, 'product-link')
        self.href_links = [a_tag.get_attribute('href') for a_tag in a_tags]
        
    
    def store_links(self):
        '''
        stores href_links in a pickle file in data directory
        '''
        current_path = os.getcwd()
        storeage_path = current_path.replace('src', 'data')
        with open(f'{storeage_path}/href_links.pkl', 'wb') as f:
            pickle.dump(self.href_links, f)
        

# if __name__ == '__main__':
scraper = Scraper('https://www.drinktrade.com/coffee/all-coffee', timeout=10, headless=False)
scraper.get_url() 
scraper.load_all()
scraper.retrieve_links()
scraper.store_links()

# %%
