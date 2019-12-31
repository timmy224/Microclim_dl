""" downloads Microclim dataset by Michael Kearney, Andrew Paul Isaac, Warren Paul Porter"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://springernature.figshare.com/collections/microclim_Global_estimates_of_hourly_microclimate_based_on_long_term_monthly_climate_averages/878253'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

def lazyLoadScroll():
    """scrolls, waits for all thumbnails to load"""
    time.sleep(5)
    bodyElem = driver.find_element_by_tag_name('body')
    no_of_pagedowns = 10

    while no_of_pagedowns:
        bodyElem.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        no_of_pagedowns -= 1

def getListofLinks():
    """gets individual links for each bioclim variable for different resolutions
    returns: links {list}
    """
    variable_urls = []

    thumbnails = driver.find_elements_by_xpath("//div[contains(@class, 'item-thumb-card')]")
    no_thumbnails = len(thumbnails)

    for i in range(1, no_thumbnails+1):
        link_xpath = driver.find_element_by_xpath("//div[contains(@class,\
                                                  'item-thumb-card')]{}//a".format([i]))
        link = link_xpath.get_attribute('href')
        variable_urls.append(link)

    return variable_urls

def auto_downloads():
    """downloads each variable"""
    links = getListofLinks()
    
    for i in links:
        print('Downloading from: ', i)
        driver.get(i)
        time.sleep(3)
        dl_button_xpath = "//a[contains(@class, 'download-button')]"
        dl_button = driver.find_element_by_xpath(dl_button_xpath)
        dl_button.click()

    print('Dataset has finished downloading!')

lazyLoadScroll()
getListofLinks()
auto_downloads()