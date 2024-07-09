import re
from typing import Dict
import logging

def count_word(text: str, word: str) -> int:
    """
    Counts the number of occurrences of a word in a given text.

    Args:
        text (str): The text to search within.
        word (str): The word to count.

    Returns:
        int: The number of occurrences of the word.
    """
    return text.lower().count(word.lower())


def get_money_formats(text: str) -> bool:
    """
    Checks if the text contains any of the defined money formats.

    Args:
        text (str): The text to check for money formats.

    Returns:
        bool: True if any money formats are found, False otherwise.
    """
    money_patterns = [
        r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
        r'\b\d+\s+dollars?\b',
        r'\b\d+\s+USD\b',
    ]
    combined_pattern = '|'.join(money_patterns)
    matches = re.findall(combined_pattern, text, re.IGNORECASE)
    return bool(matches)


def parse_news_data(news_element, search_input: str) -> Dict[str, str]:
    """
    Parses news data from a news element.

    Args:
        news_element: The element containing news data.
        search_input (str): The search query to count occurrences of.

    Returns:
        Dict[str, str]: A dictionary with parsed news data.
    """
    parsed_data = {}

    # Extract and store news title
    title_xpath = './div/header/div/div/h1'
    title = news_element.find_element('xpath', title_xpath).text
    parsed_data['title'] = title
    
    # Extract and store news date
    date_xpath = './div/header/div/div/div/div[1]/time/span[1]'
    date = news_element.find_element('xpath', date_xpath).text
    parsed_data['date'] = date

    # Extract and store news description
    description_xpath = './div/div[@data-testid="ArticleBody"]'
    description = news_element.find_element('xpath', description_xpath).text
    parsed_data['description'] = description

    # Extract and store news image filename, if available
    picfile_xpath = './div/div[@data-testid="ArticleBody"]/div/div[1]//div[1]/div/img'
    
    try:
        picfile_url = news_element.find_element('xpath', picfile_xpath).get_attribute('src')
        picfile_name = picfile_url.split('/reuters/')[-1]
        parsed_data['pic filename'] = picfile_name
    
    except Exception as e:
        # Handling Unable to locate element error:
        if 'Unable to locate element' in str(e):
            logging.info(f'The news has no image:{title}')
            parsed_data['pic filename'] = ''
        else:
            logging.debug(f'The error needs to be handled:{e}')
            raise

    # Count occurrences of search input and check for money formats
    title_description_text = f"{title}\n{description}"
    parsed_data['count of search phrases in the news'] = count_word(title_description_text, search_input)
    parsed_data['contains money'] = get_money_formats(title_description_text)

    return parsed_data