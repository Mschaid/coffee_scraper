# %%
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = 'https://www.drinktrade.com/coffee/all-coffee'


def get_links(url_=url):
    """

    """
    # set the driver
    # Getting all the links on the page.
    driver = webdriver.Chrome()
    driver_options = Options()
    driver_options.add_experimental_option('detatch', True)

    # go to page
    driver.get(url_)

    # ? click load more button until its gone - works, but #TODO  come back to this after testing if we can get all the links
    # while True:
    #     try:
    #         load_more = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[4]/div[2]/div/div[3]/button')
    #         sleep(2)
    #         load_more.click()
    #         sleep(2)
    #     except Exception as e:
    #         print(e)

    # TODO get all product links - working on this

    a_tags = driver.find_element(By.TAG_NAME, 'a')
    links = [a_tag.get_attribute('href') for a_tag in a_tags]
    return links

# %%
