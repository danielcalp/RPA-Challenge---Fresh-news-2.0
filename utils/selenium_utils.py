from typing import List, Dict
from RPA.Browser.Selenium import Selenium
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def open_site(browser: Selenium, main_url: str) -> None:
    """
    Opens the main URL in the browser using Firefox.

    Args:
        browser (Selenium): The browser instance to use.
        main_url (str): The URL of the main site to open.
    """
    options = FirefoxOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--incognito')
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/127.0")
    options.add_argument("-profile")
    options.add_argument('5if5a9hx.project_profile')
    try:
        logging.info(f'The browser will launch browser and load website: {main_url}')
        browser.open_available_browser(main_url, browser_selection="Firefox", options=options)
    except Exception as e:
        logging.critical(f'An error occurred after starting the browser and loading the website: {e}')
        raise


def search_in_browser(browser: Selenium, search_input: str, section: str) -> None:
    """
    Performs a search in the browser and selects a section.

    Args:
        browser (Selenium): The browser instance to use.
        search_input (str): The search query.
        section (str): The section to select.
    """
    user_agent = browser.execute_javascript("return navigator.userAgent;")
    logging.info(f'Your actualy user-agent is: {user_agent}')

    try:
        browser.wait_until_element_is_visible('//*[@id="onetrust-reject-all-handler"]', timeout=10)
        browser.click_element('//*[@id="onetrust-reject-all-handler"]')
    except:
        pass
    
    browser.wait_until_element_is_visible('//button[@aria-label="Open search bar"]', timeout=10)
    browser.click_element('//button[@aria-label="Open search bar"]')

    browser.wait_until_element_is_visible('//input[@type="search"]', timeout=10)
    browser.input_text('//input[@type="search"]', search_input)
    
    browser.wait_until_element_is_visible('//button[@aria-label="Search"]', timeout=10)
    browser.click_element('//button[@aria-label="Search"]')
    
    browser.wait_until_element_is_visible('//button[@id="sectionfilter"]', timeout=10)
    browser.click_element('//button[@id="sectionfilter"]')
    
    browser.wait_until_element_is_visible(f'//li[@role="option"]/span[text()="{section}"]', timeout=10)
    browser.click_element(f'//li[@role="option"]/span[text()="{section}"]')


def get_news_url_list(browser: Selenium, main_url: str) -> List[str]:
    """
    Retrieves a list of news URLs from the search results.

    Args:
        browser (Selenium): The browser instance to use.
        main_url (str): The base URL of the news site.

    Returns:
        List[str]: A list of news URLs.
    """
    news_urls = []

    while True:
        browser.wait_until_element_is_visible('//li[contains(@class, "search-results")]', timeout=10)
        news_elements = browser.find_elements('//li[contains(@class, "search-results")]')
        
        for element in news_elements:
            href = element.find_element('xpath', './/div').get_attribute('href')
            if href:
                news_urls.append(main_url + href[1:])
        
        browser.wait_until_element_is_visible('//div[contains(@class, "search-results")]/button[2][@data-testid="Button"]', timeout=10)
        next_page_button = browser.find_element('//div[contains(@class, "search-results")]/button[2][@data-testid="Button"]')
        if next_page_button.get_attribute('aria-label') == 'Disabled':
            break
        
        browser.click_element('//div[contains(@class, "search-results")]/button[2][@data-testid="Button"]')

    return news_urls


def get_news_element(browser: Selenium, url: str) -> Selenium:
    """
    Retrieves the news element from a given URL.

    Args:
        browser (Selenium): The browser instance to use.
        url (str): The URL of the news article.

    Returns:
        Selenium: The news element.
    """
    browser.go_to(url)
    news_data_element = '//article[@data-testid="Article"]/div[contains(@class, "article__main")]'
    browser.wait_until_element_is_visible(news_data_element, timeout=10)
    return browser.find_element(news_data_element)


def save_image_news(browser: Selenium, news_data: Dict[str, str]) -> None:
    """
    Saves the news image to a file.

    Args:
        browser (Selenium): The browser instance to use.
        news_data (Dict[str, str]): A dictionary containing news data, including the image filename.
    """
    pic_filename = news_data.get('pic filename', '')
    if not pic_filename:
        return
    
    image_url = f'https://cloudfront-us-east-2.images.arcpublishing.com/reuters/{pic_filename}'

    for counter in range(2):
        try:
            browser.go_to(image_url)
            image_xpath = '//img'
            browser.wait_until_element_is_visible(image_xpath, timeout=10)
            break
        except Exception as e:
            logging.warning(f'Error to find image xpath: {image_xpath} and error was raised: {e}')
            logging.info(f'A new attempt will be made for the URL {image_url}')
            pass
        if counter == 1:
            logging.error(f'The error persists, the script will continue without the image')
            return
    
    image_element = browser.find_element('//img')
    image_element.screenshot(f'output/images/{pic_filename}')