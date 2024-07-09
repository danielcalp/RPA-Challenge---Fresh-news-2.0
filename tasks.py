from robocorp import storage
from robocorp.tasks import task
from scripts.get_news import start_get_news
from scripts.save_as_csv import save_to_excel
from scripts.remove_files import remove_profile_files
import logging
from datetime import datetime
import os


def check_folder_exists(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


def logging_config():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'app_{timestamp}.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(f'logs/{log_filename}'),  # Log file
                            logging.StreamHandler()  # Console
                        ])


@task
def main() -> None:
    """
    Main task function that retrieves news data, saves it to an Excel file and removes useless files.
    """
    # Check if each folder exists
    output_folder_list = ['output', 'output/images', 'logs']
    for output_folder in output_folder_list:
        check_folder_exists(output_folder)

    # Load logging config
    logging_config()

    # Send message to logger file
    logging.info(f'The script has started')

    # Load configuration variables from storage
    variables = storage.get_json('Variables')
    
    # Extract variables from the configuration
    main_url = variables.get('main_url', '')
    search_input = variables.get('search_input', '')
    section = variables.get('section', '')
    months = variables.get('months', 0)
    
    # Retrieve news data
    news_data = start_get_news(main_url, search_input, section, months)
    
    # Save news data to an Excel file
    save_to_excel(news_data)

    # Remove useless files
    remove_profile_files()

    # Send message to logger file
    logging.info(f'The script has ended')