# Robocorp Reuters News Automation

## Overview

This project is a Python-based automation solution for extracting news data from the Reuters website. It was developed as part of the test for the Python Automation Engineer position. The goal is to showcase the ability to build a bot that automates the process of extracting and processing news data using Robocorp's RPA Framework.

## 🟢 The Challenge

The task is to automate the process of extracting news data from a chosen news site. For this test, the Reuters website was selected. The automation includes:

1. Opening the news site.
2. Entering a search phrase and selecting a news category.
3. Extracting news details such as title, date, description, and picture.
4. Saving the data into an Excel file.
5. Processing news based on a specified number of months.

### The Source

The automation is implemented for the [Reuters](https://www.reuters.com/) website.

### Parameters

The process requires the following parameters via a Robocloud work item:

- `main_url`: The Reuters link do access the website.
- `search_input`: The phrase to search for in the news.
- `section`: The category or section of the news.
- `months`: The number of months to retrieve news for (e.g., 1 for the current month, 2 for the current and previous month).

### The Process

1. **Open the Site**: Navigate to the Reuters website.
2. **Search**: Enter the search phrase and select the news section.
3. **Retrieve News**: Collect news URLs and extract details from each news article.
4. **Extract Data**:
    - Title
    - Date
    - Description
    - Picture filename
    - Count of search phrases in the title and description
    - Whether the title or description contains monetary amounts
5. **Save Data**: Store the extracted data in an Excel file, including downloaded news pictures.
5. **Delete files**: Deletes files generated after starting the script, keeping space consumption low.

## Requirements

- Python 3.8+
- Robocorp Framework
- Pandas
- Selenium
- Firefox

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/danielcalp/RPA_Challenge_Fresh_news_2.0.git
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Set Up Parameters**: Define the parameters in the Robocloud work item or configure them in a configuration file.
2. **Run the Automation**: Execute the main task using Robocorp Control Room or local execution.

## Attention

If GeoCaptcha error occurs, please insert a VPN or Proxy into the system

## Code Overview

- **`selenium_utils.py`**: Contains utility functions for interacting with the browser.
- **`parse_data_utils.py`**: Functions for parsing news data and checking for monetary values.
- **`check_date_utils.py`**: Functions for handling and comparing dates.
- **`task.py`**: The entry point that coordinates the automation workflow.
- **`save_as_csv.py`**: Handles saving the extracted data to an Excel file.
- **`remove_files.py`**: Handles deleting generated files from Firefox profile..

## Example

To run the automation locally, you can use the following command:

```bash
python task.py
Ensure that the parameters are correctly set in the Variables configuration file or passed via Robocloud work item.

Best Practices and Considerations
Code Quality: The code adheres to PEP8 standards and follows clean code practices.
Resiliency: The automation is fault-tolerant and includes error handling for both application and website issues.
Logging and Debugging: Proper logging should be implemented for real-world use (e.g., using Python's logging module).
License
This project is licensed under the MIT License.

Contact
For any questions or further information, please contact Your Name.