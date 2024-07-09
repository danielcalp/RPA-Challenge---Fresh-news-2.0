import pandas as pd
from typing import List, Dict
import logging

def save_to_excel(news_data: List[Dict[str, str]], file_path: str = "output/output.xlsx") -> None:
    """
    Saves a list of news data dictionaries to an Excel file.

    Args:
        news_data (List[Dict[str, str]]): A list of dictionaries containing news data.
        file_path (str): The path to the Excel file where the data will be saved.
    """
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(news_data)
    
    # Save the DataFrame to an Excel file
    try:
        logging.info(f'The data will be saved in excel')
        df.to_excel(file_path, index=False)
    except Exception as e:
        logging.critical(f'An error ocurred while saving excel file: {e}')
        raise
    logging.info(f'The data in excel file was saved successfully')