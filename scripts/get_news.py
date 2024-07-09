from RPA.Browser.Selenium import Selenium
from utils.selenium_utils import (
    open_site,
    search_in_browser,
    get_news_url_list,
    get_news_element,
    save_image_news
)
from utils.parse_data_utils import parse_news_data
from utils.check_date_utils import get_elapsed_date
from typing import List, Dict
import logging


def start_get_news(main_url: str, search_input: str, section: str, months: int) -> List[Dict[str, str]]:
    """
    Retrieves and processes news from Reuters website.

    Args:
        main_url (str): The URL of the main site to open.
        search_input (str): The search query.
        section (str): The section to search within.
        months (int): Number of months to consider for news data.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing parsed news data.
    """

    browser = Selenium()
    news_data = []

    try:
        open_site(browser, main_url)
        search_in_browser(browser, search_input, section)

        news_urls = get_news_url_list(browser, main_url)

        for url in news_urls:
            try:
                news_element = get_news_element(browser, url)
                parsed_data = parse_news_data(news_element, search_input)
                
                if not get_elapsed_date(parsed_data, months):
                    logging.info(f"The number of news items for the specified period has reached the limit")
                    break
                
                save_image_news(browser, parsed_data)
                news_data.append(parsed_data)

            except Exception as e:
                logging.debug(f"Error processing {url}: {e}")
                continue # Use raise or continue, depending on your case

    except Exception as e:
        logging.critical(f"An error occurred: {e}")
        html_content = browser.get_source()
        with open('output/website_now.html', 'w', encoding='utf-8') as file:
            file.write(html_content)
        html_list_element = browser.find_elements('//html')[0]
        html_list_element.screenshot(f'output/current_screen.png')
        if 'geo.captcha-delivery' in html_content:
            logging.critical(f"GeoCaptcha has been detected, please use a VPN or Proxy on your system")
        raise

    finally:
        browser.close_all_browsers()

    return news_data