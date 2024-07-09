from datetime import datetime, timedelta
import calendar

def days_in_month(year: int, month: int) -> int:
    """
    Returns the number of days in a given month of a year.

    Args:
        year (int): The year.
        month (int): The month.

    Returns:
        int: The number of days in the month.
    """
    return calendar.monthrange(year, month)[1]


def get_elapsed_date(news_parsed_data: dict, months: int) -> bool:
    """
    Determines if the news date is within the specified number of months from the current date.

    Args:
        news_parsed_data (dict): A dictionary containing news data, including the date.
        months (int): The number of months to check.

    Returns:
        bool: True if the news date is within the specified number of months, False otherwise.
    """
    news_date_str = news_parsed_data.get('date', '')
    news_date = datetime.strptime(news_date_str, "%B %d, %Y").date()

    current_date = datetime.now().date()
    days_passed = (current_date - current_date.replace(day=1)).days

    if months >= 2:
        for i in range(1, months):
            previous_month = (current_date.month - i - 1) % 12 + 1
            previous_year = current_date.year - ((current_date.month - i - 1) // 12)
            days_passed += days_in_month(previous_year, previous_month)

    date_diff = current_date - news_date
    return date_diff <= timedelta(days=days_passed)
