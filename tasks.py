import os
import logging
from datetime import datetime
from robocorp import storage
from robocorp.tasks import task
from scripts.get_news import start_get_news
from scripts.save_as_csv import save_to_excel
from scripts.remove_files import remove_profile_files


def check_folder_exists(output_folder: str) -> None:
    """
    Checks if a folder exists, and creates it if it doesn't.

    Args:
        output_folder (str): The path of the folder to check.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def configure_logging() -> None:
    """
    Configures the logging settings, including file and console handlers.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'app_{timestamp}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/{log_filename}'),
            logging.StreamHandler()
        ]
    )

@task
def main() -> None:
    """
    Main task function that retrieves news data, saves it to an Excel file, and removes unnecessary files.
    """
    # Ensure required folders exist
    output_folders = ['output', 'output/images', 'logs']
    for folder in output_folders:
        check_folder_exists(folder)

    # Configure logging
    configure_logging()

    # Log script start
    logging.info('The script has started')

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

    # Remove unnecessary files
    remove_profile_files()

    # Log script end
    logging.info('The script has ended')